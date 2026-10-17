import itertools as it,json
from collections import Counter
stats=Counter();cases=[]
def edge(u,v):return tuple(sorted((u,v)))
def matchings(vs):
 if not vs:yield frozenset();return
 a=vs[0]
 for b in vs[1:]:
  for m in matchings(tuple(v for v in vs[1:] if v!=b)):yield m|{edge(a,b)}
def haf(B,S):
 if not S:return 1
 a=S[0]
 return sum(B[a][b]*haf(B,tuple(i for i in S[1:] if i!=b)) for b in S[1:])
for n in range(2,7):
 ms=list(matchings(tuple(range(2*n))))
 for d in range(1,5):
  radius=min(n,2*d+1);seen=[];values=Counter()
  for M in ms:
   changed={i for i in range(n) if edge(2*i,2*i+1) not in M}
   if n<=2*d and n%2==0:
    chosen={edge(4*i,4*i+2) for i in range(n//2)}
    value=int(chosen<=M);kind='monomial'
   else:
    s=2*d if n>=2*d+1 else n-1
    S=tuple(range(s));a=0;B=[[0]*n for _ in range(n)]
    for u,v in M:
     i,j=u//2,v//2
     if i==j:continue
     weight=1
     if i==a:weight=1 if u%2==0 else -1
     if j==a:weight=1 if v%2==0 else -1
     B[i][j]+=weight;B[j][i]+=weight
    value=haf(B,S);kind='signed hafnian'
   if len(changed)<radius:assert value==0,(n,d,M,value)
   if value:seen.append(len(changed));values[value]+=1
   stats['integer_polynomial_evaluations']+=1
  assert seen and min(seen)==radius
  assert values[1]+values[-1]>0
  cases.append(dict(n=n,d=d,kind=kind,minimum_nonzero_support=min(seen),values=dict(values)))
  stats['parameter_cases']+=1
print(json.dumps(dict(stats),indent=2));print(json.dumps(cases,indent=2));print('PASS')
# Check the actual-edge expansion and sign-reversing involution, including s=n.
involution_inputs=involution_terms=0
for n in range(2,7):
 for s in range(2,n+1,2):
  S=set(range(s));a=0
  for M in matchings(tuple(range(2*n))):
   changed={i for i in range(n) if (2*i,2*i+1) not in M}
   if changed!=S:continue
   involution_inputs+=1
   active={e for e in M if e[0]//2 in S}
   reach={a}
   while True:
    enlarged=reach|{v//2 for e in active if any(u//2 in reach for u in e) for v in e}
    if enlarged==reach:break
    reach=enlarged
   component={e for e in active if e[0]//2 in reach}
   terms=[]
   for q in it.combinations(active,s//2):
    indices=[v//2 for e in q for v in e]
    if len(set(indices))==s:terms.append(frozenset(q))
   terms=set(terms)
   def sign(q):
    port=next(v%2 for e in q for v in e if v//2==a)
    return 1 if port==0 else -1
   for q in terms:
    partner=q^component
    assert partner!=q and partner in terms
    assert partner^component==q
    assert sign(partner)==-sign(q)
    involution_terms+=1
   assert sum(sign(q) for q in terms)==0
print('Involution inputs:',involution_inputs,'paired expanded terms:',involution_terms)
print('INVOLUTION PASS')
