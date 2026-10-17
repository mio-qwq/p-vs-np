from itertools import product,combinations
from random import Random

def rank(xs):
 p={}
 for x in xs:
  while x:
   i=x.bit_length()-1
   if i in p:x^=p[i]
   else:p[i]=x;break
 return len(p)
def apply(bs,x):
 y=0
 for i,b in enumerate(bs):
  if x>>i&1:y^=b
 return y
def ends(x):
 s={i for i in range(3) if x>>i&1}
 if len(s)==1:s.add(3)
 return s
maps=[bs for bs in product(range(1,8),repeat=3) if rank(bs)==3]
rng=Random(20261017);checks=0
for case in range(700):
 n=rng.randrange(1,10);A=[rng.randrange(1,8) for _ in range(n)]
 ids=list(range(n));rng.shuffle(ids);groups=[]
 while ids:
  k=rng.randrange(1,min(4,len(ids))+1);groups.append(ids[:k]);ids=ids[k:]
 if case%3==0:groups.append([])
 ext=A[:];independent=True
 for g in groups:
  cols=set(A[i] for i in g)
  independent &= rank(cols)==len(cols)
  ext += [a^b for a,b in combinations(cols,2)]
 indirect=independent and any(all(apply(bs,a).bit_count()<=2 for a in ext) for bs in maps)
 direct=False
 for bs in maps:
  out=[apply(bs,a) for a in A]
  if any(a.bit_count()>2 for a in out):continue
  ok=True
  for g in groups:
   common=set(range(4))
   for i in g:common &= ends(out[i])
   ok &= bool(common)
  if ok:direct=True;break
 assert direct==indirect,(A,groups,direct,indirect)
 checks+=1
print('PASS:',checks,'simultaneous multi-group tests with repetitions and empty groups')
