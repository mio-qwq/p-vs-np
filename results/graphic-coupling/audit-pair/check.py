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
def app(bs,x):
 y=0
 for i,b in enumerate(bs):
  if x>>i&1:y^=b
 return y
def ends(x,r):
 s={i for i in range(r) if x>>i&1}
 if len(s)==1:s.add(r)
 return s
maps=[bs for bs in product(range(1,4),repeat=2) if rank(bs)==2]
count=0
for n in range(2,7):
 pairs=[(i,i+1) for i in range(0,n-1,2)]
 for cols in product(range(1,4),repeat=n):
  if rank(cols)!=2:continue
  ext=list(cols)+[cols[i]^cols[j] for i,j in pairs if cols[i]!=cols[j]]
  direct=any(all(ends(app(bs,cols[i]),2)&ends(app(bs,cols[j]),2) for i,j in pairs) for bs in maps)
  graphic=any(all(app(bs,c).bit_count()<=2 for c in ext) for bs in maps)
  assert direct==graphic
  count+=1
rng=Random(42)
for _ in range(500):
 n=rng.randrange(1,9);cols=[rng.randrange(8) for _ in range(n)];pairs=[(i,i+1) for i in range(0,n-1,2)]
 original={app(cols,x) for x in range(1<<n) if all(not(x>>i&1 and x>>j&1) for i,j in pairs)}
 reduced={app(cols,x) for x in range(1<<n) if all(not(x>>i&1) for i,c in enumerate(cols) if c==0) and all(not(x>>i&1 and x>>j&1) for i,j in pairs)}
 assert original==reduced
# Rectangular redundant row presentation: map rank3 graph syndromes into five rows.
B=[1,2,3,4,5,6];U=[0b10001,0b01010,0b00111];assert rank(U)==3
A=[app(U,c) for c in B]
for z in range(64):
 b=app(A,z);t=app(B,z)
 for x in range(64):assert (app(A,x)==b)==(app(B,x)==t)
print('PASS',count,'rank-two localization/extension checks with parallel columns; 500 zero-preprocessing checks; 4096 rectangular target-fiber checks')
