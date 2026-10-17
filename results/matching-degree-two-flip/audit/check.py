#!/usr/bin/env python3
"""Independent exhaustive verifier; imports only certificate data, no discovery code."""
import json, hashlib, itertools, collections, pathlib, copy
SRC=pathlib.Path(__file__).resolve().parents[1]
EXPECTED={'DEGREE_TWO_FLIP_RADIUS.md':'765cb35eb5830be5b2d97601abf38be465f87a2a457f0aa64905db69b2cf0fe8','orbit_certificate.json':'9ea13e4436d83da1942fd7b98156f93bc7a0a75ee570841c3eab388de02c263d'}
for fn,h in EXPECTED.items(): assert hashlib.sha256((SRC/fn).read_bytes()).hexdigest()==h

def canonical(edges): return tuple(sorted(tuple(sorted(e)) for e in edges))
def matchings(vertices):
    if not vertices:
        yield (); return
    a,*rest=vertices
    for b in rest:
        for tail in matchings([v for v in rest if v!=b]):
            yield canonical(((a,b),)+tail)
def baseline(n): return tuple((2*i,2*i+1) for i in range(n))
def distance_formula(M):
    # Count connected components of the UNION, including common-edge components.
    N=2*len(M); adj=[set() for _ in range(N)]
    for a,b in M+baseline(len(M)): adj[a].add(b); adj[b].add(a)
    unseen=set(range(N)); components=0
    while unseen:
        components+=1; stack=[unseen.pop()]
        while stack:
            for b in adj[stack.pop()]:
                if b in unseen: unseen.remove(b); stack.append(b)
    return len(M)-components

def bfs(n):
    B=baseline(n); D={B:0}; Q=collections.deque([B])
    while Q:
        M=Q.popleft()
        for i,j in itertools.combinations(range(n),2):
            a,b=M[i]; c,d=M[j]
            rest=[e for k,e in enumerate(M) if k not in (i,j)]
            for replacement in (((a,c),(b,d)),((a,d),(b,c))):
                T=canonical(rest+list(replacement))
                if T not in D: D[T]=D[M]+1; Q.append(T)
    return D
C=json.loads((SRC/'orbit_certificate.json').read_text()); n=5
all_M=set(matchings(list(range(10)))); D=bfs(n)
assert len(all_M)==945 and set(D)==all_M
assert all(D[M]==distance_formula(M) for M in all_M)
assert C['denominator']==48
T=canonical(C['target']); assert T in all_M and D[T]==4
weighted=[]
for term in C['terms']:
    assert type(term['coefficient']) is int
    for raw in term['matchings']:
        M=canonical(raw)
        assert len(M)==5 and M in all_M and D[M]<=3
        weighted.append((term['coefficient'],frozenset(M)))
assert len(C['terms'])==49 and len(weighted)==346
assert len({M for c,M in weighted})==346
E=list(itertools.combinations(range(10),2))
# Check ALL formal monomials, including repeated/incident-edge products.
monomials=[()]+[(e,) for e in E]+list(itertools.combinations_with_replacement(E,2))
assert len(monomials)==1081
T=frozenset(T)
def failures(W):
    return [mon for mon in monomials if 48*int(set(mon)<=T)!=sum(c for c,M in W if set(mon)<=M)]
assert not failures(weighted)
corrupt=weighted.copy(); c,M=corrupt[0]; corrupt[0]=(c+1,M)
assert failures(corrupt)
nonzero_squarefree=[mon for mon in monomials if len(set(mon))==len(mon) and len(set(v for e in mon for v in e))==2*len(mon)]
assert len(nonzero_squarefree)==676
# Explicit action of every baseline-preserving automorphism.
orbit=set()
for perm in itertools.permutations(range(5)):
    for bits in itertools.product(range(2), repeat=5):
        relabel={2*i+p:2*perm[i]+(p^bits[i]) for i in range(5) for p in (0,1)}
        orbit.add(canonical((relabel[a],relabel[b]) for a,b in T))
assert orbit=={M for M in all_M if D[M]==4}
print('PASS hashes; 945 matching BFS/metric; 49 terms/346 distinct summands; 1081 formal monomials (676 reduced); corruption detected; all',len(orbit),'five-cycle targets covered')
# Independently check lower bounds on all small matching spaces.
total=0
for n in range(2,7):
    count=0; nonzero=[]
    for M in matchings(list(range(2*n))):
        S=set(M); dist=distance_formula(M)
        if n==2: value=int((0,2) in S)
        elif n==3: value=int((1,2) in S and (3,4) in S)
        else: value=(int((0,2) in S)-int((1,3) in S))*(int((4,6) in S)-int((5,7) in S))
        if value: nonzero.append(dist)
        assert dist>=min(n-1,3) or value==0
        count+=1
    assert min(nonzero)==min(n-1,3)
    total+=count
    print('PASS lower bound n=',n,'matchings=',count,'minimum nonzero distance=',min(nonzero))
print('PASS total lower-bound evaluations:',total)
