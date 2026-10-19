#!/usr/bin/env python3
"""Recompute frozen exact certificates in isolated copies; never use the network."""
import argparse,copy,hashlib,json,os,re,shutil,subprocess,sys,tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent
G='general-omission-20261018'
E='single-edge-perturbation-20261019'
B='single-row-boundary-20261019'
SCRIPTS=[(G+'/checker/check_q3.py','All q=3 checks passed.'),
         (E+'/checker/check.py','PASS: 8 exact cases'),
         (E+'/checker/audit_check.py','PASS: 32'),
         (B+'/checker/check.py','PASS')]
SYMBOLIC=[(B+'/independent/audit_checker.py','All exact identities and reported examples passed.'),
          (B+'/independent/save_stress_certificate.py','be7a3c0c265e30ad70ca0bcaf93ce39a84704f08ea28ff710e92cb9906fd1b74')]
CERTIFICATES=[G+'/checker/q3_results.json',E+'/checker/results.json',B+'/checker/results.json']
STRESS=B+'/independent/residual_stress_test.json'
def require(ok,msg):
    if not ok:raise ValueError(msg)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def file_map(root):return {p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob('*') if p.is_file()}
def integrity(root):
    manifest=load(root/'manifest.json')
    records=manifest['files']
    expected={f['path'] for f in records}|{'manifest.json','SHA256SUMS'}
    require(len(records)==len({f['path'] for f in records}),'Duplicate manifest path')
    actual=file_map(root)
    require(set(actual)==expected,'Missing or unexpected package file')
    for f in records:
        name=f['path'];require(not Path(name).is_absolute() and '..' not in Path(name).parts,'Unsafe path')
        raw=actual[name];require(len(raw)==f['bytes'] and sha(raw)==f['sha256'],'File hash/size mismatch: '+name)
    sums={}
    for line in (root/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1);require(name not in sums,'Duplicate SHA256SUMS entry');sums[name]=digest
    require(set(sums)==expected-{'SHA256SUMS'},'Wrong SHA256SUMS inventory')
    for name,digest in sums.items():require(sha(actual[name])==digest,'SHA256SUMS mismatch: '+name)
    return len(actual)
def provenance(root):
    p=load(root/'PROVENANCE.json');scripts=0
    for f in p['files']:
        require(sha((root/f['destination']).read_bytes())==f['packaged_sha256'],'Packaged provenance mismatch')
        if f['byte_preserved']:require(f['source_sha256']==f['packaged_sha256'],'False byte-preservation claim')
        if f['destination'].endswith('.py'):
            require(f['byte_preserved'],'Original checker modified');scripts+=1
    require(scripts==6,'Expected six unchanged source checker scripts')
    require(not (root/E/'dependencies/general-rectangle-PROOF.md').exists(),'Duplicate dependency proof retained')
    require((root/G/'PROOF.md').is_file(),'Canonical rectangle proof missing')
    for name in ('PROOF.md','RESULT.md'):
        require('../'+G+'/PROOF.md' in (root/E/name).read_text(),'Canonical dependency reference missing')
    return scripts
def links(root):
    count=0
    for p in root.rglob('*.md'):
        # Source proofs use brackets in equations such as [s_theta](UW).
        # Verify actual file/URL anchors without treating those formulas as links.
        for value in re.findall(r'\]\(([^)\s]+)\)',p.read_text()):
            if '://' in value or value.startswith('#'):continue
            if '/' not in value and '.' not in value:continue
            target=(p.parent/value.split('#')[0]).resolve()
            require(target.is_relative_to(root.resolve()) and target.exists(),'Broken local link: '+str(p)+' -> '+value);count+=1
    return count
