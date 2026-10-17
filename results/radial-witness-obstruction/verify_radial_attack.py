from fractions import Fraction as Q
from math import comb
from pathlib import Path
import json
out=Path(__file__).parent
reports=[]
def syndrome(y,m):
 s=0
 for i in range(m):
  if y>>i&1:s^=i
 return s
for m in (2,4,8):
 V=[y for y in range(1<<m) if y.bit_count()%2==0]
 T=[x for x in range(1<<m) if x.bit_count()%2==1]
 C=[{y for y in V if syndrome(y,m)==j} for j in range(m)]
 pairs=[];q=1
 while q<m:
  pairs.append((set(V)-set.union(*C[:q]),set(V)-set.union(*C[q:2*q])))
  q*=2
 checks=0
 for x in T:
  neighbors={x^(1<<i) for i in range(m)}
  assert all(len(neighbors&c)==1 for c in C)
  A,B=pairs[0]
  assert len(neighbors&A)==m-1 and len(neighbors&B)==m-1 and len(neighbors&A&B)==m-2
  # Two nontrivial mixtures over all odd spheres, not only a single sphere.
  for profile in (lambda d:1,lambda d:d+1):
   raw={d:profile(d) for d in range(1,m,2)};Z=sum(raw.values())
   weights={y:Q(raw[(x^y).bit_count()],Z*comb(m,(x^y).bit_count())) for y in V}
   mass=lambda S:sum((weights[y] for y in S),Q(0))
   assert mass(V)==1 and all(mass(c)==Q(1,m) for c in C)
   p=1-sum(Q(d*w,Z*m) for d,w in raw.items())
   assert all(mass({y for y in V if (x>>i&1)==(y>>i&1)})==p for i in range(m))
   thresholds={p,p/2,Q(1,2*m)}|{1-Q(q,m) for q in range(1,m) if 0<1-Q(q,m)<=p}
   for tau in thresholds:
    assert 0<tau<=p
    assert any(mass(A)>=tau and mass(B)>=tau and mass(A&B)<tau for A,B in pairs)
    checks+=1
 reports.append({'dimension':m,'positive_vertices':len(T),'fixed_pairs':len(pairs),'mixture_threshold_checks':checks,'every_neighbor_class_exactly_one':True})
(out/'radial_attack_verified.json').write_text(json.dumps(reports,indent=2)+'\n')
print(json.dumps(reports))
