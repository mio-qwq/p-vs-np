from itertools import combinations
from fractions import Fraction
import json
V=tuple(x for x in range(16) if x.bit_count()%2==0)
P=tuple(x for x in range(16) if x.bit_count()%2==1)
sets=[{V[i] for i in range(8) if a>>i&1} for a in range(256)]
filters=[]; weights=[]
for x in P:
 blocks=[{y for y in V if (x>>i&1)==(y>>i&1)} for i in range(4)]
 filters.append([any(b<=s for b in blocks) for s in sets]);weights.append(24)
for triple in combinations(V,3):
 if any(a^b==15 for a,b in combinations(triple,2)):continue
 filters.append([len(set(triple)&s)>=2 for s in sets]);weights.append(15)
for a,b in combinations(V,2):
 if (a^b).bit_count()!=2:continue
 r=set(V)-{a,b};filters.append([bool(r&s) for s in sets]);weights.append(10)
assert len(filters)==64 and sum(weights)==912
for f in filters:
 assert not f[0] and f[255]
 for a in range(256):
  if f[a]:
   for i in range(8):assert f[a|1<<i]
 assert any(all(f[sum(1<<j for j,y in enumerate(V) if (x>>i&1)==(y>>i&1))] for i in range(4)) for x in P)
acc=[sum(1<<j for j,f in enumerate(filters) if f[a]) for a in range(256)]
class_masks=[(1<<8)-1,((1<<32)-1)<<8,((1<<24)-1)<<40]
maxload=0
for a in range(256):
 for b in range(256):
  killed=acc[a]&acc[b]&~acc[a&b]
  load=sum(w*(killed&m).bit_count() for w,m in zip([24,15,10],class_masks))
  assert load<=240,(a,b,load)
  maxload=max(maxload,load)
assert maxload==240
print(json.dumps({'filters':64,'ordered_pairs':65536,'exact_dual':str(Fraction(sum(weights),240)),'integer_lower_bound':4,'max_scaled_load':maxload,'status':'PASS'}))