def invoke(root,name,marker,expected_failure=False):
    flags=['-B']+(['-O'] if sys.flags.optimize else [])+(['-S'] if sys.flags.no_site else [])
    proc=subprocess.run([sys.executable]+flags+[str(root/name)],cwd=root/name.split('/')[0],
                        capture_output=True,text=True,timeout=2400,
                        env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0'))
    if expected_failure:
        require(proc.returncode!=0 and marker in proc.stderr,'Deliberate mathematical corruption did not fail as expected: '+name)
    else:
        require(proc.returncode==0 and not proc.stderr and marker in proc.stdout,'Checker failed: '+name+'\n'+proc.stdout[-1000:]+'\n'+proc.stderr[-2000:])
    return proc.stdout
def compare_certificate(expected,actual):
    require(expected==actual,'Recomputed mathematical certificate differs')
def must_reject(fn,label):
    try:fn()
    except (ValueError,KeyError,FileNotFoundError):return
    raise ValueError('Negative control accepted: '+label)
def package_controls(root):
    controls=['changed_file','missing_file','unexpected_file','changed_manifest']
    for kind in controls:
        with tempfile.TemporaryDirectory(prefix='rectangle-inventory-negative-') as tmp:
            work=Path(tmp)/'package';shutil.copytree(root,work)
            if kind=='changed_file':
                p=work/G/'PROOF.md';p.write_bytes(p.read_bytes()+b'\ncorrupted\n')
            elif kind=='missing_file':(work/G/'PROOF.md').unlink()
            elif kind=='unexpected_file':(work/'unexpected.txt').write_text('unexpected')
            else:
                p=work/'manifest.json';d=load(p);d['files'][0]['sha256']='0'*64;p.write_text(json.dumps(d))
            must_reject(lambda:integrity(work),kind)
    return controls
def arithmetic_certificate_controls(root,recomputed,full):
    # These checks deliberately bypass inventory hashes and compare altered
    # mathematical values with the independently regenerated complete bytes.
    paths=CERTIFICATES+([STRESS] if full else [])
    for name in paths:
        d=load(root/name)
        if name.startswith(G):d['leading_coefficient']=str(int(d['leading_coefficient'])+1)
        elif name.startswith(E):d['cases'][0]['fiber_leading']['0']+=1
        elif name==STRESS:d['middle_coefficients_ascending'][0]=str(int(d['middle_coefficients_ascending'][0])+1)
        else:d['cases'][0]['v']=str(int(d['cases'][0]['v'])+1)
        corrupted=(json.dumps(d,indent=2)+'\n').encode()
        must_reject(lambda:compare_certificate(corrupted,recomputed[name]),name)
    return len(paths)
def source_controls(root,full):
    controls=[
      (G+'/checker/check_q3.py','sign = (-1)**(3*(12-3))','sign = -((-1)**(3*(12-3)))','Translated-minor coefficient disagrees'),
      (E+'/checker/check.py',"==ratio,'boundary ratio formula'","==-ratio,'boundary ratio formula'",'boundary ratio formula'),
      (B+'/checker/check.py','v=F(B2-F(B1*B1,m)-F(m*(m*m-1),12),m*(m*m-1))','v=F(B2-F(B1*B1,m)-F(m*(m*m-1),12),m*m-1)','cofactor second correction')]
    if full:controls.append((B+'/independent/audit_checker.py','/(m*(m*m-1))','/(m*m-1)','Exact check failed'))
    for name,old,new,marker in controls:
        with tempfile.TemporaryDirectory(prefix='rectangle-source-negative-') as tmp:
            work=Path(tmp)/'package';shutil.copytree(root,work)
            p=work/name;text=p.read_text();require(text.count(old)==1,'Ambiguous negative-control anchor: '+name)
            p.write_text(text.replace(old,new));invoke(work,name,marker,expected_failure=True)
    return len(controls)
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--full',action='store_true');args=parser.parse_args()
    before=file_map(ROOT);count=integrity(ROOT);original_scripts=provenance(ROOT);link_count=links(ROOT)
    version=None
    if args.full:
        try:import sympy
        except ImportError:raise SystemExit('Full mode requires SymPy. Install requirements.txt; default mode explicitly leaves the independent symbolic audit NOT_RUN.')
        version=sympy.__version__
    recomputed={};ran=[]
    with tempfile.TemporaryDirectory(prefix='rectangle-exact-rerun-') as tmp:
        work=Path(tmp)/'package';shutil.copytree(ROOT,work)
        for name,marker in SCRIPTS+(SYMBOLIC if args.full else []):invoke(work,name,marker);ran.append(name)
        for name in CERTIFICATES+([STRESS] if args.full else []):
            raw=(work/name).read_bytes();compare_certificate(before[name],raw);recomputed[name]=raw
    certificate_negative=arithmetic_certificate_controls(ROOT,recomputed,args.full)
    source_negative=source_controls(ROOT,args.full)
    package_negative=package_controls(ROOT)
    require(before==file_map(ROOT),'Frozen package changed during checks')
    result={'status':'PASS','verification_mode':'full' if args.full else 'standard_library',
      'python':sys.version.split()[0],'optimization':sys.flags.optimize,'sympy':version,
      'file_count':count,'integrity':'PASS','original_checker_count':original_scripts,
      'original_checkers_unchanged':True,'original_checkers_run':ran,
      'all_fresh_certificate_bytes_identical':True,'internal_relative_links_checked':link_count,
      'source_level_mathematical_corruptions_rejected':source_negative,
      'mathematical_certificate_corruptions_rejected':certificate_negative,
      'mathematical_controls_bypass_inventory_hashes':True,'packaging_corruptions_rejected':package_negative,
      'independent_symbolic_boundary_audit':'PASS' if args.full else 'NOT_RUN; requires --full and SymPy',
      'stress_certificate_reconstructed':'PASS' if args.full else 'NOT_RUN; requires --full and SymPy',
      'frozen_package_unchanged':True,
      'scope':'Structured separated-offset rectangles and single-entry extensions; one-row simultaneous resonance and arbitrary colorings remain unresolved.'}
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
