from fractions import Fraction
from pathlib import Path
from math import comb
import json,itertools
OUT=Path(__file__).parent
V=[0,3,5,6];T=[1,2,4,7]
weights={65534:Fraction(1),59624:Fraction(1,2),61064:Fraction(1,2),64160:Fraction(1,2),64704:Fraction(1,2)}
cover=[(3,12),(13,14),(7,11)]
def valid(F):
 return not(F&1) and (F>>15)&1 and all(not(F>>A&1) or(F>>B&1) for A in range(16) for B in range(16) if A&B==A)
def above(F,x):
 return all(F>>sum(1<<j for j,y in enumerate(V) if (x>>i&1)==(y>>i&1))&1 for i in range(3))
def hit(F,A,B):return (F>>A&1) and(F>>B&1) and not(F>>(A&B)&1)
Fs=[F for F in range(1<<16) if valid(F)]
Ws=[F for F in Fs if any(above(F,x) for x in T)]
assert len(Fs)==166 and len(Ws)==68
assert all(F in Ws for F in weights)
loads=[sum(w for F,w in weights.items() if hit(F,A,B)) for A in range(16) for B in range(16)]
assert max(loads)==1 and sum(weights.values())==3
assert all(any(hit(F,A,B) for A,B in cover) for F in Ws)
# Verify symmetry counts by direct enumeration of odd-size coordinate subsets.
# An odd subset of all F2^r labels has each XOR value equally often.
rows=[]
for m in [2,4,8,16]:
 counts={d:[0]*m for d in range(1,m,2)}
 for bits in range(1<<m):
  d=bits.bit_count()
  if d%2==0:continue
  sigma=0
  for i in range(m):
   if bits>>i&1:sigma^=i
  counts[d][sigma]+=1
 for d,C in counts.items():assert C==[comb(m,d)//m]*m
 # All distinct threshold behaviours of each uniform sphere; exact rational.
 checks=0
 for d in range(1,m,2):
  B=comb(m,d);max_t=B*(m-d)//m
  for t in range(1,max_t+1):
   tau=Fraction(t,B);h=m*(1-tau)
   q=1
   while 2*q<=h:q*=2
   assert q<=m//2
   assert 1-Fraction(q,m)>=tau>1-Fraction(2*q,m)
   checks+=1
 rows.append({'m':m,'odd_spheres':len(counts),'coordinate_subsets_enumerated':1<<m,'integer_sphere_thresholds_checked':checks,'syndrome_counts':counts})
# m=4 explicit one-pair attack on every radius-one threshold witness.
m=4;negative=[x for x in range(16) if x.bit_count()%2==0];positive=[x for x in range(16) if x.bit_count()%2==1]
C0={0,15};C1={3,12};A=set(negative)-C0;B=set(negative)-C1
for x in positive:
 N={x^(1<<i) for i in range(4)}
 assert len(N&A)==len(N&B)==3 and len(N&A&B)==2
report={'status':'all exact checks passed','parity3':{'all_semifilters':len(Fs),'above_target_filters':len(Ws),'ordered_pairs_checked':256,'dual_total':'3','maximum_pair_dual_load':'1','upper_cover':cover,'exact_pair_cover_number':3},'radial_syndrome_tests':rows,'explicit_m4':{'negative':negative,'excluded_from_A':sorted(C0),'excluded_from_B':sorted(C1),'positive_witnesses_defeated':8},'scope':'parity3 exact unrestricted cover; logarithmic upper cover only for radial threshold subclass, not unrestricted parity covers'}
(OUT/'certificate_results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='radial_syndrome_tests'},indent=2))
print('radial checks',[(r['m'],r['integer_sphere_thresholds_checked']) for r in rows])
