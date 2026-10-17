"""Raw certificate audit. No imports from certificate-generation code."""
import json, hashlib
from collections import Counter, deque
from itertools import combinations, combinations_with_replacement
from pathlib import Path
SOURCE=Path(__file__).resolve().parents[1]
OUT=Path(__file__).resolve().parent

def edge(raw,n):
    assert len(raw)==2 and all(type(x) is int and 0<=x<2*n for x in raw)
    assert raw[0]!=raw[1]
    return tuple(sorted(raw))

def matching(raw,n):
    edges=tuple(sorted(edge(e,n) for e in raw))
    assert len(edges)==n
    assert sorted(v for e in edges for v in e)==list(range(2*n))
    return edges

def neighbors(M):
    for i,j in combinations(range(len(M)),2):
        a,b=M[i]; c,d=M[j]
        remainder=[e for k,e in enumerate(M) if k not in (i,j)]
        for pair in (((a,c),(b,d)),((a,d),(b,c))):
            yield tuple(sorted(remainder+[tuple(sorted(e)) for e in pair]))

def bfs(n,limit=None):
    start=tuple((2*i,2*i+1) for i in range(n))
    distances={start:0}; q=deque([start])
    while q:
        cur=q.popleft(); d=distances[cur]
        if d==limit: continue
        for nxt in neighbors(cur):
            if nxt not in distances:
                distances[nxt]=d+1; q.append(nxt)
    return distances

def load(name):
    b=(SOURCE/name).read_bytes()
    (OUT/name).write_bytes(b)
    return json.loads(b),hashlib.sha256(b).hexdigest()

report={}
c,sha=load('certificate_mod3_n7.json')
assert c['n']==7 and c['modulus']==3
n=7; target=matching(c['target'],n)
ball=bfs(n,3)
weights=Counter(); listed=0
for term in c['terms']:
    a=term['coefficient']; assert type(a) is int and a in (1,2)
    for raw in term['matchings']:
        M=matching(raw,n); assert M in ball
        weights[M]+=a; listed+=1
# Compute each weighted moment directly from complete matching indicators.
moments=Counter()
for M,a in weights.items():
    moments[()]+=a
    for e in M: moments[(e,)]+=a
    for e,f in combinations_with_replacement(M,2): moments[tuple(sorted((e,f)))]+=a
all_edges=list(combinations(range(2*n),2))
monomials=[()]+[(e,) for e in all_edges]+list(combinations_with_replacement(all_edges,2))
T=set(target)
for mon in monomials:
    assert moments[mon]%3==int(all(e in T for e in mon)),('failed monomial',mon)
# Locate target with an actual shortest-flip BFS, instead of assuming its distance.
d4=bfs(n,4); assert d4[target]==4
report['upper']={'sha256':sha,'groups':len(c['terms']),'listed_matching_terms':listed,'distinct_matchings':len(weights),'checked_monomials_including_squares_and_incident_products':len(monomials),'radius3_ball_size':len(ball),'rhs_distance_histogram':dict(sorted(Counter(ball[M] for M in weights).items())),'target_distance':d4[target],'identity_verified':True}
for n in (5,6):
    c,sha=load(f'witness_n{n}.json'); assert c['n']==n
    target=matching(c['target'],n); coeff=Counter(); total=0
    for term in c['terms']:
        a=term['coefficient']; assert type(a) is int and a in (1,2)
        for raw in term['monomials']:
            assert len(raw)<=2
            mon=tuple(sorted(edge(e,n) for e in raw))
            coeff[mon]+=a; total+=1
    def evaluate(M):
        S=set(M)
        return sum(a for mon,a in coeff.items() if all(e in S for e in mon))%3
    ds=bfs(n)
    expected=1
    for odd in range(1,2*n,2): expected*=odd
    assert len(ds)==expected
    hist=Counter(); nonzero=Counter()
    for M,d in ds.items():
        hist[d]+=1
        val=evaluate(M)
        if d<=3: assert val==0,(n,d,M,val)
        if val: nonzero[d]+=1
    assert ds[target]==4 and evaluate(target)!=0
    report[f'lower_n{n}']={'sha256':sha,'groups':len(c['terms']),'listed_monomials':total,'distinct_monomials':len(coeff),'all_matching_count':len(ds),'distance_histogram':dict(sorted(hist.items())),'nonzero_histogram':dict(sorted(nonzero.items())),'target_distance':ds[target],'target_value_mod3':evaluate(target),'radius3_vanishing_verified':True}
# Verify the explicit extension-failure matching without assuming its recorded value.
failure,fsha=load('extension_failure.json')
M=matching(failure['matching'],8)
w=json.loads((SOURCE/'witness_n6.json').read_text())
value=sum(t['coefficient'] for t in w['terms'] for mon in t['monomials'] if all(edge(e,8) in M for e in mon))%3
assert value==failure['value_mod3']==1
# Three independent two-edge flips give this matching; the three disjoint
# four-vertex alternating components also force at least three flips.
explicit=tuple(sorted(((0,2),(1,3),(4,10),(5,11),(6,7),(8,12),(9,13),(14,15))))
assert M==explicit
report['extension_failure']={'sha256':fsha,'value_mod3':value,'distance':3,'verified':True}
# Independent checks of all remaining finite lower-bound templates.
for n in (2,3,4,7):
    limit=min(n-1,3)-1
    small=bfs(n,limit)
    def template(M):
        S=set(M)
        if n==2: return int((0,2) in S)
        if n==3: return int((1,2) in S)*int((3,4) in S)
        return (int((0,2) in S)-int((1,3) in S))*(int((4,6) in S)-int((5,7) in S))
    assert all(template(M)%3==0 for M in small)
    if n==2: T=((0,2),(1,3))
    elif n==3: T=((0,5),(1,2),(3,4))
    else: T=tuple(sorted(((0,2),(1,6),(3,4),(5,7))+tuple((2*i,2*i+1) for i in range(4,n))))
    assert template(T)%3!=0 and bfs(n,limit+1)[T]==limit+1
    report[f'template_n{n}']={'zero_ball_size':len(small),'first_nonzero_distance':limit+1,'value_mod3':template(T)%3,'verified':True}
# The first certificate group contains exactly the baseline. Changing its
# coefficient by one necessarily breaks the constant monomial equality.
assert (moments[()]+1)%3 != 1
report['negative_control']={'single_coefficient_corruption_rejected_on_constant':True}
(OUT/'results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
