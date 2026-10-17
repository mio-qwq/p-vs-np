from itertools import permutations,combinations,product
from functools import lru_cache
import sys,random,platform,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from solver import solve
print('Python',sys.version,'platform',platform.platform(),flush=True)
def cycles(p):
 seen=set(); out=[]
 for i in range(len(p)):
  if i in seen:continue
  c=[];j=i
  while j not in seen:seen.add(j);c.append(j);j=p[j]
  if len(c)>1:out.append(c)
 return out
def stat(p):
 c=cycles(p);return sum(map(len,c)),len(c)
def pairs(p):
 cs=cycles(p); ps=[];left=[]
 for c in cs:
  ps.extend((c[i],c[i+1],True) for i in range(0,len(c)-1,2))
  if len(c)%2:left.append(c[-1])
 ps.extend((left[i],left[i+1],False) for i in range(0,len(left)-1,2))
 return ps
cnt=0
for n in range(2,9):
 for p in permutations(range(n)):
  st=stat(p);ps=pairs(p);assert len(ps)==st[0]//2
  assert len({v for a,b,_ in ps for v in (a,b)})==2*len(ps)
  for mask in range(1,1<<len(ps)):
   q=list(p);internal=False;cross=0
   for j,(a,b,t) in enumerate(ps):
    if mask>>j&1:q[a],q[b]=q[b],q[a];internal|=t;cross+=not t
   qs=stat(q)
   assert qs<st,(p,ps,mask,q,st,qs)
   if internal:assert qs[0]<st[0]
   else:assert qs==(st[0],st[1]-cross)
   cnt+=1
 print('cube n',n,'cumulative subsets',cnt,flush=True)
def pf(A):
 if not A:return 1
 return sum((-1)**(j+1)*A[0][j]*pf(tuple(tuple(A[a][b] for b in range(len(A)) if b not in (0,j)) for a in range(len(A)) if a not in (0,j))) for j in range(1,len(A)))
pfc=0
for n in range(3,9):
 for d in range(1,(n-1)//2+1):
  seen=False
  for p in permutations(range(n)):
   A=tuple(tuple(int(p[a]==b)-int(p[b]==a) for b in range(2*d)) for a in range(2*d))
   v=pf(A)
   if stat(p)[0]<=2*d:assert v==0,(n,d,p,v)
   if abs(v)==1:seen=True
   pfc+=1
  assert seen
 print('Pfaffian n',n,'cumulative',pfc,flush=True)
# Check the integer Boolean finite difference for EVERY monomial of total degree <=d.
fdc=0
for d in range(1,7):
 m=d+1
 for exps in product(range(d+1),repeat=m):
  if sum(exps)>d:continue
  val=sum((-1)**(m-sum(bits))*__import__('math').prod(b**e for b,e in zip(bits,exps)) for bits in product((0,1),repeat=m))
  assert val==0;fdc+=1
print('integer finite-difference monomials',fdc,flush=True)
rng=random.Random(20261017);sc=0
for n in range(0,8):
 ps=list(permutations(range(n)))
 for k in range(0,5):
  for trial in range(25):
   a=[[rng.randrange(1<<k) for j in range(n)] for i in range(n)]
   def value(p):
    v=0
    for i,j in enumerate(p):v^=a[i][j]
    return v
   targets={value(p) for p in ps}
   for t in range(1<<k):
    p=solve(a,k,t)
    assert (p is not None)==(t in targets),(n,k,a,t)
    if p is not None:assert sorted(p)==list(range(n)) and value(p)==t and stat(p)[0]<=min(n,2*k+1)
    sc+=1
 print('solver n',n,'cumulative calls',sc,flush=True)
print('PASS',cnt,pfc,fdc,sc,flush=True)
