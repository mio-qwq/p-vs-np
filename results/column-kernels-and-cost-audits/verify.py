#!/usr/bin/env python3
"""Offline source-bundle verification. Every mathematical run uses a temporary copy."""
import argparse, hashlib, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parent

def require(ok, message):
    if not ok:
        raise ValueError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def load(path):
    return json.loads(path.read_text(encoding='utf-8'))

def files(root):
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob('*') if p.is_file()}

def integrity(root):
    actual = files(root)
    records = load(root/'manifest.json')['files']
    names = [x['path'] for x in records]
    require(len(names) == len(set(names)), 'Duplicate manifest path')
    require(set(actual) == set(names) | {'manifest.json','SHA256SUMS'}, 'Missing or unexpected package file')
    for rec in records:
        name = rec['path']
        require(not Path(name).is_absolute() and '..' not in Path(name).parts, 'Unsafe inventory path')
        data = actual[name]
        require(len(data) == rec['bytes'] and sha(data) == rec['sha256'], 'Hash/size mismatch: '+name)
    sums = {}
    for line in actual['SHA256SUMS'].decode().splitlines():
        digest, name = line.split('  ', 1)
        require(name not in sums, 'Duplicate SHA256SUMS path')
        sums[name] = digest
    require(set(sums) == set(actual) - {'SHA256SUMS'}, 'SHA256SUMS inventory mismatch')
    for name, digest in sums.items():
        require(sha(actual[name]) == digest, 'SHA256SUMS mismatch: '+name)
    for rec in load(root/'PROVENANCE.json')['files']:
        require(sha(actual[rec['destination']]) == rec['packaged_sha256'], 'Provenance mismatch')
        if rec['byte_preserved']:
            require(rec['source_sha256'] == rec['packaged_sha256'], 'False byte-preservation statement')
    return len(actual)

def reject(call, label):
    try:
        call()
    except (ValueError, KeyError, FileNotFoundError):
        return
    raise ValueError('Negative control was accepted: '+label)

