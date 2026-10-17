import itertools,json,random
from pathlib import Path

def rank(cols):
 piv={}
 for x in cols:
  while x:
   i=x.bit_length()-1
   if i in piv:x^=piv[i]
   else:piv[i]=x;break
 return len(piv)
def apply(basis,x):
 y=0
 for i,b in enumerate(basis):
  if x>>i&1:y^=b
 return y

def GL(r):return [bs for bs in itertools.product(range(1,1<<r),repeat=r) if rank(bs)==r]
def endpoints(x,r):
 s={i for i in range(r) if x>>i&1}
 if len(s)==1:s.add(r)
 return s

def direct_localizer(cols,pairs,r,maps):
 for B in maps:
  out=[apply(B,x) for x in cols]
  if all(1<=x.bit_count()<=2 for x in out) and all(endpoints(out[i],r)&endpoints(out[j],r) for i,j in pairs):return B,out
 return None

def extended_graphic(cols,pairs,r,maps):
 ext=cols+[cols[i]^cols[j] for i,j in pairs]
 for B in maps:
  out=[apply(B,x) for x in ext]
  if all(x.bit_count()<=2 for x in out):return B,out
 return None
r=3;maps=GL(r);checks=0
for size in range(3,8):
 for cols in itertools.combinations(range(1,8),size):
  if rank(cols)!=r:continue
  pairsets=[[]]+[[(i,j)] for i,j in itertools.combinations(range(size),2)]
  pairsets += [[(a,b),(c,d)] for a,b,c,d in itertools.permutations(range(size),4) if a<b and c<d and a<c]
  for pairs in pairsets:
   direct=direct_localizer(list(cols),pairs,r,maps)
   ext=extended_graphic(list(cols),pairs,r,maps)
   assert bool(direct)==bool(ext),(cols,pairs)
   checks+=1
# K4 includes all six unit/pair columns; opposite pair3,4 appendsmissing111.
k4=[1,2,3,4,5,6];pair=[(2,3)]
assert k4[pair[0][0]]^k4[pair[0][1]]==7
assert direct_localizer(k4,pair,3,maps) is None
assert extended_graphic(k4,pair,3,maps) is None
# A genuine rescued presentation: opposite edges of a four-cycle.
c4=[3,6,4,1];pairs=[(0,2),(1,3)]
assert all(not(endpoints(c4[i],3)&endpoints(c4[j],3)) for i,j in pairs)
rescue=extended_graphic(c4,pairs,3,maps);assert rescue
B,out=rescue;out=out[:4]
assert all(endpoints(out[i],3)&endpoints(out[j],3) for i,j in pairs)
# Every target fiber is preserved by the explicit invertible row map.
for b in range(8):
 for x in range(16):
  syndrome=0;newsyndrome=0
  for i in range(4):
   if x>>i&1:syndrome^=c4[i];newsyndrome^=out[i]
  assert (syndrome==b)==(newsyndrome==apply(B,b))
result={'GL3_maps':len(maps),'exhaustive_rank3_localization_vs_extension_checks':checks,'K4_opposite_pair':'no representation; extension all seven nonzero columns (Fano)','C4_two_opposite_pairs_rescue':{'original_columns':c4,'pairs':pairs,'row_map_images_of_units':B,'new_columns':out,'all_128_target_assignment_fibers_checked':True},'recognizer_used':'exhaustive GL3 oracle for validation only; polynomial theorem invokes known graphic recognition'}
Path(__file__).with_name('results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
