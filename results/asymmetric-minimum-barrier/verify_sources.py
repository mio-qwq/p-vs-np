#!/usr/bin/env python3
"""Verify archive bytes, then replay all checkers without optimization gaps."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def verify():
    manifest = json.loads((HERE / 'PACKAGE_MANIFEST.json').read_text())
    entries = manifest['files']
    names = [entry['path'] for entry in entries]
    require(len(names) == len(set(names)), 'Duplicate manifest paths')
    expected = set(names) | {'PACKAGE_MANIFEST.json', 'SHA256SUMS'}
    actual = set()
    for path in HERE.rglob('*'):
        require(not path.is_symlink(), 'Symlinks are not permitted')
        if path.is_file():
            actual.add(path.relative_to(HERE).as_posix())
    require(actual == expected, 'File-set mismatch: ' + repr(actual ^ expected))
    for entry in entries:
        relative = Path(entry['path'])
        require(not relative.is_absolute() and '..' not in relative.parts, 'Unsafe manifest path')
        data = (HERE / relative).read_bytes()
        require(len(data) == entry['bytes'], 'Byte count mismatch: ' + entry['path'])
        require(sha(data) == entry['sha256'], 'Digest mismatch: ' + entry['path'])
    covered = []
    for line in (HERE / 'SHA256SUMS').read_text().splitlines():
        digest, name = line.split('  ', 1)
        require(name in expected - {'SHA256SUMS'}, 'Unexpected checksum path')
        require(sha((HERE / name).read_bytes()) == digest, 'Checksum mismatch: ' + name)
        covered.append(name)
    require(len(covered) == len(set(covered)), 'Duplicate checksum paths')
    require(set(covered) == expected - {'SHA256SUMS'}, 'Incomplete checksum coverage')
    return manifest

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run-checks', action='store_true')
    args = parser.parse_args()
    manifest = verify()
    if args.run_checks:
        for checker in manifest['checkers']:
            require(checker['path'] in {entry['path'] for entry in manifest['files']}, 'Unlisted checker')
            path = HERE / checker['path']
            for mode, flags in [('normal', []), ('optimized', ['-O'])]:
                run = subprocess.run([sys.executable, '-B', *flags, str(path)], cwd=path.parent,
                    env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}, capture_output=True, check=True)
                require(run.stderr == b'', 'Unexpected checker stderr')
                require(sha(run.stdout) == checker['stdout_sha256'], 'Checker stdout mismatch: ' + checker['path'])
                verify()
                print('PASS:', checker['path'], mode)
    print('PASS: complete file set, byte lengths, SHA-256 coverage' + (' and normal/-O checker replay' if args.run_checks else ''))

if __name__ == '__main__':
    main()
