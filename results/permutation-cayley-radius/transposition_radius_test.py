import itertools, collections

def pf(p, ids):
 if not ids:return 1
 i=ids[0];answer=0
 for jpos in range(1,len(ids)):
  j=ids[jpos];a=int(p[i]==j)-int(p[j]==i)
  if a:
   answer += (-1)**(jpos+1)*a*pf(p,ids[1:jpos]+ids[jpos+1:])
 return answer

def distance(p):
 seen=set();nc=0
 for a in range(len(p)):
  if a in seen:continue
  nc+=1
  while a not in seen:seen.add(a);a=p[a]
 return len(p)-nc

for n in range(2,9):
 hist=collections.Counter();cnt=0
 for p in itertools.permutations(range(n)):
  dist=distance(p)
  if n==2:q=int(p[0]==1)
  elif n%2:q=pf(p,tuple(range(1,n)))
  else:q=(int(p[0]==1)-int(p[1]==0))*pf(p,tuple(range(2,n)))
  expected=dist==n-1 and (n%2 or n==2 or p[0]==1 or p[1]==0)
  assert bool(q)==expected,(n,p,q,expected)
  assert q in (-1,0,1)
  hist[q]+=1
  # General minor lower bound for every d that fits in n.
  for d in range(1,(n-1)//2+1):
   qd=pf(p,tuple(range(2*d)))
   if qd:assert dist>=2*d,(n,d,p,qd,dist)
   cnt+=1
 print({'n':n,'extremal_values':dict(hist),'minor_checks':cnt},flush=True)
