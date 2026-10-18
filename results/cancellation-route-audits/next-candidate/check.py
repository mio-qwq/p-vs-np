from itertools import permutations
from math import comb
from fractions import Fraction as F
import json
E=[0,5,9,12,14]; keep={1,4}
def coefficient(order):
 out={}
 for p in permutations(range(5)):
  if p[0] not in keep: continue
  sign=(-1)**sum(p[i]>p[j] for i in range(5) for j in range(i+1,5))
  poly={(0,0):1}
  for row in range(1,5):
   new={}; degree=E[p[row]]
   for (z,v),c in poly.items():
    for h in range(min(degree,order-z)+1):
     key=(z+h,v+(h if row>=3 else 0)); val=c*comb(degree,h)*((-1)**h if row in (1,3) else 1)
     new[key]=new.get(key,0)+val
   poly=new
  for (z,v),c in poly.items():
   if z==order:out[v]=out.get(v,0)+sign*c
 return {i:c for i,c in out.items() if c}
def reduce_v(poly):
 d={k:F(v) for k,v in poly.items()}
 # 209 v^4 - 1226 v^2 +209 =0
 for k in range(max(d,default=0),3,-1):
  c=d.pop(k,F(0));d[k-2]=d.get(k-2,F(0))+c*F(1226,209);d[k-4]=d.get(k-4,F(0))-c
 return {k:str(v) for k,v in d.items() if v}
out=[]
for order in range(6,15):
 p=coefficient(order);q=reduce_v(p);out.append({'moment':order,'lambda_degree':40-order,'polynomial_in_v':p,'remainder_mod_209v4_1226v2_209':q})
 if q:
  if order!=12:raise ValueError(('unexpected first survivor',order))
  break
if not out[-1]['remainder_mod_209v4_1226v2_209']:raise ValueError('no survivor')
print(json.dumps(out,indent=2))
