from itertools import chain

def matchings(v):
 if not v: yield ();return
 a=v[0]
 for j in range(1,len(v)):
  for m in matchings(v[1:j]+v[j+1:]): yield ((a,v[j]),)+m

def distance(m,n):
 adj=[[] for _ in range(n)]
 for a,b in m:
  if a//2!=b//2:adj[a//2].append(b//2);adj[b//2].append(a//2)
 seen=set();out=0
 for a in range(n):
  if a in seen or not adj[a]:continue
  stack=[a];s=set()
  while stack:
   x=stack.pop()
   if x in s:continue
   s.add(x);stack+=adj[x]
  seen|=s;out+=len(s)-1
 return out

def value(m,d):
 s=set(m);v=1
 for i in range(d):v*=int((4*i,4*i+2) in s)-int((4*i+1,4*i+3) in s)
 return v
for d,n in [(1,3),(1,4),(2,4),(2,5),(2,6),(3,6),(3,7)]:
 total=0;minimum=999
 for m in matchings(tuple(range(2*n))):
  total+=1
  if value(m,d):minimum=min(minimum,distance(m,n))
 assert minimum==(3*d+1)//2,(d,n,minimum)
 print(d,n,total,minimum)
print('PASS: integer evaluations imply same nonzero set over every field')
