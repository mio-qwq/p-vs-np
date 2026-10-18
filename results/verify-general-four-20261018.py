#!/usr/bin/env python3
"""Verify the compact general four-row result in clean temporary storage.

Run this once normally and once with -O. Each invocation uses its interpreter
mode for every child checker; no validation depends on Python assertions.
"""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
MANIFEST = 'manifest-general-four-20261018.json'
RESULT = 'monic-four-general'
PROOF_SHA256 = '5bb505df254bda0212944fe3a02b25fcdcedbda032c4b5af0055f83009d0c5e5'


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_relative(value):
    path = Path(value)
    require(isinstance(value, str) and value and not path.is_absolute()
            and '..' not in path.parts and '\\' not in value,
            'unsafe manifest path: ' + str(value))
    return path


def verify_manifest(root, manifest):
    seen = set()
    for item in manifest['files']:
        rel = safe_relative(item['path'])
        require(str(rel) not in seen, 'duplicate manifest path: ' + str(rel))
        seen.add(str(rel))
        path = root / rel
        require(not path.is_symlink(), 'symlink source: ' + str(rel))
        require(path.is_file(), 'missing manifest source: ' + str(rel))
        data = path.read_bytes()
        require(len(data) == item['bytes'], 'manifest size mismatch: ' + str(rel))
        require(digest(data) == item['sha256'], 'manifest hash mismatch: ' + str(rel))
    actual = {str(p.relative_to(root)) for p in (root / RESULT).rglob('*')
              if p.is_file() or p.is_symlink()}
    expected = {p for p in seen if p.startswith(RESULT + '/')}
    require(actual == expected, 'unexpected or unlisted result source')
    require(digest((root / RESULT / 'PROOF.md').read_bytes()) == PROOF_SHA256,
            'frozen proof mismatch')
    status = json.loads((root / RESULT / 'STATUS.json').read_text())
    require(status['status'] == 'PASS', 'independent audit is not PASS')
    require(status['proof_sha256'] == PROOF_SHA256, 'audit covers different proof')
    require(status['proof_bytes_frozen'] is True, 'proof preservation not recorded')


def reject(call, expected):
    try:
        call()
    except RuntimeError as error:
        require(expected in str(error), 'negative control failed for wrong reason: ' + str(error))
    else:
        raise RuntimeError('negative control unexpectedly accepted: ' + expected)


def main():
    require(sys.version_info >= (3, 10), 'Python 3.10+ required')
    require(importlib.util.find_spec('sympy') is not None, 'Install sympy==1.14.0')
    import sympy
    require(sympy.__version__ == '1.14.0', 'Audited environment requires sympy==1.14.0')
    manifest = json.loads((HERE / MANIFEST).read_text())
    verify_manifest(HERE, manifest)
    config = json.loads((HERE / RESULT / 'RUN_CONFIG.json').read_text())
    runs = []
    env = dict(os.environ)
    env.pop('PYTHONOPTIMIZE', None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    flags = ['-O'] if sys.flags.optimize else []
    with tempfile.TemporaryDirectory(prefix='general-four-verify-') as temp:
        root = Path(temp) / 'results'
        output = Path(temp) / 'output'
        output.mkdir()
        for item in manifest['files']:
            rel = safe_relative(item['path'])
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(HERE / rel, root / rel)
        verify_manifest(root, manifest)
        for job in config['jobs']:
            script = root / RESULT / safe_relative(job['script'])
            cwd = script.parent
            args = [a.replace('{output}', str(output)) for a in job.get('args', [])]
            result = subprocess.run([sys.executable, *flags, str(script), *args],
                                    cwd=cwd, env=env, capture_output=True, timeout=900)
            expected_exit = job.get('expected_exit', 0)
            require(result.returncode == expected_exit, 'checker failed: ' + job['name'] + '\n' +
                    result.stderr.decode('utf-8', errors='replace'))
            for marker in job.get('required_stdout', []):
                require(marker.encode() in result.stdout, 'missing result marker: ' + marker)
            for marker in job.get('required_stderr', []):
                require(marker.encode() in result.stderr, 'missing failure marker: ' + marker)
            if 'stdout_sha256' in job:
                require(digest(result.stdout) == job['stdout_sha256'],
                        'checker output changed: ' + job['name'])
            if 'combined_log_sha256' in job:
                require(digest(result.stdout + result.stderr) == job['combined_log_sha256'],
                        'checker log changed: ' + job['name'])
            files = []
            for expected in job.get('output_files', []):
                rel = safe_relative(expected['path'])
                data = (output / rel).read_bytes()
                require(digest(data) == expected['sha256'],
                        'regenerated output mismatch: ' + str(rel))
                files.append({'path': str(rel), 'sha256': digest(data), 'bytes': len(data)})
            for expected in job.get('local_generated_files', []):
                rel = safe_relative(expected['path'])
                path = cwd / rel
                require(str(path.relative_to(root)) not in
                        {item['path'] for item in manifest['files']},
                        'generated output overlaps a packaged source')
                data = path.read_bytes()
                require(digest(data) == expected['sha256'],
                        'regenerated audit output mismatch: ' + str(rel))
                files.append({'path': str(rel), 'sha256': digest(data), 'bytes': len(data)})
                path.unlink()
            runs.append({'name': job['name'], 'exit': result.returncode,
                         'expected_exit': expected_exit,
                         'stdout_sha256': digest(result.stdout),
                         'stdout_bytes': len(result.stdout), 'regenerated_files': files})
        # Packaging integrity controls are independent of the mathematical
        # negative controls run above and remain active with Python -O.
        proof = root / RESULT / 'PROOF.md'
        original = proof.read_bytes()
        proof.write_bytes(original + b'\nDeliberate negative control.\n')
        reject(lambda: verify_manifest(root, manifest), 'manifest size mismatch')
        proof.write_bytes(original)
        duplicate = dict(manifest, files=manifest['files'] + [manifest['files'][0]])
        reject(lambda: verify_manifest(root, duplicate), 'duplicate manifest path')
        unsafe = dict(manifest, files=[{'path': '../escape', 'bytes': 0, 'sha256': ''}])
        reject(lambda: verify_manifest(root, unsafe), 'unsafe manifest path')
        extra = root / RESULT / 'unexpected.txt'
        extra.write_text('Deliberate negative control.\n')
        reject(lambda: verify_manifest(root, manifest), 'unexpected or unlisted result source')
        extra.unlink()
        verify_manifest(root, manifest)
    verify_manifest(HERE, manifest)
    print(json.dumps({
        'status': 'PASS', 'proof_sha256': PROOF_SHA256,
        'scope': 'Distinct real offsets; arbitrary distinct nonnegative integer exponents; order four only.',
        'audit': 'Separate AI-assisted mathematical review and independent implementation.',
        'source_files_verified': len(manifest['files']),
        'clean_temporary_copy': True, 'generated_outputs_distributed': False,
        'packaging_negative_controls': ['altered proof', 'duplicate entry', 'unsafe path', 'unlisted file'],
        'jobs': runs,
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
