"""Portable independent audit; intentionally corrupted C6 must fail with and without -O."""
import subprocess,sys,json,hashlib,os
from pathlib import Path
HERE=Path(__file__).resolve().parent
runs=[]
def run(name,script,optimized=False,negative=False):
 args=[sys.executable]+(['-O'] if optimized else [])+[str(HERE/script)]+(['--negative-control'] if negative else [])
 proc=subprocess.run(args,cwd=HERE,text=True,capture_output=True)
 log=proc.stdout+proc.stderr
 (HERE/(name+'.log')).write_text(log)
 expected=1 if negative else 0
 passed=(proc.returncode==expected)
 if negative:passed=passed and 'Identity failed: 771515 C6; residual=-1' in log
 record={'name':name,'command':['python']+(['-O'] if optimized else [])+[script]+(['--negative-control'] if negative else []),'exit_code':proc.returncode,'expected_exit_code':expected,'passed':passed,'log_sha256':hashlib.sha256(log.encode()).hexdigest()}
 runs.append(record)
 print(('PASS' if passed else 'FAIL'),name,'exit',proc.returncode,flush=True)
 if not passed:raise RuntimeError(record)
for opt,label in [(False,'normal'),(True,'optimized')]:
 for script in ['enumerate_orbits.py','audit_identities.py','audit_dependencies.py']:
  run(label+'_'+Path(script).stem,script,opt)
 run(label+'_negative_control','audit_identities.py',opt,True)
counts={name:len(json.loads((HERE/name).read_text())['passed']) for name in ['identity_checks.json','dependency_checks.json']}
report={'status':'PASS','independent_symbolic_identity_count':sum(counts.values()),'check_counts':counts,'runs':runs}
(HERE/'verification_runs.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':'PASS','checks':counts},indent=2))
