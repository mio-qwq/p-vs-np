#!/usr/bin/env python3
"""Frozen five-row subclass package: exact certificate checks, optional full SymPy reconstruction.
All writes and negative controls are confined to temporary copies.
"""
import argparse, ast, copy, hashlib, json, math, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path, PurePosixPath
from fractions import Fraction
from urllib.parse import unquote, urlsplit
ROOT = Path(__file__).resolve().parent
BASE = '5036ebd403ec3497b9df0ca44ea8570f5d9b0c6e'
MODE = int(sys.flags.optimize)
PAYLOAD = ('PROVENANCE.json', 'README.md', 'RELEASE_NOTES.md', 'STATUS.md', 'five-row-c12-20261018/PROOF.md', 'five-row-c12-20261018/RESULT.md', 'five-row-c12-20261018/coefficients.json', 'five-row-c12-20261018/verification.json', 'five-row-c12-20261018/verify.py', 'five-row-c12-audit-20261018/AUDIT.md', 'five-row-c12-audit-20261018/audit_c12.py', 'five-row-c12-audit-20261018/audit_complement.py', 'five-row-c12-audit-20261018/audit_final_tables.py', 'five-row-c12-audit-20261018/audit_receipt.json', 'five-row-c12-audit-20261018/audit_reduction.py', 'five-row-c12-audit-20261018/complement_receipt.json', 'five-row-c12-audit-20261018/final_table_receipt.json', 'five-row-c12-audit-20261018/reduction_receipt.json', 'five-row-cancellation-20261018/AUDIT.md', 'five-row-cancellation-20261018/PROOF.md', 'five-row-cancellation-20261018/audit_independent.py', 'five-row-cancellation-20261018/audit_independent_receipt.json', 'five-row-cancellation-20261018/verification.json', 'five-row-cancellation-20261018/verify.py', 'requirements.txt', 'root-review/check.py', 'root-review/receipt.json', 'verification.json', 'verify.py')
CHECKER_SHA256 = {'five-row-c12-20261018/verify.py': '187230c31c5cf8da5bd5b4e4e0b119987e69e638e5db02d126c3583aa61238f1', 'five-row-c12-audit-20261018/audit_c12.py': '66d08db95bd6f797d2afde9fb19ec09462130c96efaf8916cb213cc5582a70ec', 'five-row-c12-audit-20261018/audit_complement.py': '20c0b8ad05235c618a010bd202cf56ce439dd9246e3c648a6231956ce54ca256', 'five-row-c12-audit-20261018/audit_reduction.py': '5b444d4d329231b072101708a34787b4a4a1f1de6bd1d34cd76b61bc5107f919', 'five-row-c12-audit-20261018/audit_final_tables.py': '5dd2664abf36d1548f6c095262991136f7d89e335cc1f311710790df3d63fee4', 'five-row-cancellation-20261018/verify.py': '17beefc8e6108cbc95081d367176fe9403a00cdbb0a9883a138353ef5bd02484', 'five-row-cancellation-20261018/audit_independent.py': '64c9957cfe9d2213fd376b2ba9e6aa77dffa826a5de127a6b8bbce59c2a042b5', 'root-review/check.py': '1c3cfa527ee4c079123a99a3441e4a6a6a129b7cb3b61cc56946af57451219d5'}
ALL_FILES = set(PAYLOAD) | {'manifest.json', 'SHA256SUMS'}
PRIMARY='five-row-c12-20261018'
AUDIT='five-row-c12-audit-20261018'
PRIOR='five-row-cancellation-20261018'

def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    def unique(pairs):
        value = {}
        for key, item in pairs:
            require(key not in value, 'Duplicate JSON key: ' + key)
            value[key] = item
        return value
    def finite(value):
        raise ValueError('Non-finite JSON constant: ' + value)
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique, parse_constant=finite)


