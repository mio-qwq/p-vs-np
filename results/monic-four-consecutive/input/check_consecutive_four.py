#!/usr/bin/env python3
"""Exact order-four masked Vandermonde certificate, Python standard library only.

All polynomials are recomputed from signed permutation products. No result from
SymPy, stored symbolic output, random samples, or floating-point arithmetic is
used. Output is a deterministic algebraic classification, not a numerical test.
"""
from fractions import Fraction as F
from itertools import permutations, combinations_with_replacement
from math import comb
from collections import Counter
from pathlib import Path
import json

# Sparse rational polynomials in b,c, exponent-pair keys.
def clean(p): return {k:F(v) for k,v in p.items() if v}
def add(p,q):
 r=dict(p)
 for k,v in q.items():r[k]=r.get(k,0)+v
 return clean(r)
def scale(p,s):return clean({k:v*s for k,v in p.items()})
def mul(p,q):
 r={}
 for (i,j),v in p.items():
  for (k,l),w in q.items():r[i+k,j+l]=r.get((i+k,j+l),0)+v*w
 return clean(r)
def divrem(p,q):
 assert q
 work=dict(p);out={};rem={};qkey=max(q);qval=q[qkey]
 while work:
  key=max(work);val=work[key]
  if all(key[i]>=qkey[i] for i in (0,1)):
   k=(key[0]-qkey[0],key[1]-qkey[1]);v=val/qval
   out[k]=out.get(k,0)+v
   work=add(work,scale(mul({k:F(1)},q),-v))
  else:
   rem[key]=val;del work[key]
 return clean(out),clean(rem)
ONE={(0,0):F(1)};B={(1,0):F(1)};C={(0,1):F(1)}
FACTORS=[B,C,add(B,scale(ONE,-1)),add(C,scale(ONE,-1)),add(C,scale(B,-1))]
D=ONE
for f in FACTORS:D=mul(D,f)
def strip(p):
 q=p
 for factor in FACTORS:
  while q:
   quotient,remainder=divrem(q,factor)
   if remainder:break
   q=quotient
 return q

# Dense rational univariate polynomials, lowest degree first.
def trim(p):
 p=list(map(F,p))
 while p and p[-1]==0:p.pop()
 return tuple(p)
def uadd(p,q):return trim([(p[i] if i<len(p) else 0)+(q[i] if i<len(q) else 0) for i in range(max(len(p),len(q)))])
def umul(p,q):
 if not p or not q:return ()
 r=[F(0)]*(len(p)+len(q)-1)
 for i,a in enumerate(p):
  for j,b in enumerate(q):r[i+j]+=a*b
 return trim(r)
def upow(p,n):
 r=(F(1),)
 for _ in range(n):r=umul(r,p)
 return r
def udivrem(p,q):
 assert q
 p=list(p);out=[F(0)]*max(0,len(p)-len(q)+1)
 while p and len(p)>=len(q):
  k=len(p)-len(q);v=p[-1]/q[-1];out[k]+=v
  for i,w in enumerate(q):p[k+i]-=v*w
  p=list(trim(p))
 return trim(out),trim(p)
def ugcd(p,q):
 while q:p,q=q,udivrem(p,q)[1]
 return trim([v/p[-1] for v in p]) if p else ()
def substitute(p,b,c):
 out=()
 for (i,j),v in p.items():out=uadd(out,tuple(v*a for a in umul(upow(b,i),upow(c,j))))
 return out

def sign(p):return (-1)**sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))
PERMS=list(permutations(range(4)))
def matchings(rows):return [p for p in PERMS if all(rows[i]>>p[i]&1 for i in range(4))]
def connected_allowed(ps):
 adj=[set() for _ in range(8)]
 for p in ps:
  for i,j in enumerate(p):adj[i].add(j+4);adj[j+4].add(i)
 seen={0};stack=[0]
 while stack:
  for v in adj[stack.pop()]-seen:seen.add(v);stack.append(v)
 return len(seen)==8

