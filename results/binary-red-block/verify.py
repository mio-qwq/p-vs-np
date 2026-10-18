#!/usr/bin/env python3
"""Verify exact certificates and a frozen inventory, using the standard library.

All checker output and deliberate corruption are confined to temporary copies.
No downloaded code, third-party dependencies, network access, or asserts.
"""
import copy
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent
BASE = '69bf4596e885277fd60a3d597faebbfc0ec945b6'
MODE = int(sys.flags.optimize)
PAYLOAD = (
    'PROVENANCE.json',
    'README.md',
    'RELEASE_NOTES.md',
    'all-red-block/AUDIT.md',
    'all-red-block/PROOF.md',
    'all-red-block/check-output.txt',
    'all-red-block/check.py',
    'all-red-block/results.json',
    'binary-fiber/AUDIT.md',
    'binary-fiber/REPORT.md',
    'binary-fiber/check-output.txt',
    'binary-fiber/check.py',
    'binary-fiber/results.json',
    'binary-fiber/root-crosscheck.json',
    'independent/PROOF.md',
    'independent/REVIEW.md',
    'independent/check.py',
    'independent/results.json',
    'verification.json',
    'verify.py',
)
ALL_FILES = set(PAYLOAD) | {'manifest.json', 'SHA256SUMS'}
CHECKER_SHA256 = {
    'all-red-block/check.py':'212031580e0fd58c234185484e68f680e4bb0bae422c2fba8d43439b1c3d1cc3',
    'binary-fiber/check.py':'5f1ae6ac4c1fe5b794a9ab7398a280dc4053abe39b0712534ed205c98cee729c',
    'independent/check.py':'93310f0cb8cc8bbbf0e4bfec709e4a5156d78b5a6f751a0380b41e4b53820bd6',
}

def require(condition, message):
    if not condition:
        raise ValueError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def read_json(path):
    def no_duplicates(pairs):
        value = {}
        for key, item in pairs:
            require(key not in value, 'Duplicate JSON key: '+key)
            value[key] = item
        return value
    def no_constant(value):
        raise ValueError('Non-finite JSON constant: '+value)
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=no_duplicates, parse_constant=no_constant)

def integrity(root):
    actual = set()
    allowed_dirs = {str(PurePosixPath(name).parent) for name in ALL_FILES} - {'.'}
    for item in root.rglob('*'):
        name = item.relative_to(root).as_posix()
        require(not item.is_symlink(), 'Symlink is not permitted: '+name)
        if item.is_dir():
            require(name in allowed_dirs, 'Unexpected directory: '+name)
        else:
            require(item.is_file(), 'Non-regular file: '+name)
            actual.add(name)
    require(actual == ALL_FILES, 'File inventory mismatch: missing='+str(sorted(ALL_FILES-actual))+', unexpected='+str(sorted(actual-ALL_FILES)))
    manifest = read_json(root/'manifest.json')
    require(manifest['schema'] == 'binary-red-block-manifest-v1', 'Manifest schema mismatch')
    require(manifest['algorithm'] == 'sha256', 'Manifest algorithm mismatch')
    require(manifest['expected_base_commit'] == BASE, 'Base commit mismatch')
    require([entry['path'] for entry in manifest['files']] == sorted(PAYLOAD), 'Manifest path list mismatch')
    for entry in manifest['files']:
        content = (root/entry['path']).read_bytes()
        require(len(content) == entry['bytes'], 'Size mismatch: '+entry['path'])
        require(sha(content) == entry['sha256'], 'Hash mismatch: '+entry['path'])
    expected_sums = ''.join(sha((root/name).read_bytes())+'  '+name+'\n' for name in sorted(set(PAYLOAD)|{'manifest.json'}))
    require((root/'SHA256SUMS').read_text(encoding='utf-8') == expected_sums, 'SHA256SUMS mismatch')
    for name, digest in CHECKER_SHA256.items():
        require(sha((root/name).read_bytes()) == digest, 'Original mathematical checker changed: '+name)
    provenance = read_json(root/'PROVENANCE.json')
    for record in provenance['files']:
        name = record['packaged_path']
        require(name in ALL_FILES, 'Unknown provenance path: '+name)
        data = (root/name).read_bytes()
        require(len(data) == record['packaged_bytes'] and sha(data) == record['packaged_sha256'], 'Provenance mismatch: '+name)
        if name in CHECKER_SHA256:
            require(record['byte_for_byte'] is True and record['source_sha256'] == sha(data), 'Checker provenance mismatch: '+name)
    for record in provenance['omitted_identical_outputs']:
        require(sha((root/record['identical_to_packaged']).read_bytes()) == record['sha256'], 'Deduplication provenance mismatch')
    return len(actual)

