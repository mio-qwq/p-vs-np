#!/usr/bin/env python3
"""Verify frozen scope certificates using only the Python standard library.

All mutations and checker-generated files are confined to temporary copies.
No asserts, downloaded code, third-party dependencies, or network access.
"""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
PAYLOAD = (
    'PROVENANCE.json',
    'README.md',
    'affine-layer/REPORT.md',
    'affine-layer/REVIEW.md',
    'affine-layer/certificate.json',
    'affine-layer/check-normal.json',
    'affine-layer/check-optimized.json',
    'affine-layer/check.py',
    'affine-layer/negative-control.txt',
    'extremal-transfer/RESULT.md',
    'extremal-transfer/REVIEW.md',
    'extremal-transfer/check.py',
    'extremal-transfer/results.json',
    'support-mask/REPORT.md',
    'support-mask/check.py',
    'support-mask/results.json',
    'verification.json',
    'verify.py',
)
ALL_FILES = set(PAYLOAD) | {'manifest.json', 'SHA256SUMS'}
MODE = int(sys.flags.optimize)

def require(condition, message):
    if not condition:
        raise ValueError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def read_json(path):
    def no_duplicates(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, 'Duplicate JSON key: ' + key)
            result[key] = value
        return result
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=no_duplicates)

def integrity(root):
    actual = set()
    allowed_dirs = {str(PurePosixPath(name).parent) for name in ALL_FILES} - {'.'}
    for item in root.rglob('*'):
        name = item.relative_to(root).as_posix()
        require(not item.is_symlink(), 'Symlink is not permitted: ' + name)
        if item.is_dir():
            require(name in allowed_dirs, 'Unexpected directory: ' + name)
        else:
            require(item.is_file(), 'Non-regular file: ' + name)
            actual.add(name)
    require(actual == ALL_FILES, 'File inventory mismatch: missing=' + str(sorted(ALL_FILES-actual)) + ', unexpected=' + str(sorted(actual-ALL_FILES)))
    manifest = read_json(root/'manifest.json')
    require(manifest['schema'] == 'colored-fiber-scope-manifest-v1', 'Manifest schema mismatch')
    require(manifest['algorithm'] == 'sha256', 'Manifest algorithm mismatch')
    require(manifest['expected_base_commit'] == '94d094d82d14e15729cac0b478d0d6f1bec33de9', 'Dependency commit mismatch')
    entries = manifest['files']
    require([entry['path'] for entry in entries] == sorted(PAYLOAD), 'Manifest path list mismatch')
    for entry in entries:
        content = (root/entry['path']).read_bytes()
        require(len(content) == entry['bytes'], 'Size mismatch: ' + entry['path'])
        require(sha(content) == entry['sha256'], 'Hash mismatch: ' + entry['path'])
    expected_sums = ''.join(sha((root/name).read_bytes()) + '  ' + name + '\n' for name in sorted(set(PAYLOAD) | {'manifest.json'}))
    require((root/'SHA256SUMS').read_text(encoding='utf-8') == expected_sums, 'SHA256SUMS mismatch')
    return len(actual)

def run(root, script, *args, expected_exit=0):
    flags = ['-B'] + (['-' + 'O'*MODE] if MODE else [])
    command = [sys.executable] + flags + [str(root/script)] + list(args)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0')
    process = subprocess.run(command, cwd=str((root/script).parent), env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
    if expected_exit == 0:
        require(process.returncode == 0, script + ' failed: ' + process.stderr.decode('utf-8', errors='replace'))
        require(not process.stderr, script + ' emitted unexpected stderr')
    else:
        require(process.returncode != 0, script + ' accepted a negative control')
    return process

def check_mathematics(root):
    with tempfile.TemporaryDirectory(prefix='colored-fiber-math-') as directory:
        work = Path(directory)/'package'
        shutil.copytree(root, work)
        affine = run(work, 'affine-layer/check.py')
        result = json.loads(affine.stdout)
        mode_file = 'check-optimized.json' if MODE else 'check-normal.json'
        frozen = read_json(work/'affine-layer'/mode_file)
        # -OO is supported as well; only the interpreter metadata can differ.
        frozen['optimization'] = MODE
        require(result == frozen, 'Affine output differs from frozen certificate')
        require(result['status'] == 'PASS', 'Affine checker did not pass')

        support = run(work, 'support-mask/check.py')
        require((work/'support-mask/results.json').read_bytes() == (root/'support-mask/results.json').read_bytes(), 'Support certificate differs')
        support_data = read_json(work/'support-mask/results.json')
        require(support_data['status'] == 'PASS', 'Support checker did not pass')

        extremal = run(work, 'extremal-transfer/check.py')
        require(json.loads(extremal.stdout) == read_json(root/'extremal-transfer/results.json'), 'Extremal counts differ')
        extremal_data = json.loads(extremal.stdout)
        total = sum(item['extremal_checks'] for item in extremal_data.values())
        require(total == 31380, 'Extremal total mismatch')

        bad = read_json(work/'affine-layer/certificate.json')
        bad['costs'][0] += 1
        bad_path = work/'affine-layer/altered-certificate.json'
        bad_path.write_text(json.dumps(bad), encoding='utf-8')
        negative = run(work, 'affine-layer/check.py', '--certificate', str(bad_path), expected_exit=1)
        require(b'Integer matrix fails to realize the stated exact layer' in negative.stderr, 'Unexpected negative-control failure')
        return {
            'affine': {'status':'PASS', 'binary_matrices':result['binary_matrices_checked'], 'constant_on_family':result['binary_matrices_constant_on_family'], 'polynomial_coefficients_low_to_high':result['polynomial_coefficients_low_to_high']},
            'support': {'status':'PASS', 'results_sha256':sha((work/'support-mask/results.json').read_bytes()), 'binary_3x3_determinants':support_data['binary_3x3_determinants']},
            'extremal': {'status':'PASS', 'checks':total},
            'altered_integer_certificate_rejected':True,
        }

def corruption_controls(root):
    controls = []
    for kind in ('modified_file', 'missing_file', 'unexpected_file', 'altered_manifest'):
        with tempfile.TemporaryDirectory(prefix='colored-fiber-corruption-') as directory:
            work = Path(directory)/'package'
            shutil.copytree(root, work)
            if kind == 'modified_file':
                target = work/'affine-layer/REPORT.md'
                target.write_bytes(target.read_bytes()+b'corruption\n')
            elif kind == 'missing_file':
                (work/'affine-layer/certificate.json').unlink()
            elif kind == 'unexpected_file':
                (work/'unlisted.txt').write_text('unexpected\n')
            else:
                target = work/'manifest.json'
                data = read_json(target)
                data['files'][0]['sha256'] = '0'*64
                target.write_text(json.dumps(data))
            rejected = False
            try:
                integrity(work)
            except (ValueError, KeyError, OSError):
                rejected = True
            require(rejected, 'Corruption control was accepted: ' + kind)
            controls.append(kind)
    return controls

def main():
    count = integrity(ROOT)
    mathematical = check_mathematics(ROOT)
    controls = corruption_controls(ROOT)
    integrity(ROOT)
    result = {
        'status':'PASS',
        'optimization':MODE,
        'file_count':count,
        'integrity':'PASS',
        'clean_temporary_copy':True,
        'source_files_unchanged':True,
        'mathematical_checks':mathematical,
        'rejected_packaging_corruptions':controls,
        'scope':'Finite scope certificates and structural proofs; no ASNC or P-versus-NP claim.',
    }
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, OSError, subprocess.SubprocessError) as error:
        print('FAIL: '+str(error), file=sys.stderr)
        sys.exit(1)
