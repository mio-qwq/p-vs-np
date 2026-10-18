#!/usr/bin/env python3
"""Independent exact audit. Does not import or execute producer arithmetic.

All 65,536 labelled supports are covered. Polynomial determinants use a
2+2 Laplace expansion in SymPy's QQ polynomial rings. Common zeros are excluded
using raw coefficient polynomials restricted to an independently found affine
line and saturated by the distinctness polynomial. No numerical samples.
"""
import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
from time import monotonic
from sympy import QQ
from sympy.polys.rings import ring

HERE=Path(__file__).resolve().parent
FROZEN={
 'REPORT.md':'85356654eb474399665ac8ffdc65548c786598cddd7a8aa08f96a3f0ae3facb9',
 'check_tail_gap.py':'4b4f841b3a9796072612b6645bc2bae0d86ee32e47dceb34e78b59ae8987b0d9',
 'exact_certificate.json':'e4ec005ccd471665c9f7b81ef3116eaf3fa8f1c2b719413583af1e9b67185a78'}

def need(ok,msg):
 if not ok: raise RuntimeError(msg)

@lru_cache(None)
def pm_count(rows, columns):
 """Count perfect matchings by deletion-contraction, not permutation listing."""
 if not rows: return int(not columns)
 if len(rows)!=columns.bit_count(): return 0
 choices=rows[0]&columns
 total=0
 while choices:
  bit=choices&-choices; choices-=bit
  total+=pm_count(rows[1:],columns^bit)
 return total

@lru_cache(None)
def support_info(rows):
 n=len(rows); columns=(1<<n)-1
 count=pm_count(rows,columns)
 if not count: return count,0,()
 # Signed matching recurrence gives the binary matrix determinant.
 def integer_det(rs, cs):
  if not rs:return 1
  total=0
  for pos,col in enumerate(cs):
   if rs[0]>>col&1:
    total+=(-1)**pos*integer_det(rs[1:],cs[:pos]+cs[pos+1:])
  return total
 top=integer_det(rows,tuple(range(n)))
 # An edge is allowed exactly when its complementary minor has a matching.
 allowed=[]
 for i,row in enumerate(rows):
  allowed.append(sum(1<<j for j in range(n) if row>>j&1 and
     pm_count(rows[:i]+rows[i+1:],columns^(1<<j))))
 # Grow a connected component by alternating row and column closure.
 unseen=set(range(n)); components=[]
 while unseen:
  rset={min(unseen)}; cset=set()
  while True:
   newc={j for i in rset for j in range(n) if allowed[i]>>j&1}
   newr={i for i in range(n) if any(allowed[i]>>j&1 for j in newc)}
   if newr==rset and newc==cset:break
   rset,cset=newr,newc
  need(len(rset)==len(cset),'Unbalanced allowed-edge component')
  unseen-=rset; components.append((tuple(sorted(rset)),tuple(sorted(cset))))
 return count,top,tuple(components)

R,x,bb,cc=ring('x,b,c',QQ)
S,b,c=ring('b,c',QQ)
U,t=ring('t',QQ)
D=b*c*(b-1)*(c-1)*(c-b)
FACTORS=(b,c,b-1,c-1,c-b)

def sat(poly, divisor):
 """Remove the entire gcd with divisor repeatedly, rather than factor peeling."""
 if not poly:return poly
 while True:
  common=poly.gcd(divisor)
  if common.is_ground:return poly
  poly=poly.exquo(common)

def determinant_coeffs(rows,m):
 powers=[[(x+offset)**e for e in (0,1,2,m)] for offset in (0,1,bb,cc)]
 A=[[powers[i][j] if rows[i]>>j&1 else R.zero for j in range(4)] for i in range(4)]
 det=R.zero
 # Generalized Laplace expansion along rows {0,1}.
 for j,k in combinations(range(4),2):
  l,h=[q for q in range(4) if q not in (j,k)]
  det+=(-1)**(1+j+k)*(A[0][j]*A[1][k]-A[0][k]*A[1][j])*(A[2][l]*A[3][h]-A[2][h]*A[3][l])
 coeffs=[S.zero for _ in range(m+4)]
 for (i,j,k),value in det.items():
  coeffs[i][j,k]=value
 return coeffs

