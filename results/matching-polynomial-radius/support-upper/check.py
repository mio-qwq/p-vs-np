import itertools as it,json
from collections import Counter
stats=Counter()
def edge(u,v):return tuple(sorted((u,v)))
def matchings(vs):
 if not vs:yield frozenset();return
 a=vs[0]
 for b in vs[1:]:
  for m in matchings(tuple(v for v in vs[1:] if v!=b)):yield m|{edge(a,b)}
def cycles(M,n):
 mate={a:b for e in M for a,b in (e,e[::-1])}
 unseen={v for v in range(2*n) if mate[v]!=v^1};cs=[]
 while unseen:
  s=min(unseen);v=s;cyc=[]
  while True:
   w=mate[v];cyc.append((v,w));unseen.discard(v);unseen.discard(w)
   v=w^1
   if v==s:break
  cs.append(cyc)
 return cs
def measure(M,n):
 cs=cycles(M,n)
 return sum(map(len,cs)),len(cs)
for n in range(7):
 base={edge(2*i,2*i+1) for i in range(n)}
 for M in matchings(tuple(range(2*n))):
  stats['matchings']+=1
  cs=cycles(M,n);m=sum(map(len,cs));c=len(cs);switches=[];left=[]
  for cy in cs:
   for j in range(0,len(cy)-1,2):
    (a,b),(x,y)=cy[j:j+2]
    assert x==b^1
    switches.append(({edge(a,b),edge(x,y)},{edge(b,x),edge(a,y)},'internal'))
   if len(cy)%2:left.append(cy[-1])
  for j in range(0,len(left)-1,2):
   (a,b),(x,y)=left[j:j+2]
   switches.append(({edge(a,b),edge(x,y)},{edge(a,x),edge(b,y)},'cross'))
  assert len(switches)==m//2
  endpoints=[]
  for old,new,kind in switches:
   assert old<=M and not old&base
   assert len(new)==2 and not old&new
   endpoints.extend(v for e in old for v in e)
   if kind=='internal':assert new&base
   else:assert not new&base
  assert len(endpoints)==len(set(endpoints))
  for mask in range(1,1<<len(switches)):
   N=set(M);aff=Counter({e:1 for e in M});internal=False;crosses=0
   for j,(old,new,kind) in enumerate(switches):
    if mask>>j&1:
     N-=old;N|=new
     for e in old:aff[e]-=1
     for e in new:aff[e]+=1
     internal|=kind=='internal';crosses+=kind=='cross'
   assert sorted(v for e in N for v in e)==list(range(2*n))
   assert all(val==int(e in N) for e,val in aff.items())
   mm,cc=measure(N,n)
   if internal:assert mm<m
   else:assert mm==m and cc==c-crosses
   assert (mm,cc)<(m,c)
   stats['nonempty_cube_vertices']+=1
   stats['internal_vertices' if internal else 'cross_only_vertices']+=1
print(json.dumps(stats,indent=2));print('PASS')
