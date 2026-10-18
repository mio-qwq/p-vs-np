from itertools import combinations
from collections import Counter
import json

def mul(a,b):
 out=0
 while b:
  if b&1:out^=a
  b>>=1;a<<=1
  if a&32:a^=37
 return out
v=[]
for x in range(32):
 x2=mul(x,x); x3=mul(x2,x); x5=mul(x2,x3)
 v.append(x|(x3<<5)|(x5<<10))
count=0
for six in combinations(v,6):
 a,b,c,d,e,f=six
 assert a^b^c^d^e^f
 count+=1
columns=[sum(((x>>j)&1)<<i for i,x in enumerate(v)) for j in range(15)]
# enumerate every linear functional as XOR of evaluation columns, then complements
words=[0]
for c in columns:words += [w^c for w in words]
assert len(set(words))==32768
hist=Counter()
for w in words:
 hist[w.bit_count()]+=1;hist[32-w.bit_count()]+=1
assert hist=={0:1,8:620,12:13888,16:36518,20:13888,24:620,32:1}
assert count==906192
print(json.dumps({'status':'PASS','six_subsets':count,'affine_histogram':dict(sorted(hist.items()))},indent=2))
