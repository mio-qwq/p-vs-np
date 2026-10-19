#!/usr/bin/env python3
"""Verify all exact theorem certificates in disposable copies, without network or dependencies."""
from pathlib import Path,PurePosixPath
import copy,hashlib,json,os,re,shutil,subprocess,sys,tempfile
from urllib.parse import unquote,urlsplit
ROOT=Path(__file__).resolve().parent
MODE=int(sys.flags.optimize)
PAYLOAD=('CHECKPOINT.md', 'PROOF.md', 'PROVENANCE.json', 'README.md', 'RELEASE_NOTES.md', 'STATUS.md', 'audit/AUDIT.md', 'audit/REPRODUCE.txt', 'audit/SOURCE_MANIFEST.json', 'audit/check_independent.py', 'audit/check_negative_controls.py', 'audit/check_qclosed.py', 'audit/independent-results.json', 'audit/negative-control-results.json', 'audit/qclosed-results.json', 'cancellation_result.json', 'check.py', 'check_cancellation.py', 'results.json', 'verification.json', 'verify.py')
CHECKER_SHA256={'check.py': '098529c33919f7a2b149f3d56d816dafebee6ec08716ee721f41f52c0f29f888', 'check_cancellation.py': 'e243e74bfa8197550699ec696938f30eaf34f0b48786643af79b6e4cc38ea94d', 'audit/check_independent.py': 'fdaa1372421d991aed6787750aca9d4b11faadeb1f3a15e02c6cbe1db042bc7f', 'audit/check_qclosed.py': '5373c63e31d35946b55d4c8181b2dcd5527c1e8ea3b289d90cdeb286fa082da2', 'audit/check_negative_controls.py': '9694c26cacf55d656ad4b7dd6ea94a5d9dd4ee57595fba4aff89001699e7c971'}
PROOF_SHA256='f796d745708ca05d4f69e3c55949cc053ab8b6c8561dc07cc090c5838556183f'
ALL_FILES=set(PAYLOAD)|{'manifest.json','SHA256SUMS'}

def require(ok,message):
    if not ok:raise ValueError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def read_json(path):
    def unique(pairs):
        out={}
        for key,value in pairs:
            require(key not in out,'Duplicate JSON key: '+key)
            out[key]=value
        return out
    def finite(value):raise ValueError('Nonfinite JSON value: '+value)
    return json.loads(path.read_text(encoding='utf-8'),object_pairs_hook=unique,parse_constant=finite)

def integrity(root):
    actual=set();allowed_dirs={str(PurePosixPath(p).parent) for p in ALL_FILES}-{'.'}
    for path in root.rglob('*'):
        rel=path.relative_to(root).as_posix()
        require(not path.is_symlink(),'Symlink not permitted: '+rel)
        if path.is_dir():require(rel in allowed_dirs,'Unexpected directory: '+rel)
        else:
            require(path.is_file(),'Nonregular file: '+rel)
            actual.add(rel)
    require(actual==ALL_FILES,'File inventory mismatch: missing='+str(sorted(ALL_FILES-actual))+', unexpected='+str(sorted(actual-ALL_FILES)))
    manifest=read_json(root/'manifest.json')
    require(manifest['schema']=='rectangular-moment-manifest-v1' and manifest['algorithm']=='sha256','Manifest schema/algorithm mismatch')
    require([e['path'] for e in manifest['files']]==sorted(PAYLOAD),'Manifest fixed inventory mismatch')
    for entry in manifest['files']:
        raw=(root/entry['path']).read_bytes()
        require(len(raw)==entry['bytes'] and sha(raw)==entry['sha256'],'File size/hash mismatch: '+entry['path'])
    expected=''.join(sha((root/name).read_bytes())+'  '+name+'\n' for name in sorted(set(PAYLOAD)|{'manifest.json'}))
    require((root/'SHA256SUMS').read_text()==expected,'SHA256SUMS mismatch')
    require(sha((root/'PROOF.md').read_bytes())==PROOF_SHA256,'Audited proof changed')
    for name,digest in CHECKER_SHA256.items():
        require(sha((root/name).read_bytes())==digest,'Original checker changed: '+name)
    provenance=read_json(root/'PROVENANCE.json')
    require(provenance['source_freeze_confirmed'] is True and provenance['remote_writes'] is False,'Provenance status mismatch')
    require(provenance['source_freeze_manifest']['all_entries_verified'] is True and provenance['audit_freeze_manifest']['all_entries_verified'] is True,'Source freeze not verified')
    records={e['packaged_path']:e for e in provenance['files']}
    require(len(records)==len(provenance['files']),'Duplicate provenance entries')
    for name,entry in records.items():
        require(name in ALL_FILES,'Unknown provenance path: '+name)
        raw=(root/name).read_bytes()
        require(len(raw)==entry['packaged_bytes'] and sha(raw)==entry['packaged_sha256'],'Provenance hash mismatch: '+name)
        if entry['byte_for_byte']:
            require(entry['source_sha256']==sha(raw) and entry['source_bytes']==len(raw),'Source byte preservation mismatch: '+name)
        if name in CHECKER_SHA256 or name=='PROOF.md':
            require(entry['byte_for_byte'] is True,'Frozen proof/checker changed: '+name)
    audit=read_json(root/'audit/SOURCE_MANIFEST.json')
    require(audit['audited_proof_sha256']==PROOF_SHA256,'Audit proof hash mismatch')
    require(audit['full_polynomial_cases']==15 and audit['affine_q_cases']==90 and audit['negative_controls']==2 and audit['normal_optimized_agree'] is True,'Audit scope mismatch')
    for name,digest in audit['files'].items():
        packaged='audit/'+name
        if packaged in records:require(records[packaged]['source_sha256']==digest,'Audit original-source hash mismatch: '+name)
    return len(actual)

