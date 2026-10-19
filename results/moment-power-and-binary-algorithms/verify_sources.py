#!/usr/bin/env python3
"""Verify all exact package bytes and optionally rerun canonical checkers."""
from pathlib import Path
import argparse, hashlib, json, os, subprocess, sys
HERE = Path(__file__).resolve().parent

def verify():
    manifest = json.loads((HERE / 'PACKAGE_MANIFEST.json').read_text())
    expected = {x['path'] for x in manifest['files']} | {'PACKAGE_MANIFEST.json', 'SHA256SUMS'}
    actual = {str(p.relative_to(HERE)) for p in HERE.rglob('*') if p.is_file()}
    if actual != expected:
        raise RuntimeError('Missing or unexpected files: ' + repr(actual ^ expected))
    for item in manifest['files']:
        data = (HERE / item['path']).read_bytes()
        if len(data) != item['bytes'] or hashlib.sha256(data).hexdigest() != item['sha256']:
            raise RuntimeError('Manifest byte mismatch: ' + item['path'])
    for line in (HERE / 'SHA256SUMS').read_text().splitlines():
        digest, relative = line.split('  ', 1)
        if hashlib.sha256((HERE / relative).read_bytes()).hexdigest() != digest:
            raise RuntimeError('Checksum mismatch: ' + relative)
    return manifest

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run-checks', action='store_true')
    args = parser.parse_args()
    manifest = verify()
    if args.run_checks:
        for relative in manifest['checkers']:
            path = HERE / relative
            for mode in ([], ['-O']):
                subprocess.run([sys.executable, *mode, str(path)], cwd=path.parent, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}, check=True)
        verify()
    print('PASS: exact package bytes' + (' and local normal/-O checker reruns' if args.run_checks else ''))

if __name__ == '__main__':
    main()
