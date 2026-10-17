import itertools,json
from pathlib import Path
out=Path(__file__).parent
V=[0,3,5,6];T=[1,2,4,7];full=15
relations=[(a,b) for a in range(16) for b in range(16) if a&b==a]
Fs=[];Ws=[]
for mid in range(1<<14):
 F=(mid<<1)|(1<<15)
 if not all(not(F>>a&1) or F>>b&1 for a,b in relations):continue
 Fs.append(F)
 if any(all(F>>sum(1<<j for j,y in enumerate(V) if (y>>i&1)==(x>>i&1))&1 for i in range(3)) for x in T):Ws.append(F)
assert len(Fs)==166 and len(Ws)==68
weighted=[(sum(1<<S for S in range(1,16)),2)]
for x in T:
 neighbors=sum(1<<j for j,y in enumerate(V) if (x^y).bit_count()==1)
 F=sum(1<<S for S in range(16) if (S&neighbors).bit_count()>=2)
 assert F in Ws
 weighted.append((F,1))
def defeats(F,A,B):return bool(F>>A&1 and F>>B&1 and not(F>>(A&B)&1))
loads=[sum(w for F,w in weighted if defeats(F,A,B)) for A in range(16) for B in range(16)]
assert max(loads)==2 and sum(w for _,w in weighted)==6
cover=[(3,12),(13,14),(7,11)]
assert all(any(defeats(F,A,B) for A,B in cover) for F in Ws)
result={'semifilters':len(Fs),'above_some_target_filters':len(Ws),'all_ordered_pairs_checked':256,'dual_weight_denominator':2,'weighted_filters':weighted,'maximum_scaled_pair_load':max(loads),'total_scaled_dual_weight':6,'cover':cover,'exact_fractional_cover':3,'exact_integral_cover':3}
(out/'parity3_verified.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
