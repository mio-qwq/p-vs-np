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
for n in range(2,7):
 ms=list(matchings(tuple(range(2*n))))
 for d in range(1,5):
  radius=min(n,2*d+1);seen=[]
  for M in ms:
   changed={i for i in range(n) if edge(2*i,2*i+1) not in M}
   if n<=2*d and n%2==0:
    chosen={edge(4*i,4*i+2) for i in range(n//2)}
    value=int(chosen<=M);kind='monomial'
   else:
    s=2*d if n>=2*d+1 else n-1
    S=tuple(range(s));B=[[0]*n for _ in range(n)]
    for u,v in M:
     i,j=u//2,v//2
     if i!=j:B[i][j]^=1;B[j][i]^=1
    assert all(sum(row)%2==0 for row in B)
    value=pf(B,S);kind='Pfaffian'
   if len(changed)<radius:assert value==0,(n,d,M)
   if value:seen.append(len(changed))
   stats['polynomial_evaluations']+=1
  assert seen and min(seen)==radius
  cases.append(dict(n=n,d=d,kind=kind,minimum_nonzero_support=min(seen)))
  stats['parameter_cases']+=1
# K2 exception and zero-degree cases are logically constant restrictions.
assert list(matchings((0,1)))==[frozenset({(0,1)})]
print(json.dumps(dict(stats),indent=2));print(json.dumps(cases,indent=2));print('PASS')
