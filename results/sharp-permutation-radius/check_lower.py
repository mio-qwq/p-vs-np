"""Integer arithmetic controls; the written proof covers arbitrary fields and n."""
from itertools import permutations
from math import factorial

def pf(A):
 if not A:return 1
 return sum((-1 if j%2==0 else 1)*A[0][j]*pf([[A[a][b] for b in range(1,len(A)) if b!=j] for a in range(1,len(A)) if a!=j]) for j in range(1,len(A)))
def skew_minor(p,S,sign=-1):
 return [[int(p[i]==j)+sign*int(p[j]==i) for j in S] for i in S]
def fullcycle(p):
 seen=set();j=0
 while j not in seen:seen.add(j);j=p[j]
 return len(seen)==len(p)
for n in (3,5,7):
 count=0
 for p in permutations(range(n)):
  v=pf(skew_minor(p,list(range(n-1))))
  assert (v!=0)==fullcycle(p)
  assert v in (-1,0,1)
  count+=v!=0
 assert count==factorial(n-1)
 print('odd sharpness',n,count)
for n in (2,4,6):
 count=0
 for p in permutations(range(n)):
  v=all(p[i]==i+1 for i in range(0,n,2))
  if v:assert all(p[i]!=i for i in range(n));count+=1
 assert count==factorial(n//2)
 print('even sharpness',n,count)
for p in permutations(range(6)):
 if sum(i!=j for i,j in enumerate(p))<=4:assert pf(skew_minor(p,[0,1,2,3]))==0
p=(1,2,3,4,0,5)
assert abs(pf(skew_minor(p,[0,1,2,3])))==1
# An incorrect symmetric + sign over characteristic zero fails the claimed vanishing.
p=(1,0,3,2,4)
assert pf(skew_minor(p,[0,1,2,3]))==0
assert pf(skew_minor(p,[0,1,2,3],sign=1))==4
print('extra fixed coordinate and wrong-sign controls passed')