def evaluate(poly,bt,ct):
 if not poly:return U.zero
 bp=[U.one];cp=[U.one]
 for i in range(max(ij[0] for ij in poly)):bp.append(bp[-1]*bt)
 for i in range(max(ij[1] for ij in poly)):cp.append(cp[-1]*ct)
 return sum((value*bp[i]*cp[j] for (i,j),value in poly.items()),U.zero)

def independently_prove(coeffs):
 nonzero=[j for j,p in enumerate(coeffs) if p]
 need(bool(nonzero),'Identically zero determinant')
 # A single saturated coefficient may already exclude the whole domain.
 lead=nonzero[-1]; L=sat(coeffs[lead],D)
 if L.is_ground:return {'kind':'direct','degree':lead,'constant':str(L)}
 if max(i+j for i,j in L)>1:
  for j in nonzero:
   q=sat(coeffs[j],D)
   if q.is_ground:return {'kind':'direct','degree':j,'constant':str(q)}
  raise RuntimeError('No direct obstruction and leading relation is nonlinear')
 l0=L.get((0,0),QQ.zero);lb=L.get((1,0),QQ.zero);lc=L.get((0,1),QQ.zero)
 if lc: bt=t;ct=-l0/lc-(lb/lc)*t
 else:
  need(bool(lb),'Constant erroneously sent to line branch')
  bt=U(-l0/lb);ct=t
 need(not evaluate(L,bt,ct),'Independent line does not solve leading relation')
 g=U.zero
 for q in coeffs:g=g.gcd(evaluate(q,bt,ct))
 if g:g=g.monic()
 dt=evaluate(D,bt,ct)
 need(bool(dt),'Relation forces coincident offsets')
 residue=sat(g,dt)
 if residue:residue=residue.monic()
 need(bool(residue) and residue.is_ground,
      'Unresolved distinct-offset common zero: '+str(residue))
 return {'kind':'raw_line','degree':lead,'line':str(L),'b':str(bt),'c':str(ct),
         'raw_gcd':str(g),'distinctness':str(dt),'saturated_gcd':str(residue)}

def read_poly(serialized):return S.from_dict({(i,j):QQ(value) for i,j,value in serialized})
def read_uni(serialized):return U.from_dict({(i,):QQ(v) for i,v in enumerate(serialized) if QQ(v)})

def verify_saved_record(record, rows, coeffs):
 need(tuple(record['rows'])==rows,'Wrong record support')
 need(record['matching_count']==support_info(rows)[0],'Wrong matching count')
 j=record['coefficient_degree']; need(0<=j<len(coeffs),'Invalid degree')
 if record['kind']=='direct':
  need(read_poly(record['coefficient'])==coeffs[j],'Stored direct coefficient is incorrect')
  q=coeffs[j]
  # Verify its supplied scalar using exact successive division; arithmetic is
  # delegated to an independent polynomial-ring implementation.
  for f in FACTORS:
   while q:
    quo,rem=q.div(f)
    if rem:break
    q=quo
  need(q.is_ground and q==S(QQ(record['stripped_constant'])) and bool(q),
       'Invalid direct constant witness')
 else:
  need(record['kind']=='linear_reduction','Unknown record kind')
  stripped=[]
  for p in coeffs:
   for f in FACTORS:
    while p:
     quo,rem=p.div(f)
     if rem:break
     p=quo
   stripped.append(p)
  L=read_poly(record['leading_stripped'])
  need(stripped[j]==L and bool(L),'Incorrect saved leading relation')
  need(j==max(k for k,q in enumerate(stripped) if q),'Incorrect leading degree')
  need(max(i+k for i,k in L)<=1 and not L.is_ground,'Relation is not affine linear')
  bt=read_uni(record['b_of_t']);ct=read_uni(record['c_of_t'])
  need(not evaluate(L,bt,ct),'Saved parameterization misses line')
  # Affine, nonconstant map into a line is surjective over C.
  need(max(bt.degree(),ct.degree())==1,'Saved map does not cover line')
  g=U.zero
  for q in stripped:g=g.gcd(evaluate(q,bt,ct))
  if g:g=g.monic()
  need(g==read_uni(record['reduced_gcd']) and bool(g),'Wrong saved gcd')
  dt=evaluate(D,bt,ct)
  need(dt==read_uni(record['distinctness_polynomial']) and bool(dt),'Wrong saved distinctness')
  residue=g
  for removed in record['removed_distinctness_gcds']:
   h=read_uni(removed)
   need(h==residue.gcd(dt).monic() and not h.is_ground,'Wrong saved removed gcd')
   residue=residue.exquo(h)
  need(residue==U(QQ(record['final_constant'])) and residue.is_ground and bool(residue),
       'Saved gcd saturation did not finish')

