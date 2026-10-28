#!/usr/bin/env python3
"""Portable exact replay. No network; all generated files live in a temporary directory."""
import argparse
from collections import Counter
import hashlib
from itertools import permutations
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time
sys.dont_write_bytecode = True
from phi import phi_direct
import sympy as s

ROOT = Path(__file__).resolve().parents[1]
ORDERS = sorted(''.join(p) for p in permutations('abcde')
                if p.index('b') < p.index('c') and p.index('d') < p.index('e'))
NAMES = ['shapes', 'L_zero', 'A_zero', 'K_zero', 'regular', 'M_zero',
         'Z_zero', 'R_minus4', 'mod101', 'mod103']

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def run(argv, cwd):
    out = subprocess.run(list(map(str, argv)), cwd=cwd, text=True,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    return out.stdout

def hashes():
    path = ROOT / 'SHA256SUMS'
    require(path.is_file(), 'missing SHA256SUMS')
    count = 0
    for line in path.read_text().splitlines():
        digest, name = line.split('  ', 1)
        target = ROOT / name
        require(target.is_file(), 'missing manifest file ' + name)
        require(hashlib.sha256(target.read_bytes()).hexdigest() == digest,
                'hash mismatch ' + name)
        count += 1
    return count

def polynomial():
    L, A, t, R, Z = s.symbols('L A t R Z')
    data = json.loads((ROOT/'inputs/C7_FORMULAS.json').read_text())
    P = s.Poly(s.cancel(L**5*s.sympify(data['Phi']).subs(
        {R:A/L, Z:t+2*A/L+1}, simultaneous=True)), L, A, t, domain=s.ZZ)
    terms = [(int(c), *m) for m, c in P.terms()]
    require(len(terms) == 112 and P.degree_list() == (8, 6, 6), 'P7 shape')
    source = (ROOT/'sources/engine_a.cpp').read_text()
    block = source.split('static const Term terms[]={', 1)[1].split('};', 1)[0]
    embedded = [(int(c), int(i), int(j), int(k)) for i,j,k,c in
                re.findall(r'\{(-?\d+),(-?\d+),(-?\d+),(-?\d+)\}', '{'+block)]
    require(embedded == terms, 'engine A term table differs from fresh Phi expansion')
    require(re.findall(r'"([abcde]{5})"', source) == ORDERS, 'all 30 labels')
    return terms

def peval(terms, L, A, t):
    return sum(c*L**i*A**j*t**k for c,i,j,k in terms)

def coords(row):
    B,C,D,E = row
    u=D+E; x=u-B; y=u-C; L=x+y; A=x*y; t=u-L
    M=2*L**3-5*L**2*t+2*L*t*t-18*A*L+A*t-15*A-20*L
    order=''.join(ch for val,ch in sorted(zip((0,*row),'abcde')))
    return L,A,t,M,order

def valid(row, H):
    B,C,D,E=row
    require(B<C and D<E and len(set((0,*row)))==5, 'canonical distinctness')
    require(max(0,*row)-min(0,*row)<=H, 'span')
    require(D*E==(D+E)*(B+C)-B*B-C*C, 'C3')

def read_a(path, H):
    rows=[]
    for line in path.read_text().splitlines():
        v=list(map(int,line.split())); require(len(v)==7, 'engine A row length')
        row=tuple(v[:4]); valid(row,H); B,C,D,E=row
        require(v[4:]==[D+E-B,D+E-C,B+C-D-E], 'engine A coordinates')
        rows.append(row)
    require(len(rows)==len(set(rows)), 'duplicate A output')
    return set(rows)

def read_b(path, H):
    rows=[]
    for line in path.read_text().splitlines():
        v=line.split(); require(len(v)==9, 'engine B row length')
        row=tuple(map(int,v[:4]));valid(row,H);L,A,t,M,order=coords(row)
        require(v[4]==order and list(map(int,v[5:]))==[L,A,t,M], 'B coordinates')
        rows.append(row)
    require(len(rows)==len(set(rows)), 'duplicate B output')
    return set(rows)

def exact(rows, terms):
    negative=positive=0
    for row in rows:
        L,A,t,M,order=coords(row)
        require(L*A*(A+2*L)!=0, 'excluded low branch in survivor data')
        v=peval(terms,L,A,t)
        require(v%101==0 and v%103==0, 'invalid modular survivor')
        require(v==phi_direct(L,A,t), 'sparse P7 versus handwritten Phi mismatch')
        require(v!=0, 'exact P7 zero')
        positive+=v>0;negative+=v<0
    return {'rows':len(rows),'positive_P7':positive,'negative_P7':negative,'P7_zeros':0,
            'handwritten_factored_Phi_agrees':True}

def parse_b(text):
    meta={};orders={}
    for line in text.splitlines():
        v=line.split()
        if len(v)==11 and v[0] in ORDERS: orders[v[0]]=list(map(int,v[1:]))
        elif len(v)==2 and v[0]!='seconds':meta[v[0]]=int(v[1])
    require(set(meta)=={'H','bc_pairs','factor_pairs','all_c3','selected_c3'}, 'B summary')
    require(meta['all_c3']==meta['selected_c3'], 'B must run all orders')
    return meta,{o:orders.get(o,[0]*10) for o in ORDERS}

def pair(Aexe,Bexe,H,work):
    a=json.loads(run([Aexe,H,work/f'a-{H}.tsv'],work))
    meta,b=parse_b(run([Bexe,H,'all'],work))
    sums=[sum(row[i] for row in b.values()) for i in range(10)]
    require(a['height']==H and meta['H']==H, 'height mismatch')
    require(a['BC_pairs']==meta['bc_pairs'], 'outer pair count')
    for k,i in [('shapes',0),('L_zero',1),('A_zero',2),('K_zero',3),
                ('regular',4),('mod101',8),('mod103',9)]:
        require(a[k]==sums[i], 'independent engine counter '+k)
    require(a['orders']==[b[o][0] for o in ORDERS], 'per-order C3 counters')
    ra=read_a(work/f'a-{H}.tsv',H)
    rb=read_b(work/f'allorders-survivors-{H}.tsv',H)
    require(len(ra)==a['mod103']==len(rb)==sums[9], 'truncated output / survivor count')
    require(ra==rb, 'independent engine survivor sets differ')
    return a,meta,b,ra

def small_control(Bexe,terms,work,b,rows):
    H=40; brute=set();byorder={o:[0]*10 for o in ORDERS};bc_pairs=0
    for B in range(-H,H+1):
        if B==0:continue
        for C in range(B+1,H+1):
            if C==0 or max(0,C)-min(0,B)>H:continue
            bc_pairs+=1
            for D in range(-H,H+1):
                den=D-B-C;num=D*(B+C)-B*B-C*C
                if den==0 or num%den:continue
                E=num//den;row=(B,C,D,E)
                if D>=E or len(set((0,*row)))!=5 or max(0,*row)-min(0,*row)>H:continue
                brute.add(row);L,A,t,M,o=coords(row);c=byorder[o];c[0]+=1
                if L==0:c[1]+=1;continue
                if A==0:c[2]+=1;continue
                if A+2*L==0:c[3]+=1;continue
                c[4]+=1;c[5]+=M==0;c[6]+=L*(t+1)+2*A==0;c[7]+=A+4*L==0
                value=peval(terms,L,A,t)
                if value%101:continue
                c[8]+=1
                if value%103:continue
                c[9]+=1
    run([Bexe,H,'dump'],work)
    dumped=[tuple(map(int,line.split()[:4])) for line in (work/'all-40.tsv').read_text().splitlines()]
    require(len(dumped)==len(set(dumped)), 'duplicate dumped C3 tuple')
    require(set(dumped)==brute and len(brute)==3402, 'direct-E vs signed-divisor coverage')
    require(byorder==b, 'direct bigint vs C++ modular/low/singular counts at H40')
    negatives=sum(D-B-C<0 and E-B-C<0 for B,C,D,E in brute)
    require(negatives==1081, 'negative-negative divisor omission control')
    return {'height':H,'C3_tuples':len(brute),'BC_pairs':bc_pairs,
            'omitting_negative_negative_branch_loses':negatives,
            'both_engines_and_direct_E_counts_agree':True}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--quick',action='store_true',help='H40 + all 2432 recorded exact survivors; skip full height and fresh coefficient derivation')
    parser.add_argument('--full',action='store_true',help='default: add both full-height engines and fresh C3-C7 derivation')
    parser.add_argument('--sanitize',action='store_true',help='compile both engines with undefined/bounds sanitizers')
    parser.add_argument('--skip-hashes',action='store_true',help='development-only; report omitted hash verification')
    args=parser.parse_args();require(not(args.quick and args.full),'choose quick or full')
    start=time.monotonic();report={'mode':'quick' if args.quick else 'full'}
    report['verified_manifest_files']=None if args.skip_hashes else hashes()
    terms=polynomial();report['integer_P7_terms']=len(terms)
    stored=read_b(ROOT/'certificates/survivors.tsv',1632)
    require(len(stored)==2432,'certificate count');report['exact_certificate']=exact(stored,terms)
    compiler=shutil.which('g++');require(compiler is not None,'g++ is required')
    report['compiler']=run([compiler,'--version'],ROOT).splitlines()[0]
    report['python']=sys.version.split()[0];report['sympy']=s.__version__
    with tempfile.TemporaryDirectory(prefix='overlap-proof-') as temp:
        work=Path(temp)
        header='struct Term { long long c; int l,a,t; };\nconst std::vector<Term> P7={\n'
        header+=''.join('{'+','.join(map(str,row))+'},\n' for row in terms)+'};\n'
        (work/'polynomials.hpp').write_text(header)
        flags=['-std=c++17','-O2','-Wall','-Wextra']
        if args.sanitize:flags+=['-fsanitize=undefined,bounds','-fno-sanitize-recover=all','-D_GLIBCXX_ASSERTIONS']
        Aexe=work/'engine_a';Bexe=work/'engine_b'
        for source,exe in [('engine_a.cpp',Aexe),('engine_b.cpp',Bexe)]:
            run([compiler,*flags,'-I',work,ROOT/'sources'/source,'-o',exe],work)
        a,meta,b,rows=pair(Aexe,Bexe,40,work)
        report['small_control']=small_control(Bexe,terms,work,b,rows)
        report['structural_control']=json.loads(run([sys.executable,ROOT/'scripts/check_structure.py'],work))['status']
        if not args.quick:
            a,meta,b,rows=pair(Aexe,Bexe,1632,work)
            require(rows==stored,'full replay differs from recorded certificate')
            require(a==json.loads((ROOT/'certificates/engine_a_counts.json').read_text()),'recorded A counts')
            audit=json.loads((ROOT/'certificates/engine_b_audit.json').read_text())
            require(meta==audit['complete_C3_totals'],'recorded B totals')
            require(b=={o:audit['per_order'].get(o,[0]*10) for o in ORDERS},'recorded B per-order counters')
            report['full_engine_counts']=a;report['full_singular_counts']={name:sum(v[i] for v in b.values()) for name,i in [('M_zero',5),('Z_zero',6),('R_minus4',7)]}
            report['full_exact_replay']=exact(rows,terms)
            # The independent coefficient script derives before reading the old table.
            output=run([sys.executable,ROOT/'scripts/check_coefficients.py'],work)
            report['fresh_coefficient_control']=json.loads(output)
            require(report['fresh_coefficient_control']['status']=='PASS','coefficient checker status')
    report['sanitizers']=args.sanitize;report['elapsed_seconds']=round(time.monotonic()-start,3)
    report['status']='PASS';print(json.dumps(report,indent=2,sort_keys=True))

if __name__=='__main__':main()