# Coefficient array in x, each entry a b,c polynomial.
def shifted_power(row,e):
 out=[]
 for xdegree in range(e+1):
  shiftdegree=e-xdegree;coef=F(comb(e,xdegree))
  if row==0: p=ONE if shiftdegree==0 else {}
  elif row==1:p=ONE
  elif row==2:p={(shiftdegree,0):F(1)}
  else:p={(0,shiftdegree):F(1)}
  out.append(scale(p,coef))
 return out
def xmul(p,q):
 out=[{} for _ in range(len(p)+len(q)-1)]
 for i,a in enumerate(p):
  for j,b in enumerate(q):out[i+j]=add(out[i+j],mul(a,b))
 return out
TERMS={}
for p in PERMS:
 coeffs=[scale(ONE,sign(p))]
 for i,e in enumerate(p):coeffs=xmul(coeffs,shifted_power(i,e))
 TERMS[p]=coeffs

def dump_poly(p):return [[i,j,str(v)] for (i,j),v in sorted(p.items())]
def dump_u(p):return [str(v) for v in p]

counts=Counter();certificates=[]
for rows in combinations_with_replacement(range(1,16),4):
 counts['nonzero_row_multisets']+=1
 ps=matchings(rows)
 if not ps:counts['no_perfect_matching']+=1;continue
 counts['with_perfect_matching']+=1
 if sum(sign(p) for p in ps):counts['nonzero_top_coefficient']+=1;continue
 counts['singular_support']+=1
 if not connected_allowed(ps):counts['decomposes_into_orders_at_most_three']+=1;continue
 counts['connected_singular_support']+=1
 coeffs=[{} for _ in range(7)]
 for p in ps:
  for j,a in enumerate(TERMS[p]):coeffs[j]=add(coeffs[j],a)
 stripped=[strip(p) for p in coeffs]
 simple=[j for j,p in enumerate(stripped) if p and set(p)=={(0,0)}]
 cert={'rows':rows,'matching_count':len(ps),'coefficients_by_x_degree':[dump_poly(p) for p in coeffs]}
 if simple:
  counts['distinctness_factor_coefficient']+=1
  j=simple[-1];cert.update(kind='direct',coefficient_degree=j,stripped_constant=str(stripped[j][0,0]))
 else:
  j=max(j for j,p in enumerate(stripped) if p)
  L=stripped[j]
  assert all(i+k<=1 for i,k in L),(rows,L)
  l0=L.get((0,0),0);lb=L.get((1,0),0);lc=L.get((0,1),0)
  if lc:
   b=(F(0),F(1));c=trim((-l0/lc,-lb/lc))
  else:
   assert lb
   b=trim((-l0/lb,));c=(F(0),F(1))
  polys=[substitute(p,b,c) for p in stripped]
  g=()
  for p in polys:g=ugcd(g,p)
  assert g,(rows,'identically zero after relation')
  d=substitute(D,b,c);assert d,(rows,'relation forces repeated offsets')
  residue=g
  while len(residue)>1:
   common=ugcd(residue,d)
   if len(common)<=1:break
   residue,rem=udivrem(residue,common);assert not rem
  cert.update(kind='linear_reduction',leading_stripped=dump_poly(L),b_of_t=dump_u(b),c_of_t=dump_u(c),reduced_gcd=dump_u(g),distinctness_polynomial=dump_u(d))
  if len(residue)==1:
   counts['linear_reduction_distinctness_obstruction']+=1
  else:
   assert rows==(6,15,15,15) and residue==(F(1),F(1),F(1)),(rows,residue)
   # t^2+t+1=(t+1/2)^2+3/4 is positive for all real t.
   counts['positive_quadratic_obstruction']+=1
   cert['real_obstruction']='t^2+t+1=(t+1/2)^2+3/4>0'
 certificates.append(cert)
assert counts['connected_singular_support']==207
assert counts['distinctness_factor_coefficient']==171
assert counts['linear_reduction_distinctness_obstruction']==35
assert counts['positive_quadratic_obstruction']==1
out={'result':'All 4x4 binary masks with a perfect matching have nonzero shifted determinant for four distinct real offsets and consecutive exponents.','arithmetic':'Python fractions.Fraction; complete symbolic coefficients; no parameter samples','counts':dict(counts),'certificates':certificates}
Path(__file__).with_name('exact_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='certificates'},indent=2))
print('PASS: all 207 remaining row-mask classes proved over the reals.')
