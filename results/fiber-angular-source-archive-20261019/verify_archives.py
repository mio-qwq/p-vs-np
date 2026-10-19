#!/usr/bin/env python3
"""Hash-check, clean-extract and replay source archives in both Python modes."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,os,platform,subprocess,sys,tempfile,zipfile
ROOT=Path(__file__).resolve().parent

def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inventory(root):return {str(p.relative_to(root)):sha(p) for p in sorted(root.rglob('*')) if p.is_file()}
def integrity(root):
    entries={}
    for line in (root/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1);p=Path(name)
        require(not p.is_absolute() and '..' not in p.parts and name not in entries,'Unsafe or duplicate hash path')
        entries[name]=digest
    require(inventory(root)==dict(entries,SHA256SUMS=sha(root/'SHA256SUMS')),'Manifest file inventory or SHA256 mismatch')
    return len(entries)
def replay(record):
    archive=ROOT/record['archive'];require(sha(archive)==record['sha256'],'Archive hash mismatch')
    require(archive.stat().st_size==record['bytes'],'Archive size mismatch')
    with tempfile.TemporaryDirectory(prefix='fiber-angular-clean-') as td:
        dest=Path(td)
        with zipfile.ZipFile(archive) as z:
            entries=z.infolist();names=[i.filename for i in entries]
            require(z.testzip() is None,'Archive CRC error')
            require(len(names)==len(set(names))==record['payload_files'] and names==sorted(names),'ZIP count/order mismatch')
            for i in entries:
                p=Path(i.filename)
                require(not p.is_absolute() and '..' not in p.parts and p.parts[0]==archive.stem,'Unsafe ZIP path')
                require(i.date_time==(2026,10,19,0,0,0) and i.external_attr>>16==0o100644 and not i.extra,'Unexpected ZIP metadata')
            z.extractall(dest)
        root=dest/archive.stem;before=inventory(root);integrity(root)
        modes=[]
        env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0');env.pop('PYTHONOPTIMIZE',None)
        for optimized in (False,True):
            cmd=[sys.executable]+(['-O'] if optimized else [])+[record['entrypoint']]
            result=subprocess.run(cmd,cwd=root,env=env,capture_output=True,text=True)
            require(result.returncode==0 and not result.stderr,'Replay failed: '+archive.name+'\n'+result.stdout+result.stderr)
            report=json.loads(result.stdout)
            require(report.get('status') in ('PASS','all checks passed'),'Replay has no success result')
            modes.append({'optimized':optimized,'exit_code':result.returncode,'stdout_sha256':hashlib.sha256(result.stdout.encode()).hexdigest(),'report':report})
        require(inventory(root)==before,'Extracted payload changed during replay')
        return {'archive':archive.name,'sha256':record['sha256'],'bytes':record['bytes'],'payload_files':record['payload_files'],'clean_extraction':'PASS','source_tree_unchanged':True,'modes':modes}

def main():
    count=integrity(ROOT);manifest=json.loads((ROOT/'ARCHIVES.json').read_text());before=inventory(ROOT)
    with ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(replay,manifest['archives']))
    require(inventory(ROOT)==before,'Outer source archive directory changed')
    versions={'python':platform.python_version()}
    if manifest['repository'].endswith('p-vs-np'):
        versions['compiler']=subprocess.check_output(['g++','--version'],text=True).splitlines()[0]
    else:
        import sympy
        versions['sympy']=sympy.__version__
    print(json.dumps({'status':'PASS','repository':manifest['repository'],'parent_commit':manifest['parent_commit'],'outer_integrity_files':count,'versions':versions,'archives':results,'new_solver_runs':0,'source_trees_unchanged':True,'negative_controls':'Replayed by each included harness where applicable.','claim_boundary':'Exact regression and finite certificates complement written proofs; no Millennium-problem resolution or formal verification claim.'},indent=2,ensure_ascii=False))
if __name__=='__main__':main()