def internal_links(root):
    checked = 0
    for name in sorted(ALL_FILES):
        if not name.endswith('.md'):
            continue
        path = root/name
        prose = path.read_text(encoding='utf-8')
        prose = re.sub(r'\\\[.*?\\\]|\\\(.*?\\\)', '', prose, flags=re.S)
        prose = re.sub(r'`[^`]*`', '', prose)
        prose = re.sub(r'^(?: {4}|\t).*$', '', prose, flags=re.M)
        for target in re.findall(r'\[[^\]]*\]\(([^\s)]+)\)', prose):
            parts = urlsplit(target)
            if parts.scheme in ('http', 'https'):
                continue
            require(not parts.scheme and not parts.netloc and not parts.path.startswith('/'), 'Non-relative internal link: '+target)
            if parts.path:
                resolved = (path.parent/unquote(parts.path)).resolve()
                require(resolved.is_relative_to(root.resolve()), 'Link escapes package: '+target)
                require(resolved.is_file(), 'Broken internal link: '+name+' -> '+target)
                checked += 1
    return checked

def run(root, script, code=None, args=()):
    flags = ['-B'] + (['-'+'O'*MODE] if MODE else [])
    command = [sys.executable] + flags + (['-c',code] if code is not None else [str(root/script)]) + list(args)
    process = subprocess.run(command, cwd=str(root), env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0'), capture_output=True, timeout=300)
    require(process.returncode == 0, (script or 'cross-check')+' failed: '+process.stderr.decode('utf-8', errors='replace'))
    require(not process.stderr, (script or 'cross-check')+' emitted unexpected stderr')
    return process.stdout

def compare_certificate(recomputed, candidate, label):
    require(recomputed == candidate, label+' differs from exact fresh recomputation')

def check_mathematics(root):
    with tempfile.TemporaryDirectory(prefix='binary-red-block-math-') as directory:
        work = Path(directory)/'package'
        shutil.copytree(root, work)
        supplied_stdout = run(work, 'binary-fiber/check.py')
        require(supplied_stdout == (root/'binary-fiber/check-output.txt').read_bytes(), 'Supplied checker stdout differs')
        require((work/'binary-fiber/results.json').read_bytes() == (root/'binary-fiber/results.json').read_bytes(), 'Supplied certificate bytes differ')
        supplied = read_json(work/'binary-fiber/results.json')
        compare_certificate(supplied, read_json(root/'binary-fiber/results.json'), 'Supplied certificate')
        require(supplied['status'] == 'PASS' and len(supplied['cases']) == 5, 'Supplied example count/status differs')
        example = supplied['cases'][0]['targets'][1]
        require(example['even'] == 117 and example['odd'] == 117 and example['support_edges'] == 36, 'Interior example counts/support differ')
        require(example['degree'] == 12 and example['leading_coefficient'] == 6 and example['first_four_signed_coefficient_moments'] == [0,0,0,6], 'Interior example coefficient/moments differ')
        require(supplied['singular_boundary']['coefficients_low_to_high'] == [-24,-60,-38,-12,-2], 'Singular boundary differs')

        independent_stdout = run(work, 'independent/check.py')
        require(independent_stdout == (root/'independent/results.json').read_bytes(), 'Independent certificate bytes differ')
        independent = json.loads(independent_stdout)
        compare_certificate(independent, read_json(root/'independent/results.json'), 'Independent certificate')
        require(len(independent) == 5, 'Independent example count differs')

        # The source checker is unmodified. Its reusable raw-matrix routines are
        # loaded in a child interpreter under the current optimization mode.
        code = r'''
import contextlib, hashlib, io, json, runpy, sys
from pathlib import Path
root = Path(sys.argv[1])
with contextlib.redirect_stdout(io.StringIO()):
    ns = runpy.run_path(str(root/'binary-fiber/check.py'))
raw_source = (root/'independent/results.json').read_bytes()
cases = json.loads(raw_source)
summary = []
for case in cases:
    a, e = case['offsets'], case['exponents']
    red = {tuple(edge) for edge in case['red']}
    actual = ns['determinant'](ns['raw_matrix'](a,e,red))
    expected = {(t,q):v for t,p in enumerate(case['polynomials']) for q,v in enumerate(p) if v}
    if actual != expected:
        raise ValueError('Independent raw Laplace coefficient mismatch')
    summary.append({'n':len(a), 'red_edges':case['red'], 'degree':case['degree'], 'leading':case['leading'], 'all_coefficients_match':True})
print(json.dumps({'status':'PASS', 'method':'independent raw bivariate Laplace determinant compared coefficient-by-coefficient with root permutation-expansion outputs', 'source_sha256':hashlib.sha256(raw_source).hexdigest(), 'cases':summary}))
'''
        crosscheck = json.loads(run(work, None, code=code, args=(str(work),)))
        compare_certificate(crosscheck, read_json(root/'binary-fiber/root-crosscheck.json'), 'Raw-Laplace cross-check')
        require(crosscheck['status'] == 'PASS' and len(crosscheck['cases']) == 5, 'Cross-check case count/status differs')

        all_red_stdout = run(work, 'all-red-block/check.py', args=(str(work/'all-red-block/results.json'),))
        require(all_red_stdout == (root/'all-red-block/check-output.txt').read_bytes(), 'All-red checker stdout differs')
        require((work/'all-red-block/results.json').read_bytes() == (root/'all-red-block/results.json').read_bytes(), 'All-red certificate bytes differ')
        all_red = read_json(work/'all-red-block/results.json')
        compare_certificate(all_red, read_json(root/'all-red-block/results.json'), 'All-red certificate')
        require(all_red['checks'] == 'All exact checks passed' and all_red['case_count'] == 8 and all_red['target_count'] == 20, 'All-red case count/status differs')
        require(all_red['checker_sha256'] == CHECKER_SHA256['all-red-block/check.py'], 'All-red checker embedded hash differs')
        require(all_red['results'][0]['targets'][1]['coefficients_low_to_high'] == ['-24','-60','-38','-12','-2'], 'All-red boundary polynomial differs')

        # These controls bypass inventory/hashes and compare corrupted numerical
        # certificates with independently rerun arithmetic results.
        altered_supplied = copy.deepcopy(supplied)
        altered_supplied['cases'][0]['targets'][1]['coefficients_low_to_high'][12] += 1
        altered_independent = copy.deepcopy(independent)
        altered_independent[0]['polynomials'][1][12] += 1
        altered_all_red = copy.deepcopy(all_red)
        altered_all_red['results'][0]['targets'][1]['coefficients_low_to_high'][4] = '-1'
        rejected = []
        for label, fresh, altered in (('supplied_polynomial_coefficient', supplied, altered_supplied), ('independent_polynomial_coefficient', independent, altered_independent), ('all_red_polynomial_coefficient', all_red, altered_all_red)):
            altered_path = work/('altered-'+label+'.json')
            altered_path.write_text(json.dumps(altered), encoding='utf-8')
            rejected_one = False
            try:
                compare_certificate(fresh, read_json(altered_path), label)
            except ValueError as error:
                require('differs from exact fresh recomputation' in str(error), 'Unexpected certificate failure')
                rejected_one = True
            require(rejected_one, 'Altered mathematical certificate accepted: '+label)
            rejected.append(label)
        return {
            'all_red_block_checker':{'status':'PASS', 'theorem_examples':8, 'target_fibers':20, 'results_sha256':sha((root/'all-red-block/results.json').read_bytes())},
            'supplied_checker':{'status':'PASS', 'theorem_examples':5, 'singular_boundary_examples':1, 'results_sha256':sha((root/'binary-fiber/results.json').read_bytes())},
            'independent_checker':{'status':'PASS', 'theorem_examples':5, 'results_sha256':sha(independent_stdout)},
            'raw_laplace_crosscheck':{'status':'PASS', 'cases':5, 'all_coefficients_match':True},
            'interior_example':{'even':117, 'odd':117, 'support_edges':36, 'degree':12, 'leading_coefficient':6, 'first_four_signed_moments':[0,0,0,6]},
            'altered_mathematical_certificates_rejected':rejected,
            'certificate_controls_independent_of_hashes':True,
        }

def corruption_controls(root):
    controls = []
    for kind in ('modified_file', 'missing_file', 'unexpected_file', 'altered_manifest'):
        with tempfile.TemporaryDirectory(prefix='binary-red-block-corruption-') as directory:
            work = Path(directory)/'package'
            shutil.copytree(root, work)
            if kind == 'modified_file':
                target = work/'binary-fiber/REPORT.md'
                target.write_bytes(target.read_bytes()+b'corruption\n')
            elif kind == 'missing_file':
                (work/'binary-fiber/results.json').unlink()
            elif kind == 'unexpected_file':
                (work/'unlisted.txt').write_text('unexpected\n')
            else:
                target = work/'manifest.json'
                data = read_json(target)
                data['files'][0]['sha256'] = '0'*64
                target.write_text(json.dumps(data), encoding='utf-8')
            rejected = False
            try:
                integrity(work)
            except (ValueError, KeyError, OSError):
                rejected = True
            require(rejected, 'Corruption control was accepted: '+kind)
            controls.append(kind)
    return controls

def main():
    count = integrity(ROOT)
    links = internal_links(ROOT)
    mathematical = check_mathematics(ROOT)
    controls = corruption_controls(ROOT)
    integrity(ROOT)
    print(json.dumps({
        'status':'PASS', 'optimization':MODE, 'file_count':count,
        'integrity':'PASS', 'internal_relative_links_checked':links,
        'original_mathematical_checkers_unchanged':True,
        'clean_temporary_copy':True, 'source_files_unchanged':True,
        'mathematical_checks':mathematical,
        'rejected_packaging_corruptions':controls,
        'scope':'Sufficient nonsingular proper-block and all-red square-block theorems on complete bipartite graphs; finite exact corroboration, no general ASNC or P-versus-NP conclusion.',
    }, indent=2, sort_keys=True))

if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError, subprocess.SubprocessError) as error:
        print('FAIL: '+str(error), file=sys.stderr)
        sys.exit(1)