def integrity(root):
    actual = set()
    allowed_dirs = {str(PurePosixPath(name).parent) for name in ALL_FILES} - {'.'}
    for item in root.rglob('*'):
        name = item.relative_to(root).as_posix()
        require(not item.is_symlink(), 'Symlink not permitted: ' + name)
        if item.is_dir():
            require(name in allowed_dirs, 'Unexpected directory: ' + name)
        else:
            require(item.is_file(), 'Non-regular file: ' + name)
            actual.add(name)
    require(actual == ALL_FILES, 'File inventory mismatch: missing=' + str(sorted(ALL_FILES-actual)) + ', unexpected=' + str(sorted(actual-ALL_FILES)))
    manifest = read_json(root/'manifest.json')
    require(manifest['schema'] == 'five-row-one-partial-row-manifest-v1', 'Manifest schema mismatch')
    require(manifest['algorithm'] == 'sha256' and manifest['expected_base_commit'] == BASE, 'Manifest algorithm/base mismatch')
    require([e['path'] for e in manifest['files']] == sorted(PAYLOAD), 'Manifest inventory mismatch')
    for entry in manifest['files']:
        content = (root/entry['path']).read_bytes()
        require(len(content) == entry['bytes'] and sha(content) == entry['sha256'], 'File size/hash mismatch: ' + entry['path'])
    sums = ''.join(sha((root/name).read_bytes())+'  '+name+'\n' for name in sorted(set(PAYLOAD)|{'manifest.json'}))
    require((root/'SHA256SUMS').read_text(encoding='utf-8') == sums, 'SHA256SUMS mismatch')
    for name, digest in CHECKER_SHA256.items():
        require(sha((root/name).read_bytes()) == digest, 'Original checker changed: ' + name)
    for entry in read_json(root/'PROVENANCE.json')['files']:
        name = entry['packaged_path']
        require(name in ALL_FILES, 'Unknown provenance path: ' + name)
        content = (root/name).read_bytes()
        require(len(content) == entry['packaged_bytes'] and sha(content) == entry['packaged_sha256'], 'Provenance mismatch: ' + name)
        if name in CHECKER_SHA256:
            require(entry['byte_for_byte'] is True and entry['source_sha256'] == sha(content), 'Checker provenance mismatch: ' + name)
    return len(actual)


def internal_links(root):
    checked = 0
    for name in sorted(ALL_FILES):
        if not name.endswith('.md'):
            continue
        path = root/name
        prose = path.read_text(encoding='utf-8')
        prose = re.sub(r'\\\[.*?\\\]|\\\(.*?\\\)', '', prose, flags=re.S)
        prose = re.sub(r'`[^`]*`', '', prose)
        prose = re.sub(r'^(?: {4}|\t).*$', '', prose, flags=re.M)
        for target in re.findall(r'\[[^\]]*\]\(([^\s)]+)\)', prose):
            parts = urlsplit(target)
            if parts.scheme in ('http', 'https'):
                continue
            require(not parts.scheme and not parts.netloc and not parts.path.startswith('/'), 'Non-relative internal link: ' + target)
            if parts.path:
                resolved = (path.parent/unquote(parts.path)).resolve()
                require(resolved.is_relative_to(root.resolve()) and resolved.is_file(), 'Broken or escaping link: ' + name+' -> '+target)
                checked += 1
    return checked