def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--certificate',type=Path,help='Also independently check all saved certificate witnesses')
 ap.add_argument('--source-dir',type=Path,help='Also verify the three original frozen source hashes')
 ap.add_argument('--output-dir',type=Path,default=HERE,help='Directory for independent results and corrupt-control files')
 args=ap.parse_args();start=monotonic();args.output_dir.mkdir(parents=True,exist_ok=True)
 if args.source_dir:
  for name,digest in FROZEN.items():
   need(sha256((args.source_dir/name).read_bytes()).hexdigest()==digest,'Frozen artifact changed: '+name)
  print('PASS: frozen hashes',flush=True)

 # Enumerate every labelled binary 4x4 mask, including masks with zero rows.
 all_counts=Counter();classes=set(); connected=set();class_counts=Counter()
 for mask in range(1<<16):
  rows=tuple(sorted((mask>>(4*i))&15 for i in range(4)))
  count,top,components=support_info(rows)
  all_counts['all_labelled_masks']+=1
  if not count:all_counts['no_perfect_matching']+=1;continue
  all_counts['with_perfect_matching']+=1
  if top:all_counts['nonzero_top_coefficient']+=1
  elif len(components)>1:all_counts['disconnected_singular']+=1
  else:all_counts['connected_singular']+=1
  classes.add(rows)
  if not top and len(components)==1:connected.add(rows)
 for rows in classes:
  count,top,components=support_info(rows)
  class_counts['with_perfect_matching']+=1
  if top:class_counts['nonzero_top_coefficient']+=1
  elif len(components)>1:
   class_counts['disconnected_singular']+=1
   need(all(len(rr)<=3 for rr,cc in components),'Disconnected block exceeds order three')
  else:class_counts['connected_singular']+=1
 nonzero_classes={tuple(sorted((mask>>(4*i))&15 for i in range(4)))
                  for mask in range(1<<16) if all((mask>>(4*i))&15 for i in range(4))}
 need(len(nonzero_classes)==3060,'Wrong nonzero-row orbit count')
 need(len(nonzero_classes-classes)==1062,'Wrong no-matching orbit count')
 need(class_counts==Counter(with_perfect_matching=1998,nonzero_top_coefficient=940,
      disconnected_singular=851,connected_singular=207),'Incorrect support reduction')
 print('PASS: all 65,536 labelled supports; '+str(dict(all_counts)),flush=True)
 print('PASS: independent row-orbit reduction; '+str(dict(class_counts)),flush=True)
 order3=Counter()
 for mask in range(1<<9):
  rows=tuple((mask>>(3*i))&7 for i in range(3))
  count=pm_count(rows,7);order3[count]+=1
  if count==4:need(mask.bit_count()==8,'Four-matchings support not full minus one edge')
 need(dict(order3)=={0:265,1:150,2:69,3:18,4:9,6:1},'Incorrect order-three classification')
 print('PASS: all 512 order-three supports independently classified',flush=True)

 saved=json.loads(args.certificate.read_text()) if args.certificate else None
 if args.certificate:
  need(isinstance(saved,dict) and isinstance(saved.get('cases'),list),'Malformed saved certificate')
 cases=saved['cases'] if saved else [{'exponents':[0,1,2,m]} for m in range(4,12)]
 need([q['exponents'] for q in cases]==[[0,1,2,m] for m in range(4,12)],'Incomplete exponent coverage')
 output={'labelled_counts':dict(all_counts),'orbit_counts':dict(class_counts),
         'order3_counts':dict(order3),'cases':[]}
 for case in cases:
  m=case['exponents'][-1]
  if saved:
   records=case['certificates']
   expected_counts={'nonzero_row_multisets':3060,'no_perfect_matching':1062,
    'with_perfect_matching':1998,'nonzero_top_coefficient':940,'singular_support':1058,
    'decomposes_into_orders_at_most_three':851,'connected_singular_support':207,
    'distinctness_factor_coefficient':171 if m==4 else 173,
    'linear_reduction_distinctness_obstruction':36 if m==4 else 34}
   need(case['counts']==expected_counts,'Incorrect saved class counts')
   need(Counter(r['kind'] for r in records)==Counter(direct=171 if m==4 else 173,
        linear_reduction=36 if m==4 else 34),'Incorrect saved method counts')
   need(len(records)==207,'Incorrect record count')
   lookup={tuple(r['rows']):r for r in records}
   need(set(lookup)==connected and len(lookup)==207,'Certificate omitted or duplicated a support')
  proofs=[];kinds=Counter()
  for rows in sorted(connected):
   coefficients=determinant_coeffs(rows,m)
   proof=independently_prove(coefficients)
   if saved:verify_saved_record(lookup[rows],rows,coefficients)
   proof['rows']=rows;proofs.append(proof);kinds[proof['kind']]+=1
  output['cases'].append({'m':m,'kinds':dict(kinds),'proofs':proofs})
  extra=' and saved witnesses checked' if saved else ''
  print(f'PASS: m={m}, all 207 supports independently proved{extra}; {dict(kinds)}',flush=True)

 # Exact negative controls using the same independent determinant expansion.
 exceptional=determinant_coeffs((6,15,15,15),3)
 quadratic=t*t+t+1;bt=t;ct=-1-t
 need(all(not evaluate(p,bt,ct).rem(quadratic) for p in exceptional),'m=3 counterexample not zero')
 need(evaluate(D,bt,ct).gcd(quadratic).is_ground,'m=3 counterexample has repeated offsets')
 try:independently_prove(exceptional)
 except RuntimeError as exc:
  need('Unresolved distinct-offset common zero' in str(exc) and 't**2 + t + 1' in str(exc),
       'm=3 rejected for an unexpected reason: '+str(exc))
 else:raise RuntimeError('False m=3 extension was accepted')
 print('PASS: m=3 exact complex counterexample and rejection',flush=True)
 repeated=determinant_coeffs((15,15,15,15),4)
 need(all(not evaluate(p,U.zero,U(2)) for p in repeated),'Repeated-offset counterexample not zero')
 need(not evaluate(D,U.zero,U(2)),'Repeated offsets were not excluded')
 print('PASS: repeated-offset zero determinant is outside distinctness domain',flush=True)

 # Corrupt a physically saved direct witness, then reread and reject it.
 rows=(3,5,10,12);coeffs=determinant_coeffs(rows,4);p=coeffs[0]
 rec={'rows':list(rows),'matching_count':support_info(rows)[0],'kind':'direct',
      'coefficient_degree':0,'coefficient':[[i,j,str(v)] for (i,j),v in sorted(p.items())],
      'stripped_constant':'-1'}
 verify_saved_record(rec,rows,coeffs)
 rec['coefficient'][0][2]=str(QQ(rec['coefficient'][0][2])+1)
 corruptpath=args.output_dir/'corrupt_witness.json'
 corruptpath.write_text(json.dumps(rec,separators=(',',':'))+'\n')
 try:verify_saved_record(json.loads(corruptpath.read_text()),rows,coeffs)
 except RuntimeError as exc:need('Stored direct coefficient is incorrect' in str(exc),'Wrong corruption rejection')
 else:raise RuntimeError('Corrupt coefficient accepted')
 if saved:
  corrupt=json.loads(args.certificate.read_text())
  first=corrupt['cases'][0]['certificates'][0]
  first['coefficient'][0][2]=str(QQ(first['coefficient'][0][2])+1)
  (args.output_dir/'corrupt_certificate.json').write_text(json.dumps(corrupt,separators=(',',':'))+'\n')
 print('PASS: physical coefficient corruption independently rejected',flush=True)
 output['elapsed_seconds']=monotonic()-start
 (args.output_dir/'independent_results.json').write_text(json.dumps(output,indent=2)+'\n')
 print(f'PASS: complete independent exact audit in {monotonic()-start:.1f} seconds',flush=True)

if __name__=='__main__':main()
