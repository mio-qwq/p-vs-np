#!/usr/bin/env python3
"""Reproduce this research release in clean temporary copies (standard library)."""
from hashlib import sha256
from pathlib import Path
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / 'manifest-20261018.json'


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(data):
    return sha256(data).hexdigest()


def verify_manifest(root, manifest):
    for item in manifest['files']:
        rel = Path(item['path'])
        require(not rel.is_absolute() and '..' not in rel.parts, 'unsafe manifest path')
        data = (root / rel).read_bytes()
        require(len(data) == item['bytes'], 'manifest size mismatch: ' + item['path'])
        require(digest(data) == item['sha256'], 'manifest hash mismatch: ' + item['path'])


def run(cwd, args, expected=0):
    env = dict(os.environ)
    env.pop('PYTHONOPTIMIZE', None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    # Optimization flags are supplied explicitly, never inherited from this process.
    command = [sys.executable, *args]
    result = subprocess.run(command, cwd=cwd, env=env, capture_output=True, timeout=120)
    require(result.returncode == expected,
            'unexpected exit for ' + ' '.join(args) + ': ' +
            result.stderr.decode('utf-8', errors='replace'))
    return result


def main():
    require(sys.version_info >= (3, 10), 'Python 3.10+ is required')
    manifest = json.loads(MANIFEST.read_text())
    verify_manifest(HERE, manifest)
    with tempfile.TemporaryDirectory(prefix='auxiliary-research-') as temp:
        copied = Path(temp) / 'results'
        shutil.copytree(HERE, copied, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', 'exact_certificate.json', 'audit_results.json'))
        verify_manifest(copied, manifest)
        fixed = copied / 'fixed-depth-hull-obstruction'
        monic = copied / 'monic-four-consecutive'
        fixed_output = run(fixed, ['check_depth_five.py']).stdout
        require(fixed_output == (fixed / 'certificate.json').read_bytes(),
                'fixed-depth certificate did not regenerate byte-identically')
        fixed_data = json.loads(fixed_output)
        independent = run(fixed, ['independent_check.py']).stdout
        require(independent == (fixed / 'independent_output.json').read_bytes(),
                'independent fixed-depth output did not regenerate byte-identically')
        independent_data = json.loads(independent)
        require(fixed_data['status'] == independent_data['status'] == 'PASS',
                'fixed-depth checker status')
        generated = json.loads((monic / 'GENERATED.json').read_text())['artifacts']
        require(not (monic / 'input/exact_certificate.json').exists(),
                'compact source unexpectedly includes the generated certificate')
        require(not (monic / 'audit_results.json').exists(),
                'compact source unexpectedly includes generated audit results')
        producer = run(monic, ['input/check_consecutive_four.py'])
        certificate = (monic / 'input/exact_certificate.json').read_bytes()
        expected_certificate = generated['input/exact_certificate.json']
        require(digest(certificate) == expected_certificate['sha256'] and
                len(certificate) == expected_certificate['bytes'],
                'generated monic certificate differs from its frozen expected bytes')
        normal = run(monic, ['audit_certificate.py'])
        expected_results = (monic / 'audit_results.json').read_bytes()
        expected_audit = generated['audit_results.json']
        require(digest(expected_results) == expected_audit['sha256'] and
                len(expected_results) == expected_audit['bytes'],
                'generated independent audit results differ from their expected bytes')
        optimized = run(monic, ['-O', 'audit_certificate.py'])
        require(normal.stdout == optimized.stdout,
                'normal and optimized monic output differ')
        require((monic / 'audit_results.json').read_bytes() == expected_results,
                'optimized monic audit results differ')
        audit = json.loads(expected_results)
        negatives = audit['negative_controls']
        require(len(negatives) == 10, 'incorrect negative-control count')
        require([v['outcome'] for v in negatives] == ['REJECTED'] * 8 + ['DISPROVED'] * 2,
                'negative controls did not all behave as expected')
        # Exercise the public CLI with a physically corrupt certificate.
        corrupt = json.loads(certificate)
        corrupt['certificates'][0]['coefficients_by_x_degree'][0][0][2] = '999'
        corrupt_path = monic / 'corrupt-coefficient.json'
        corrupt_path.write_text(json.dumps(corrupt) + '\n')
        bad = run(monic, ['audit_certificate.py', '--certificate', corrupt_path.name], expected=1)
        require(b'determinant coefficient mismatch' in bad.stderr,
                'corrupt CLI certificate was not rejected for its coefficient')
        # The pin on the publication-edited report must remain enforced.
        report_path = monic / 'input/REPORT.md'
        report = report_path.read_bytes()
        report_path.write_bytes(report + b'\ncorrupt provenance test\n')
        bad_hash = run(monic, ['audit_certificate.py'], expected=1)
        require(b'frozen input hash mismatch' in bad_hash.stderr,
                'altered frozen-input hash was not rejected')
        try:
            verify_manifest(copied, manifest)
        except RuntimeError as error:
            require('manifest ' in str(error), 'unexpected manifest negative-control failure')
        else:
            raise RuntimeError('manifest accepted a corrupted report')
        report_path.write_bytes(report)
        corrupt_path.unlink()
        verify_manifest(copied, manifest)
        summary = {
            'status': 'PASS',
            'arithmetic': 'Python standard-library exact integers and Fraction; no external dependencies',
            'clean_temporary_copy': True,
            'manifest_files_verified': len(manifest['files']),
            'fixed_depth': {
                'six_subsets_checked': fixed_data['six_subsets_checked'],
                'affine_functionals_checked': fixed_data['affine_functionals_checked'],
                'independent_six_subsets_checked': independent_data['six_subsets'],
                'general_orbit_parameter_sanity_checks': fixed_data['general_lemma_orbit_parameter_sanity_checks'],
                'certificate_byte_identical': True,
                'independent_output_byte_identical': True,
                'negative_controls': fixed_data['negative_controls'],
            },
            'monic_four': {
                'labeled_masks_checked': sum(audit['labeled_mask_counts'][k] for k in
                                             ('zero_row_masks', 'no_perfect_matching_nonzero_rows', 'with_perfect_matching')),
                'symbolic_certificates_checked': len(audit['witnesses']),
                'generated_certificate_matches_frozen_hash': True,
                'generated_audit_results_match_expected_hash': True,
                'generated_certificate_sha256': digest(certificate),
                'generated_audit_results_sha256': digest(expected_results),
                'large_json_outputs_excluded_from_clean_copy': True,
                'normal_optimized_output_byte_identical': True,
                'normal_stdout_sha256': digest(normal.stdout),
                'optimized_stdout_sha256': digest(optimized.stdout),
                'producer_stdout_sha256': digest(producer.stdout),
                'negative_controls': negatives,
                'physical_corrupt_certificate_exit': bad.returncode,
                'altered_report_hash_exit': bad_hash.returncode,
                'manifest_corruption_rejected': True,
            },
        }
    # Confirm originals did not change during the clean-copy runs.
    verify_manifest(HERE, manifest)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
