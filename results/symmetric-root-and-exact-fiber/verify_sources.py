#!/usr/bin/env python3
"""Verify exact package bytes and optionally rerun all canonical checkers."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import subprocess
import sys

HERE = Path(__file__).resolve().parent

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def verify():
    manifest = json.loads((HERE / 'PACKAGE_MANIFEST.json').read_text())
    names = [item['path'] for item in manifest['files']]
    require(len(names) == len(set(names)), 'Duplicate manifest path')
    expected = set(names) | {'PACKAGE_MANIFEST.json', 'SHA256SUMS'}
    actual = set()
    for path in HERE.rglob('*'):
        require(not path.is_symlink(), 'Symlink not allowed: ' + str(path))
        if path.is_file():
            actual.add(path.relative_to(HERE).as_posix())
    require(actual == expected, 'Missing or unexpected files: ' + repr(actual ^ expected))
    for item in manifest['files']:
        relative = Path(item['path'])
        require(not relative.is_absolute() and '..' not in relative.parts, 'Unsafe manifest path')
        data = (HERE / relative).read_bytes()
        require(len(data) == item['bytes'], 'Byte count mismatch: ' + item['path'])
        require(hashlib.sha256(data).hexdigest() == item['sha256'], 'Manifest hash mismatch: ' + item['path'])
    covered = []
    for line in (HERE / 'SHA256SUMS').read_text().splitlines():
        digest, relative = line.split('  ', 1)
        require(relative in expected - {'SHA256SUMS'}, 'Unexpected checksum path: ' + relative)
        require(hashlib.sha256((HERE / relative).read_bytes()).hexdigest() == digest, 'Checksum mismatch: ' + relative)
        covered.append(relative)
    require(len(covered) == len(set(covered)) and set(covered) == expected - {'SHA256SUMS'}, 'Incomplete or duplicate checksum coverage')
    return manifest

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run-checks', action='store_true')
    args = parser.parse_args()
    manifest = verify()
    if args.run_checks:
        for relative in manifest['checkers']:
            require(relative in {item['path'] for item in manifest['files']}, 'Unlisted checker')
            path = HERE / relative
            for flags in ([], ['-O']):
                subprocess.run([sys.executable, '-B', *flags, str(path)], cwd=path.parent, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}, check=True)
                verify()
    print('PASS: exact package bytes' + (' and local normal/-O checker reruns' if args.run_checks else ''))

if __name__ == '__main__':
    main()
