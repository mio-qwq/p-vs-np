from pathlib import Path
from fractions import Fraction
import itertools,json
OUT=Path(__file__).parent
V=[0,3,5,6,9,10,12,15];T=[x for x in range(16) if x.bit_count()%2];Q=256
matches={x:[sum(1<<j for j,y in enumerate(V) if ((x^y)>>i&1)==0) for i in range(4)] for x in T}
def makeF(pred):return sum(1<<S for S in range(Q) if pred(S))
canonical=[makeF(lambda S,x=x:any((S&B)==B for B in matches[x])) for x in T]
triples=[sum(1<<V.index(y) for y in R) for R in itertools.combinations(V,3) if all((a^b)!=15 for a,b in itertools.combinations(R,2))]
majorities=[makeF(lambda S,R=R:(S&R).bit_count()>=2) for R in triples]
excluded=[(a,b) for a,b in itertools.combinations(V,2) if (a^b).bit_count()==2]
hit_six=[makeF(lambda S,R=(255^(1<<V.index(a))^(1<<V.index(b))):bool(S&R)) for a,b in excluded]
assert len(canonical)==8 and len(majorities)==32 and len(hit_six)==24
classes=[canonical,majorities,hit_six];scaled_weights=[24,15,10]
for Fs in classes:
 for F in Fs:
  assert not(F&1) and F>>255&1
  assert all(not(F>>A&1) or(F>>B&1) for A in range(Q) for B in range(Q) if A&B==A)
  assert any(all(F>>B&1 for B in matches[x]) for x in T)
summary={i:{'maximum_scaled_load':0,'attaining_pair':None,'attaining_counts':None,'pairs_checked':0} for i in range(9)}
patterns=set();maxload=0
for A in range(Q):
 for B in range(A,Q):
  I=A&B
  counts=tuple(sum(bool(F>>A&1 and F>>B&1 and not(F>>I&1)) for F in Fs) for Fs in classes)
  load=sum(c*w for c,w in zip(counts,scaled_weights));assert load<=240
  t=I.bit_count();row=summary[t];row['pairs_checked']+=1
  if row['attaining_pair'] is None or load>row['maximum_scaled_load']:
   row.update(maximum_scaled_load=load,attaining_pair=(A,B),attaining_counts=counts)
  patterns.add(counts);maxload=max(maxload,load)
assert maxload==240
# General complementary-negative-pair lemma, exhaustive all 3-bit targets.
checks=0
for target_mask in range(1,255):
 TT=[x for x in range(8) if target_mask>>x&1];VV=[x for x in range(8) if not(target_mask>>x&1)]
 for y in VV:
  z=y^7
  if z not in VV or y>z:continue
  A=set(VV)-{y};B=set(VV)-{z}
  for x in TT:
   blocks=[{v for v in VV if ((v^x)>>i&1)==0} for i in range(3)]
   assert all(blocks)
   f=lambda S:any(C<=S for C in blocks)
   assert f(A) and f(B) and not f(A&B);checks+=1
report={'status':'exact integer certificate verified','m':4,'negative':V,'target':T,'families':[{'name':n,'count':len(Fs),'weight':str(Fraction(w,240))} for n,Fs,w in zip(['canonical','majority_on_nonantipodal_triple','hit_six_excluding_distance_two_pair'],classes,scaled_weights)],'dual_total':'19/5','integer_lower_bound':4,'all_unordered_pairs_checked':32896,'distinct_active_load_patterns':len(patterns),'load_certificate':'24 a + 15 b + 10 c <= 240 for every pair','by_intersection_size':summary,'complementary_pair_3bit_target_point_checks':checks,'scope':'finite lower bound for unrestricted parity4 cover; no equality upper bound or scalable claim'}
(OUT/'verified_certificate.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
