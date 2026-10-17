import itertools as it,json
from collections import Counter
stats=Counter();cases=[]
def edge(u,v):return tuple(sorted((u,v)))
def matchings(vs):
 if not vs:yield frozenset();return
 a=vs[0]
 for b in vs[1:]:
  for m in matchings(tuple(v for v in vs[1:] if v!=b)):yield m|{edge(a,b)}
def pf(B,S):
 if not S:return 1
 a=S[0];v=0
 for b in S[1:]:
  if B[a][b]:v^=pf(B,tuple(i for i in S[1:] if i!=b))
 return v

def distance(M,n):
 mate={a:b for e in M for a,b in (e,e[::-1])}
 unseen=set(range(2*n));components=0
 while unseen:
  start=min(unseen);v=start;components+=1
  while True:
   w=mate[v];unseen.discard(v);unseen.discard(w);v=w^1
   if v==start:break
 return n-components
for n in range(2,7):
 ms=list(matchings(tuple(range(2*n))))
 for d in range(1,5):
  radius=min(n-1,2*d);seen=[]
  for M in ms:
   B=[[0]*n for _ in range(n)]
   for u,v in M:
    i,j=u//2,v//2
    if i!=j:B[i][j]^=1;B[j][i]^=1
   if n==2:
    value=int((0,2) in M);kind='single edge'
   elif n>=2*d+1:
    value=pf(B,tuple(range(2*d)));kind='Pfaffian'
   elif n%2:
    value=pf(B,tuple(range(n-1)));kind='Pfaffian'
   else:
    value=B[0][1]*pf(B,tuple(range(2,n)));kind='entry times Pfaffian'
   dist=distance(M,n)
   if dist<radius:assert value==0,(n,d,M)
   if value:seen.append(dist)
   stats['polynomial_evaluations']+=1
  assert seen and min(seen)==radius
  cases.append(dict(n=n,d=d,kind=kind,minimum_nonzero_distance=min(seen)))
  stats['parameter_cases']+=1
print(json.dumps(dict(stats),indent=2));print(json.dumps(cases,indent=2));print('PASS')
from collections import deque
bfs_cases=0
for n in range(1,6):
 baseline=frozenset((2*i,2*i+1) for i in range(n));D={baseline:0};Q=deque([baseline])
 while Q:
  M=Q.popleft();assert D[M]==distance(M,n);bfs_cases+=1
  for e,f in it.combinations(M,2):
   a,b=e;c,d=f
   for new in ({edge(a,c),edge(b,d)},{edge(a,d),edge(b,c)}):
    N=(M-{e,f})|new
    if N not in D:D[N]=D[M]+1;Q.append(N)
 assert len(D)==len(list(matchings(tuple(range(2*n)))))
print('Exact flip-graph BFS comparisons:',bfs_cases);print('BFS PASS')