def internal_links(root):
    count=0
    for name in sorted(ALL_FILES):
        if not name.endswith('.md'):continue
        prose=(root/name).read_text()
        prose=re.sub(r'`[^`]*`','',prose)
        prose=re.sub(r'^(?: {4}|\t).*$', '', prose, flags=re.M)
        for target in re.findall(r'\[[^\]]*\]\(([^\s)]+)\)',prose):
            parts=urlsplit(target)
            if parts.scheme in ('http','https'):continue
            require(not parts.scheme and not parts.netloc and not parts.path.startswith('/'),'Nonrelative link: '+target)
            if parts.path:
                resolved=((root/name).parent/unquote(parts.path)).resolve()
                require(resolved.is_relative_to(root.resolve()) and resolved.is_file(),'Broken or escaping link: '+name+' -> '+target)
                count+=1
    return count

def compare(actual,expected,label):
    require(actual==expected,label+' differs from exact fresh recomputation')
def reject_math(actual,wrong,label):
    try:compare(actual,wrong,label)
    except ValueError as error:
        require('differs from exact fresh recomputation' in str(error),'Unexpected rejection reason')
        return label
    raise ValueError('Changed mathematical certificate accepted: '+label)
def run(root,script):
    command=[sys.executable,'-S','-B']+(['-'+'O'*MODE] if MODE else [])+[str(root/script)]
    result=subprocess.run(command,cwd=(root/script).parent,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0'),timeout=1800)
    require(result.returncode==0 and not result.stderr,script+' failed: '+result.stderr.decode(errors='replace'))
    return result

def mathematics(root):
    jobs=[('check.py','results.json'),('check_cancellation.py','cancellation_result.json'),('audit/check_independent.py','audit/independent-results.json'),('audit/check_qclosed.py','audit/qclosed-results.json'),('audit/check_negative_controls.py','audit/negative-control-results.json')]
    fresh={};controls=[]
    with tempfile.TemporaryDirectory(prefix='rectangular-moment-math-') as directory:
        work=Path(directory)/'package';shutil.copytree(root,work)
        for script,receipt in jobs:
            result=run(work,script)
            expected=read_json(root/receipt);actual=read_json(work/receipt)
            compare(actual,expected,receipt)
            require((work/receipt).read_bytes()==(root/receipt).read_bytes(),'Fresh certificate bytes differ: '+receipt)
            fresh[receipt]=actual
            if script.endswith('check_negative_controls.py'):
                require(b'two deliberately wrong normalizations were rejected' in result.stdout,'Source negative controls did not run')
        producer=fresh['results.json'];full=fresh['audit/independent-results.json'];closed=fresh['audit/qclosed-results.json'];negative=fresh['audit/negative-control-results.json'];cancel=fresh['cancellation_result.json']
        require(len(producer)==7 and len(full)==15 and len(closed)==90,'Exact case count mismatch')
        require(len(negative)==2 and all(v['caught'] is True for v in negative),'Source negative-control failure')
        require(cancel['D']==11 and cancel['degree']==7 and cancel['leading']=='32040 sqrt(2) (z-1)^2','Irrational cancellation outcome mismatch')
        by_name={v['name']:v for v in full}
        expected_examples={'r3_k3_standard':(3,15,13,'-37324800'),'r3_k4_ideal':(4,51,48,'118970202193920'),'r4_k5_ideal':(5,69,65,'20071103433434726400000')}
        for name,(k,D,degree,scalar) in expected_examples.items():
            case=by_name[name]
            require((case['k'],case['D'],case['actual_degree'],case['predicted_scalar'])==(k,D,degree,scalar),'Milestone example mismatch: '+name)
            require(case['leading_w_coefficients']==[0]*(len(case['I']))+[int(scalar)],'Leading w coefficient mismatch: '+name)
        for name in ['r2_k3_integer_qzero','r2_k3_integer_qzero_shifted']:
            case=by_name[name]
            require(case['q']=='0' and case['predicted_degree']==9 and case['actual_degree']==7 and case['leading_w_coefficients']==[0,0,37645207142400],'Integer cancellation mismatch: '+name)
        pairs=[('n8 first two moments equal','r3_k3_standard'),('n6 gapped first two moments equal','r2_k3_ideal'),('n8 gapped first three moments equal','r3_k4_ideal'),('n10 first four moments equal','r4_k5_ideal')]
        for a,b in pairs:
            lhs=next(v for v in producer if v['name']==a);rhs=by_name[b]
            compare((lhs['first_differing_moment'],lhs['D'],lhs['degree'],lhs['q'],lhs['coefficient']),(rhs['k'],rhs['D'],rhs['actual_degree'],rhs['q'],rhs['predicted_scalar']),'Independent overlap '+a)
        # These altered numerical certificates are passed directly to mathematical
        # comparison, without invoking hashes or inventory validation.
        wrong=copy.deepcopy(producer);wrong[0]['coefficient']=str(int(wrong[0]['coefficient'])+1)
        controls.append(reject_math(producer,wrong,'producer candidate coefficient'))
        wrong=copy.deepcopy(full);wrong[0]['nonzero_lambda_coefficients'][str(wrong[0]['actual_degree'])][1]+=1
        controls.append(reject_math(full,wrong,'independent full-polynomial coefficient'))
        wrong=copy.deepcopy(closed);wrong[-1]['q'][-1]='0'
        controls.append(reject_math(closed,wrong,'affine closed-form coefficient'))
        wrong=copy.deepcopy(cancel);wrong['complete_coefficients']['7'][0]='32041 sqrt(2)'
        controls.append(reject_math(cancel,wrong,'irrational cancellation coefficient'))
    return {'producer_cases':7,'irrational_full_permutation_count':720,'independent_complete_bivariate_cases':15,'affine_closed_form_families':90,'independent_algorithm_overlap_cases':4,'source_level_negative_controls_rejected':[v['control'] for v in negative],'mathematical_certificates_rejected':controls,'mathematical_negative_controls_independent_of_inventory_hashes':True,'all_original_checkers_rerun':True,'all_fresh_certificate_bytes_match':True,'all_subprocesses_exclude_site_packages':True,'highest_first_differing_moment_in_full_reconstruction':5,'integer_qzero_actual_degree':7,'standard_n8_actual_degree':13,'standard_n10_k5_actual_degree':65}

def corruption_controls(root):
    caught=[]
    for kind in ['modified_file','missing_file','unexpected_file','altered_manifest']:
        with tempfile.TemporaryDirectory(prefix='rectangular-moment-corruption-') as directory:
            work=Path(directory)/'package';shutil.copytree(root,work)
            if kind=='modified_file':
                p=work/'README.md';p.write_bytes(p.read_bytes()+b'changed\n')
            elif kind=='missing_file':(work/'cancellation_result.json').unlink()
            elif kind=='unexpected_file':(work/'unlisted.txt').write_text('unexpected\n')
            else:
                p=work/'manifest.json';data=read_json(p);data['files'][0]['sha256']='0'*64;p.write_text(json.dumps(data))
            try:integrity(work)
            except (ValueError,KeyError,OSError):caught.append(kind)
            else:raise ValueError('Corruption incorrectly accepted: '+kind)
    return caught

def main():
    require(sys.version_info>=(3,10),'Python 3.10 or later required')
    require(len(sys.argv)==1,'No optional modes; this verifier always reruns every included checker')
    count=integrity(ROOT);links=internal_links(ROOT);math=mathematics(ROOT);controls=corruption_controls(ROOT);integrity(ROOT)
    print(json.dumps({'status':'PASS','optimization':MODE,'python':sys.version.split()[0],'file_count':count,'integrity':'PASS','audited_proof_sha256':PROOF_SHA256,'original_checker_count':len(CHECKER_SHA256),'original_checkers_unchanged':True,'frozen_package_unchanged':True,'internal_relative_links_checked':links,'mathematical_checks':math,'packaging_corruptions_rejected':controls,'scope':'First-differing-moment theorem for one structured rectangular family. Arbitrary colorings, general ASNC, and P versus NP remain unresolved.'},indent=2,sort_keys=True))
if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,TypeError,OSError,subprocess.SubprocessError) as error:
        print('FAIL: '+str(error),file=sys.stderr);sys.exit(1)