def package_controls(root):
    first = load(root/'manifest.json')['files'][0]['path']
    for label in ('changed_bytes','missing_file','extra_file','changed_manifest'):
        with tempfile.TemporaryDirectory(prefix='research-negative-') as tmp:
            work = Path(tmp)/'package'
            shutil.copytree(root, work)
            if label == 'changed_bytes':
                p = work/first
                p.write_bytes(p.read_bytes()+b'corruption\n')
            elif label == 'missing_file':
                (work/first).unlink()
            elif label == 'extra_file':
                (work/'unexpected').write_text('corruption')
            else:
                m = load(work/'manifest.json')
                m['files'][0]['sha256'] = '0'*64
                (work/'manifest.json').write_text(json.dumps(m))
            reject(lambda: integrity(work), label)
    return 4

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--full', action='store_true', help='Also run symbolic checkers; requires SymPy.')
    parser.add_argument('--exhaustive', action='store_true', help='Also compile/run the finite K5 supplement, when present; requires g++.')
    parser.add_argument('--upstream-dir', type=Path, help='Optional offline directory containing sources at receipt upstream_path or basename; validate external source hashes.')
    args = parser.parse_args()
    before = files(ROOT)
    count = integrity(ROOT)
    config = load(ROOT/'verification.json')
    version = None
    if args.full and any(c.get('sympy') for c in config['checkers']):
        try:
            import sympy
        except ImportError:
            raise SystemExit('Full mode requires SymPy; install requirements.txt. Default mode records symbolic checks as NOT_RUN.')
        version = sympy.__version__
    runs = []
    skipped = []
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0')
    environment.pop('PYTHONOPTIMIZE', None)  # assert-based originals must really run normally
    with tempfile.TemporaryDirectory(prefix='research-exact-') as tmp:
        work = Path(tmp)/'package'
        shutil.copytree(ROOT, work)
        for check in config['checkers']:
            if check.get('sympy') and not args.full:
                skipped.append({'path':check['path'],'status':'NOT_RUN','reason':'requires --full and SymPy'})
                continue
            optimized = bool(sys.flags.optimize) and not check.get('requires_normal_python', False)
            command = [sys.executable, '-B']+(['-O'] if optimized else [])+(['-S'] if sys.flags.no_site else [])+[str(work/check['path'])]
            proc = subprocess.run(command, cwd=(work/check['path']).parent, capture_output=True, text=True, timeout=2400, env=environment)
            require(proc.returncode == 0, 'Checker failed: '+check['path']+'\n'+proc.stdout[-1500:]+'\n'+proc.stderr[-1500:])
            if check.get('stdout_json'):
                actual = json.loads(proc.stdout)
                expected = load(work/check['stdout_json'])
                require(actual == expected, 'Recomputed stdout certificate differs: '+check['path'])
            for cert in check.get('certificates', []):
                actual = (work/cert).read_bytes()
                require(actual == before[cert], 'Recomputed certificate bytes differ: '+cert)
                reject(lambda: require(actual+b'CORRUPTED' == before[cert], 'certificate mismatch'), cert)
            if check.get('stdout_marker'):
                require(check['stdout_marker'] in proc.stdout, 'Missing completion marker: '+check['path'])
            runs.append({'path':check['path'],'status':'PASS','python_optimization':1 if optimized else 0,'requires_normal_python':check.get('requires_normal_python',False),'stdout_sha256':sha(proc.stdout.encode())})
        if config.get('exhaustive'):
            c = config['exhaustive']
            if args.exhaustive:
                compiler = shutil.which('g++')
                require(compiler is not None, '--exhaustive requires g++; no software is installed automatically')
                binary = Path(tmp)/'finite-k5-check'
                compiled = subprocess.run([compiler,'-std=c++17','-O2',str(work/c['source']),'-o',str(binary)],capture_output=True,text=True,timeout=180)
                require(compiled.returncode == 0, 'Compilation failed: '+compiled.stderr)
                proc = subprocess.run([str(binary)],capture_output=True,text=True,timeout=2400)
                require(proc.returncode == 0 and proc.stdout.encode() == before[c['stdout']], 'Finite K5 certificate differs: '+proc.stdout)
                runs.append({'path':c['source'],'status':'PASS','scope':'finite canonical K5 only','stdout_sha256':sha(proc.stdout.encode())})
            else:
                skipped.append({'path':c['source'],'status':'NOT_RUN','reason':'finite historical supplement; use --exhaustive for a fresh run'})
    source_controls = []
    for control in config.get('source_negative_controls', []):
        if control.get('sympy') and not args.full:
            continue
        with tempfile.TemporaryDirectory(prefix='research-math-negative-') as tmp:
            work = Path(tmp)/'package'
            shutil.copytree(ROOT, work)
            target = work/control['path']
            text = target.read_text()
            require(text.count(control['old']) == 1, 'Ambiguous mathematical negative control')
            target.write_text(text.replace(control['old'], control['new']))
            optimized = bool(sys.flags.optimize) and not control.get('requires_normal_python', False)
            command = [sys.executable, '-B']+(['-O'] if optimized else [])+(['-S'] if sys.flags.no_site else [])+[str(target)]
            proc = subprocess.run(command, cwd=target.parent, capture_output=True, text=True, timeout=2400, env=environment)
            require(proc.returncode != 0 and control['error_marker'] in proc.stderr, 'Wrong mathematical control accepted: '+control['path'])
            source_controls.append(control['path'])
    source_count = 0
    if args.upstream_dir:
        receipt = load(ROOT/'UPSTREAM_SOURCES.json')
        for rec in receipt['sources']:
            path = args.upstream_dir/rec['upstream_path']
            if not path.exists():
                path = args.upstream_dir/Path(rec['upstream_path']).name
            data = path.read_bytes()
            require(len(data) == rec['bytes'] and sha(data) == rec['sha256'], 'External source mismatch: '+str(path))
            if rec.get('git_blob_sha'):
                require(hashlib.sha1(('blob '+str(len(data))+'\0').encode()+data).hexdigest() == rec['git_blob_sha'], 'External Git blob mismatch')
            source_count += 1
    controls = package_controls(ROOT)
    require(before == files(ROOT), 'Frozen package changed during verification')
    result = {'status':'PASS','python':sys.version.split()[0],'aggregate_optimization':sys.flags.optimize,'sympy':version,'file_count':count,'integrity':'PASS','runs':runs,'not_run':skipped+config.get('historical_only',[]),'packaging_negative_controls':controls,'mathematical_source_corruptions_rejected':source_controls,'certificate_corruption_controls':'PASS for each regenerated certificate','upstream_sources_rehashed':source_count,'frozen_package_unchanged':True,'scope':config['scope']}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__ == '__main__':
    main()