def run(root, script, args=(), expect_success=True):
    flags = ['-B'] + (['-'+'O'*MODE] if MODE else [])
    process = subprocess.run([sys.executable]+flags+[str(root/script)]+list(args), cwd=str((root/script).parent), env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0'), capture_output=True, timeout=900)
    if expect_success:
        require(process.returncode == 0 and not process.stderr, script+' failed: '+process.stderr.decode(errors='replace'))
    return process


def compare(fresh, candidate, label):
    require(fresh == candidate, label + ' differs from exact fresh recomputation')


def rejected_math(fresh, altered, label):
    try:
        compare(fresh, altered, label)
    except ValueError as error:
        require('differs from exact fresh recomputation' in str(error), 'Unexpected mathematical rejection')
        return label
    raise ValueError('Modified mathematical certificate accepted: ' + label)

# Tiny sparse rational polynomial engine. No eval(), symbolic dependency,
# floating-point arithmetic, interpolation or exponent-tuple sampling.
VARIABLES=('d','T','E2','E4','rho','q','h','r','s','t')
ZERO=(0,)*len(VARIABLES)
def clean(p):return {k:Fraction(v) for k,v in p.items() if v}
def constant(v):return clean({ZERO:Fraction(v)})
def variable(name):
    v=list(ZERO);v[VARIABLES.index(name)]=1
    return {tuple(v):Fraction(1)}
def plus(a,b):
    out=dict(a)
    for k,v in b.items():out[k]=out.get(k,0)+v
    return clean(out)
def minus(a,b):return plus(a,{k:-v for k,v in b.items()})
def times(a,b):
    out={}
    for k,v in a.items():
        for l,w in b.items():
            key=tuple(x+y for x,y in zip(k,l));out[key]=out.get(key,0)+v*w
    return clean(out)
def power(a,n):
    require(isinstance(n,int) and n>=0,'Polynomial exponent must be a nonnegative integer')
    out=constant(1)
    while n:
        if n%2:out=times(out,a)
        a=times(a,a);n//=2
    return out
def scalar(a):
    require(set(a)<= {ZERO},'Expected scalar polynomial')
    return a.get(ZERO,Fraction(0))
def parse(expression,env=None):
    env={} if env is None else env
    def visit(node):
        if isinstance(node,ast.Constant):
            require(type(node.value)==int,'Only exact integer constants are allowed')
            return constant(node.value)
        if isinstance(node,ast.Name):
            require(node.id in VARIABLES,'Unknown polynomial variable: '+node.id)
            value=env.get(node.id,variable(node.id))
            return value if isinstance(value,dict) else constant(value)
        if isinstance(node,ast.UnaryOp) and isinstance(node.op,(ast.UAdd,ast.USub)):
            value=visit(node.operand);return value if isinstance(node.op,ast.UAdd) else minus({},value)
        if isinstance(node,ast.BinOp):
            a,b=visit(node.left),visit(node.right)
            if isinstance(node.op,ast.Add):return plus(a,b)
            if isinstance(node.op,ast.Sub):return minus(a,b)
            if isinstance(node.op,ast.Mult):return times(a,b)
            if isinstance(node.op,ast.Div):
                denominator=scalar(b);require(denominator!=0,'Division by zero')
                return clean({k:v/denominator for k,v in a.items()})
            if isinstance(node.op,ast.Pow):
                n=scalar(b);require(n.denominator==1,'Nonintegral polynomial power')
                return power(a,int(n))
        raise ValueError('Unsupported polynomial syntax: '+ast.dump(node))
    return visit(ast.parse(expression,mode='eval').body)
def substitute(poly,env):
    out={}
    for exponents,value in poly.items():
        term=constant(value)
        for name,degree in zip(VARIABLES,exponents):
            if degree:
                v=env.get(name,variable(name));v=v if isinstance(v,dict) else constant(v)
                term=times(term,power(v,degree))
        out=plus(out,term)
    return out
def coefficients(poly,name):
    index=VARIABLES.index(name);out={}
    for exponents,value in poly.items():
        require(all(e==0 for i,e in enumerate(exponents) if i!=index),'Other variables remain')
        out[exponents[index]]=value
    return out

EXPRESSIONS={
'A':'5*T+4*d**2-460',
'P':'68*T+74*d**2-3050',
'Q':'2*T-74*d**2+3050',
'N':'(33*d**2-600*d+7335)*T+25*d**4-480*d**3+2830*d**2+55200*d-630695',
'K':'(468*d**2-8160*d+90060)*T+490*d**4-8880*d**3+75580*d**2+366000*d-4015910',
'J':'(232*d**2-240*d-6760)*T-490*d**4+8880*d**3-75580*d**2-366000*d+4015910',
'H':'(48*d**2-24240)*T**2+(90*d**4-55860*d**2+1875930)*T+55*d**6-28125*d**4+2236245*d**2-38150575',
'C':'(24235-547*d**2)*T**2+(-435*d**4+37590*d**2-1039395)*T+55*d**6-28125*d**4+2236245*d**2-38150575',
'F':'41*q**4-11300*q**3-5027466*q**2-242872100*q+2999439785',
}

def exact_certificates(root,changed_coefficients=None,changed_tables=None,changed_proof=None):
    checks=[]
    def equal(label,a,b):
        require(a==b,'Exact certificate mismatch: '+label);checks.append(label)
    forms={k:parse(v) for k,v in EXPRESSIONS.items()}
    A,P,Q,N,K,J,H,C,F=(forms[k] for k in ('A','P','Q','N','K','J','H','C','F'))
    equal('division-free pair elimination',minus(times(A,K),times(P,N)),times(constant(2),H))
    equal('division-free complement elimination',minus(times(Q,N),times(A,J)),times(constant(2),C))
    source=read_json(root/PRIMARY/'coefficients.json') if changed_coefficients is None else changed_coefficients
    E2,E4,d,T=(variable(k) for k in ('E2','E4','d','T'))
    scale=times(d,T)
    pair10=times(times(constant(Fraction(-1,20160)),scale),minus(times(A,power(E2,2)),times(P,E4)))
    full10=parse('E4*T**2*d/288')
    pair12=times(times(constant(Fraction(1,4838400)),times(E2,scale)),minus(times(N,power(E2,2)),times(K,E4)))
    full12=parse('-E2*E4*T**2*d*(d**2-12*d+119)/6912')
    comp12=times(times(constant(Fraction(-1,4838400)),times(E2,scale)),plus(times(N,power(E2,2)),times(J,E4)))
    expected={'pair10':pair10,'full10':full10,'pair12':pair12,'full12':full12,'comp12':comp12}
    independent=read_json(root/AUDIT/'audit_receipt.json')
    for key,poly in expected.items():
        equal('source coefficient formula '+key,parse(source[key]),poly)
        equal('independent frozen coefficient '+key,parse(independent['computed'][key]),poly)
    equal('complement C12 subtraction',minus(full12,pair12),comp12)
    equal('independent pair eliminated polynomial',parse(independent['pair_half_resultant']),H)
    complementary=read_json(root/AUDIT/'complement_receipt.json')
    equal('independent complement eliminated polynomial',parse(complementary['half_resultant']),C)
    # Symbolic discriminant and exact shifted-polynomial sign certificates.
    a=parse('48*d**2-24240');b=parse('90*d**4-55860*d**2+1875930');c=substitute(H,{'T':0})
    disc=minus(power(b,2),times(constant(4),times(a,c)))
    equal('pair discriminant identity',disc,times(constant(-60),substitute(F,{'q':power(d,2)})))
    Fshift=substitute(F,{'q':parse('529+h')})
    equal('F shift at 529',Fshift,parse('41*h**4+75456*h**3+45880320*h**2+9229344768*h+5573836800'))
    lo=parse('92-4*d**2/5');M=parse('(d**2-18*d+17)/2')
    equal('C lower endpoint identity',substitute(C,{'T':lo}),parse('21*(9*d**2-385)*(7*d**4+10*d**2-220625)/25'))
    C0=substitute(C,{'T':0,'d':parse('25+h')})
    CM=minus({},substitute(C,{'T':M}));CM=substitute(CM,{'d':parse('25+h')})
    equal('negative C(M) expansion',CM,parse('1197*h**6/4+72099*h**5/2+1756644*h**4+44343384*h**3+613489632*h**2+4440240000*h+13283343360'))
    shifted=[('F beyond 23',Fshift),('C(0) beyond 25',C0),('-C(M) beyond 25',CM)]
    for label,expr in [('-leading C','547*d**2-24235'),('-lower endpoint','4*d**2/5-92'),('lower endpoint first factor','9*d**2-385'),('lower endpoint second factor','7*d**4+10*d**2-220625'),('R','(3*d-15)/2'),('B','d*(d-15)/2'),('M','(d**2-18*d+17)/2')]:
        shifted.append((label,substitute(parse(expr),{'d':parse('25+h')})))
    for label,poly in shifted:
        cs=coefficients(poly,'h');require(cs and cs.get(0,0)>0 and all(v>0 for v in cs.values()),'Nonpositive sign certificate '+label);checks.append('positive coefficients: '+label)
    # Cross multiplication for T(rho), avoiding nonpolynomial division.
    numerator=parse('460-4*d**2+(74*d**2-3050)*rho');denominator=parse('5+2*rho')
    equal('C10 solved numerator',plus(times(denominator,parse('4*d**2-460+(-74*d**2+3050)*rho')),times(numerator,denominator)),{})
    equal('T minus lower endpoint numerator',minus(numerator,times(lo,denominator)),parse('42*rho*(9*d**2-385)/5'))
    equal('positive integer product bound',parse('(r-1)*(s-1)*(t-1)'),parse('r*s*t-(r*s+r*t+s*t)+(r+s+t)-1'))
    # Parity logic for d=3 modulo 4: R odd and B even leave exactly one odd outside exponent.
    possible=[k for k in range(4) if k%2==1 and (k*(k-1)//2)%2==0]
    equal('retained-pair parity count',possible,[1])
    tables={};raw_discriminants={}
    for label,poly,ds in [('pair',H,range(1,23,4)),('complement',C,range(1,25,2))]:
        table=[];raw=[]
        for D in ds:
            cs=coefficients(substitute(poly,{'d':D}),'T');require(set(cs)<= {0,1,2} and cs.get(2,0)!=0,'Degenerate quadratic')
            abc=[cs.get(k,Fraction(0)) for k in (2,1,0)];require(all(v.denominator==1 for v in abc),'Nonintegral quadratic')
            aa,bb,cc=map(int,abc);raw.append((D,bb*bb-4*aa*cc))
            content=math.gcd(aa,bb,cc);sign=1 if aa>0 else -1
            a,b,c=(sign*v//content for v in (aa,bb,cc));delta=b*b-4*a*c;floor=math.isqrt(delta) if delta>=0 else None
            require(delta<0 or floor*floor<delta<(floor+1)**2,'Integer root not excluded')
            table.append({'d':D,'primitive_coefficients':[a,b,c],'discriminant':delta,'floor_sqrt':floor})
        tables[label]=table;raw_discriminants[label]=raw
    frozen=read_json(root/PRIMARY/'verification.json')['discriminant_tables'] if changed_tables is None else changed_tables
    for label,table in tables.items():
        equal(label+' table length',len(frozen[label]),len(table))
        for actual,row in zip(table,frozen[label]):
            equal(label+' recorded discriminant metadata', {k:row[k] for k in ('d','discriminant','floor_sqrt')},{k:actual[k] for k in ('d','discriminant','floor_sqrt')})
            a,b,c=actual['primitive_coefficients']
            equal(label+' recorded primitive polynomial',parse(row['primitive_quadratic']),parse(f'{a}*T**2+({b})*T+({c})'))
    for row,(D,delta) in zip(independent['finite_exclusions'],raw_discriminants['pair']):
        equal('independent raw discriminant d='+str(D),(row['d'],row['discriminant']),(D,delta))
    for actual,row in zip(tables['complement'],complementary['finite_exclusions']):
        vals=row['primitive_coefficients'];vals=vals if vals[0]>0 else [-v for v in vals]
        equal('independent primitive complement d='+str(actual['d']),(row['d'],vals,row['primitive_discriminant']),(actual['d'],actual['primitive_coefficients'],actual['discriminant']))
    prose=(root/PRIMARY/'PROOF.md').read_text() if changed_proof is None else changed_proof
    rows=re.findall(r'\| (\d+) \| `([^`]+)` \| (-?\d+) \| (\w+) \|',prose)
    expected_rows=tables['pair']+tables['complement'];equal('printed proof row count',len(rows),18)
    for (D,expr,delta,floor),row in zip(rows,expected_rows):
        expr=re.sub(r'(?<=\d)(?=T)','*',expr.replace('²','**2'));a,b,c=row['primitive_coefficients']
        equal('printed primitive quadratic d='+D,parse(expr),parse(f'{a}*T**2+({b})*T+({c})'))
        equal('printed row data d='+D,(int(D),int(delta),None if floor=='negative' else int(floor)),(row['d'],row['discriminant'],row['floor_sqrt']))
    return {'status':'PASS','exact_certificate_checks':len(checks),'finite_gap_count':18,'primitive_discriminant_tables':tables,'determinant_reconstruction':'NOT_RUN in certificate mode; requires --full','method':'Sparse rational polynomial arithmetic, exact integer gcd and isqrt, no third-party dependencies'}


def full_symbolic(root):
    import sympy
    controls=[]
    with tempfile.TemporaryDirectory(prefix='five-row-full-') as directory:
        work=Path(directory)/'package';shutil.copytree(root,work)
        for folder in (PRIMARY,PRIOR):
            fresh=json.loads(run(work,folder+'/verify.py').stdout)
            require(fresh['optimized']==bool(MODE),'Source optimization mode differs')
            expected=read_json(root/folder/'verification.json')
            compare({k:v for k,v in fresh.items() if k not in ('optimized','sympy')},{k:v for k,v in expected.items() if k not in ('optimized','sympy')},folder+' primary receipt')
        # Run audit_c12 before receipt consumers. audit_reduction also imports
        # audit_c12, which independently reconstructs and refreshes its receipt.
        for script,receipt in [('audit_c12.py','audit_receipt.json'),('audit_complement.py','complement_receipt.json'),('audit_reduction.py','reduction_receipt.json'),('audit_final_tables.py','final_table_receipt.json')]:
            run(work,AUDIT+'/'+script)
            fresh=read_json(work/AUDIT/receipt);expected=read_json(root/AUDIT/receipt)
            compare({k:v for k,v in fresh.items() if k!='sympy'},{k:v for k,v in expected.items() if k!='sympy'},script+' receipt')
        run(work,PRIOR+'/audit_independent.py')
        fresh=read_json(work/PRIOR/'audit_independent_receipt.json');expected=read_json(root/PRIOR/'audit_independent_receipt.json')
        compare({k:v for k,v in fresh.items() if k!='sympy'},{k:v for k,v in expected.items() if k!='sympy'},'prerequisite independent audit')
        compare(json.loads(run(work,'root-review/check.py').stdout),read_json(root/'root-review/receipt.json'),'additional root review')
        for script,message in [(PRIMARY+'/verify.py',b'pair C12: residual = -1'),(PRIOR+'/verify.py',b'C9 after C6,C7,C8: residual = -1'),(AUDIT+'/audit_c12.py',b'deliberately corrupted C12: -1'),(AUDIT+'/audit_complement.py',b'deliberately corrupted complementary resultant: -1')]:
            p=run(work,script,('--negative-control',),expect_success=False)
            require(p.returncode!=0 and message in p.stderr,'Wrong or missing mathematical rejection: '+script)
            controls.append(script)
    return {'status':'PASS','sympy':sympy.__version__,'original_checkers_run':8,'primary_theorem_checks':69,'prerequisite_primary_checks':31,'independent_C12_checks':15,'independent_complement_checks':31,'independent_reduction_checks':4,'printed_rows_checked':18,'source_negative_controls_rejected':controls,'all_fresh_receipts_match':True}


def negative_controls(root):
    rejected=[]
    cases=[]
    altered=read_json(root/PRIMARY/'coefficients.json');altered['pair12']='('+altered['pair12']+')+1'
    cases.append(('coefficient_formula',{'changed_coefficients':altered}))
    altered=read_json(root/PRIMARY/'verification.json')['discriminant_tables'];altered['pair'][1]['discriminant']+=1
    cases.append(('finite_discriminant',{'changed_tables':altered}))
    altered=(root/PRIMARY/'PROOF.md').read_text().replace('| 11529 | 107 |','| 11530 | 107 |')
    cases.append(('printed_proof_table',{'changed_proof':altered}))
    for kind,options in cases:
        try:exact_certificates(root,**options)
        except ValueError as error:
            require('Exact certificate mismatch:' in str(error),'Unexpected negative-control failure')
            rejected.append(kind)
        else:raise ValueError('Modified mathematical certificate accepted: '+kind)
    return rejected


def corruption_controls(root):
    rejected=[]
    for kind in ('modified_file','missing_file','unexpected_file','altered_manifest'):
        with tempfile.TemporaryDirectory(prefix='five-row-corruption-') as directory:
            work=Path(directory)/'package';shutil.copytree(root,work)
            if kind=='modified_file':
                path=work/'README.md';path.write_bytes(path.read_bytes()+b'corrupt\n')
            elif kind=='missing_file':(work/PRIMARY/'coefficients.json').unlink()
            elif kind=='unexpected_file':(work/'unlisted.txt').write_text('unexpected\n')
            else:
                path=work/'manifest.json';data=read_json(path);data['files'][0]['sha256']='0'*64;path.write_text(json.dumps(data))
            try:integrity(work)
            except (ValueError,KeyError,OSError):rejected.append(kind)
            else:raise ValueError('Corruption accepted: '+kind)
    return rejected


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--full',action='store_true',help='Reconstruct all determinant identities and rerun source audits; installed SymPy required.')
    args=parser.parse_args()
    if args.full:
        try:import sympy
        except ImportError as error:raise ValueError('--full requires installed SymPy; no symbolic checks were skipped.') from error
    count=integrity(ROOT);links=internal_links(ROOT)
    certificate=exact_certificates(ROOT);math_controls=negative_controls(ROOT)
    symbolic=full_symbolic(ROOT) if args.full else {'status':'NOT_RUN','reason':'Use --full with installed SymPy to reconstruct determinant coefficients and rerun source audits. Frozen symbolic receipts are hash-checked only in default mode.'}
    packaging_controls=corruption_controls(ROOT);integrity(ROOT)
    print(json.dumps({'status':'PASS','verification_mode':'full' if args.full else 'default','optimization':MODE,'python':sys.version.split()[0],'file_count':count,'integrity':'PASS','internal_relative_links_checked':links,'original_mathematical_checkers_unchanged':True,'source_files_unchanged':True,'mathematical_checks':certificate,'symbolic_verification':symbolic,'mathematical_corruptions_rejected':math_controls,'mathematical_controls_bypass_inventory_hashes':True,'rejected_packaging_corruptions':packaging_controls,'scope':'Binary 5-by-5 masks with four full rows and a nonempty remaining row only; distinct real offsets and distinct nonnegative integer exponents.'},indent=2,sort_keys=True))

if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,TypeError,OSError,subprocess.SubprocessError) as error:
        print('FAIL: '+str(error),file=sys.stderr);sys.exit(1)
