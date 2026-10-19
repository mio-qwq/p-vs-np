#!/usr/bin/env python3
"""Verify source bytes; optionally rerun the eight audited local checkers."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import subprocess
import sys

HERE = Path(__file__).resolve().parent

def verify():
    manifest = json.loads((HERE / 'PACKAGE_MANIFEST.json').read_text())
    expected = {x['path'] for x in manifest['files']} | {'PACKAGE_MANIFEST.json', 'SHA256SUMS'}
    actual = {str(p.relative_to(HERE)) for p in HERE.rglob('*') if p.is_file()}
    if actual != expected:
        raise RuntimeError('Unexpected or missing files: ' + repr(actual ^ expected))
    for entry in manifest['files']:
        path = HERE / entry['path']
        data = path.read_bytes()
        if len(data) != entry['bytes'] or hashlib.sha256(data).hexdigest() != entry['sha256']:
            raise RuntimeError('Byte verification failed: ' + entry['path'])
    for line in (HERE / 'SHA256SUMS').read_text().splitlines():
        digest, name = line.split('  ', 1)
        if hashlib.sha256((HERE / name).read_bytes()).hexdigest() != digest:
            raise RuntimeError('Hash-list verification failed: ' + name)
    return manifest

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run-checks', action='store_true')
    args = parser.parse_args()
    manifest = verify()
    if args.run_checks:
        for relative in manifest.get('checkers', []):
            path = HERE / relative
            for mode in ([], ['-O']):
                subprocess.run([sys.executable, *mode, str(path)], cwd=path.parent,
                               env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}, check=True)
        verify()
    print('PASS: exact package bytes' + (' and local checker reruns' if args.run_checks else ''))

if __name__ == '__main__':
    main()
