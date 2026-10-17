from itertools import combinations, product
from functools import lru_cache
from random import Random

def matchings(items):
    if not items:return [()]
    x,*tail=items
    out=matchings(tail)
    out=[tuple(P) for P in out]
    for j,y in enumerate(tail):
        for P in matchings(tail[:j]+tail[j+1:]):out.append(((x,y),)+P)
    return out

def solve_original(n,edges,pairs,b):
    for mask in range(1<<len(edges)):
        parity=[0]*n
        for e,(v,w) in enumerate(edges):
            if mask>>e&1:parity[v]^=1;parity[w]^=1
        if parity!=list(b):continue
        if any((mask>>e&1) and (mask>>f&1) for P in pairs for e,f in P):continue
        return mask
    return None

def gadget(n,edges,pairs,b):
    adj=[];names=[]
    def vertex(name):names.append(name);adj.append(0);return len(adj)-1
    def link(a,c):adj[a]|=1<<c;adj[c]|=1<<a
    ports={}; local=[[] for _ in range(n)]
    for e,(v,w) in enumerate(edges):
        for z in (v,w):ports[z,e]=vertex(('port',z,e));local[z].append(ports[z,e])
    external=[]
    for e,(v,w) in enumerate(edges):
        p,q=ports[v,e],ports[w,e];link(p,q);external.append((p,q))
    for v in range(n):
        d=len(local[v]);p=len(pairs[v]);c=d-p
        for e,f in pairs[v]:
            a=vertex(('aux',v,e,f));link(a,ports[v,e]);link(a,ports[v,f])
        if (c-b[v])%2:local[v].append(vertex(('dummy',v)))
        for p,q in combinations(local[v],2):link(p,q)
    return adj,external,names

def perfect(adj):
    @lru_cache(None)
    def rec(mask):
        if not mask:return ()
        if mask.bit_count()%2:return None
        # Fail-first choice minimizes available neighbors.
        vs=[i for i in range(len(adj)) if mask>>i&1]
        u=min(vs,key=lambda i:(adj[i]&mask).bit_count())
        rest=mask^(1<<u);ns=adj[u]&rest
        while ns:
            bit=ns&-ns;ns-=bit;v=bit.bit_length()-1
            M=rec(rest^bit)
            if M is not None:return ((u,v),)+M
        return None
    return rec((1<<len(adj))-1)

def check(n,edges,pairs,b):
    sol=solve_original(n,edges,pairs,b)
    adj,external,names=gadget(n,edges,pairs,b);M=perfect(adj)
    assert (sol is None)==(M is None),(n,edges,pairs,b,sol,M)
    if M is not None:
        chosen={frozenset(e) for e in M}
        mask=sum(1<<e for e,pq in enumerate(external) if frozenset(pq) in chosen)
        parity=[0]*n
        for e,(v,w) in enumerate(edges):
            if mask>>e&1:parity[v]^=1;parity[w]^=1
        assert parity==list(b)
        assert not any((mask>>e&1) and (mask>>f&1) for P in pairs for e,f in P)

count=0
for n in range(0,4):
    possible=list(combinations(range(n),2))
    for mask in range(1<<len(possible)):
        edges=[e for i,e in enumerate(possible) if mask>>i&1]
        incident=[[e for e,ends in enumerate(edges) if v in ends] for v in range(n)]
        for pairs in product(*(matchings(I) for I in incident)):
            for b in product((0,1),repeat=n):check(n,edges,pairs,b);count+=1
print('exhaustive n<=3 graph/pair/parity instances',count)
rng=Random(31820)
for trial in range(2000):
    n=rng.randrange(1,7)
    edges=[e for e in combinations(range(n),2) if rng.random()<.45]
    if len(edges)>11:edges=edges[:11]
    incident=[[e for e,ends in enumerate(edges) if v in ends] for v in range(n)]
    pairs=[rng.choice(matchings(I)) for I in incident]
    b=[rng.randrange(2) for _ in range(n)]
    check(n,edges,pairs,b)
print('2000 seeded random graph/pair/parity instances PASS')
# Two parallel edges and their conflict are represented by distinct ports.
for b in product((0,1),repeat=2):
 for pairs in product(((),((0,1),)),repeat=2):check(2,[(0,1),(0,1)],pairs,b)
print('parallel-edge controls PASS')
