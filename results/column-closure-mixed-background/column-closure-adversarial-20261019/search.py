from itertools import permutations
from math import comb
from fractions import Fraction

def mul(p,q):
 out=[0]*(len(p)+len(q)-1)
 for i,x in enumerate(p):
  for j,y in enumerate(q):out[i+j]+=x*y
 return out

def sign(p):return (-1)**sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))
def laplace(a,e,c,removed=frozenset()):
 out=[[0]*(1+sum(e)) for _ in a]
 counts=[0]*len(a)
 for p in permutations(range(len(a))):
  if any((r,j) in removed for r,j in enumerate(p)):continue
  s=p.index(c)
  counts[s]+=1
  term=[sign(p)]
  for r,j in enumerate(p):term=mul(term,[comb(e[j],k)*a[r]**(e[j]-k) for k in range(e[j]+1)])
  for k,x in enumerate(term):out[s][k]+=x
 return out,counts

if __name__=='__main__':
 a=(-3,-1,1,3);e=(0,1,2,4);c=1
 print('FULL',laplace(a,e,c))
 for d in range(4):
  if d==c:continue
  for r in range(4):
   T,counts=laplace(a,e,c,{(r,d)})
   val=[Fraction(t[1],768) for t in T]
   print('REMOVE',r,d,'VALUES',val,'MATCHINGS',counts)
   if min(val)<0:print('T=',T)
