import sys,itertools,random,json
from pathlib import Path
from star_solver import *
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'pair'))
# Avoid importing executable test.py: implement tiny independent GL checker here.
def span(bs):
 S={0}
 for b in bs:S|={x^b for x in list(S)}
 return S
def apply(B,x):
 y=0
 for i,b in enumerate(B):
  if x>>i&1:y^=b
 return y
maps=[B for B in itertools.product(range(1,8),repeat=3) if len(span(B))==8]
def endpoints(x):
 s={i for i in range(3) if x>>i&1}
 if len(s)==1:s.add(3)
 return s
checks=0
for m in range(3,7):
 for cols in itertools.combinations(range(1,8),m):
  if rank(cols)<3:continue
  for k in range(1,m+1):
   for ids in itertools.combinations(range(m),k):
    data=extension(list(cols),[(list(ids),k-1)])
    indirect=bool(data and any(all(apply(B,c).bit_count()<=2 for c in data[0]) for B in maps))
    direct=False
    for B in maps:
     out=[apply(B,c) for c in cols]
     if any(c.bit_count()>2 for c in out):continue
     common=set(range(4))
     for i in ids:common&=endpoints(out[i])
     if common:direct=True;break
    assert direct==indirect,(cols,ids)
    checks+=1
# Three triangle directions have graphic pair-sum extension but no star.
triangle=[1,2,3]
assert rank(triangle)==2 and extension(triangle,[([0,1,2],2)]) is None
assert all(c.bit_count()<=2 for c in triangle+[triangle[i]^triangle[j] for i,j in itertools.combinations(range(3),2)])
# Parallel duplicates must retain separate quota counts.
A=[1,1,2,4];groups=[([0,1,2,3],2)]
data=extension(A,groups);assert data and len(data[1][0])==3
edges=[(0,3),(0,3),(1,3),(2,3),(0,1),(0,2),(1,2)]
for target in range(8):
 result=solve_star_certificate(A,groups,target,4,edges)
 expected=[]
 for mask in range(16):
  s=0
  for i,a in enumerate(A):
   if mask>>i&1:s^=a
  if s==target and mask.bit_count()<=2:expected.append(mask)
 assert (result is None)==(not expected)
 if result is not None:assert result in expected
out={'rank3_common_star_vs_extension_plus_independence_checks':checks,'triangle_independence_check_required':True,'parallel_duplicate_quota_all8_targets':True}
Path(__file__).with_name('results.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
