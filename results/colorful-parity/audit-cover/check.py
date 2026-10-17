from pathlib import Path
"""Independent local model and exhaustive controls; standard library only."""
from itertools import permutations, combinations
import random, json, sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from cover_solver import solve as root_solve
OUT=Path(__file__).parent

def family(n,t):
    if t<=1:
        yield (0,)*n; return
    L=(n-1).bit_length(); r=min(L,t-1)
    for bits in combinations(range(L),r):
        codes=[sum(((i>>b)&1)<<j for j,b in enumerate(bits)) for i in range(n)]
        for chosen in combinations(range(1<<r),t):
            ranks={v:j for j,v in enumerate(chosen)}
            yield tuple(ranks.get(v,0) for v in codes)

def one_coloring(a,lab,k,target,colors,reserve=True,mandatory=True,closecheck=True):
    n=len(a); M={i for i in range(n) if not a[i][i]}
    if len({colors[i] for i in M})<len(M):return None
    reserved={colors[i]:i for i in M}
    vertices=[i for i in range(n) if not reserve or colors[i] not in reserved or reserved[colors[i]]==i]
    req=sum(1<<c for c in reserved) if mandatory else 0
    D=target
    for i in range(n):D^=lab[i][i]
    cycles={}
    for s in vertices:
        states={(1<<colors[s],s,0):(s,)}
        while states:
            nxt={}
            for (mask,u,val),path in states.items():
                if len(path)>1 and (a[u][s] or not closecheck):
                    cycles.setdefault((mask,val^lab[u][s]^lab[u][u]),path)
                for v in vertices:
                    bit=1<<colors[v]
                    if a[u][v] and not mask&bit:
                        nxt.setdefault((mask|bit,v,val^lab[u][v]^lab[u][u]),path+(v,))
            states=nxt
    pack={0:{0:()}}
    for mask in range(1<<(max(colors,default=-1)+1)):
        for val,cs in list(pack.get(mask,{}).items()):
            if val==D and mask&req==req:
                p=list(range(n))
                for cyc in cs:
                    for j,u in enumerate(cyc):p[u]=cyc[(j+1)%len(cyc)]
                return tuple(p)
            for (cm,cv),cy in cycles.items():
                if not mask&cm:pack.setdefault(mask|cm,{}).setdefault(val^cv,cs+(cy,))
    return None

def solve(a,lab,k,target,C):
    n=len(a);R={i for side,i in C if side==0};S={i for side,i in C if side==1}
    assert all(a[i][j] or i in R or j in S for i in range(n) for j in range(n))
    t=min(n,2*(k+len(C))+1)
    for colors in family(n,t):
        p=one_coloring(a,lab,k,target,colors)
        if p is not None:return p
    return None

def valid(a,lab,p,target):
    if p is None:return False
    value=0
    for i,j in enumerate(p):
        if not a[i][j]:return False
        value^=lab[i][j]
    return value==target and sorted(p)==list(range(len(a)))

def mincover(a):
    n=len(a)
    for q in range(2*n+1):
        for C in combinations([(s,i) for s in range(2) for i in range(n)],q):
            if all(a[i][j] or (0,i) in C or (1,j) in C for i in range(n) for j in range(n)):return C

rng=random.Random(20261017); counts={'solver_cases':0,'polynomial_evaluations':0,'mixed_covers':0}

def check(a,lab,k,C):
    n=len(a);ps=list(permutations(range(n)));q=len(C)
    for target in range(1<<k):
        feasible=[p for p in ps if valid(a,lab,p,target)]
        for p in ps:
            f=1
            for side,i in C:
                av=sum(a[i][j]*(p[i]==j) for j in range(n)) if side==0 else sum(a[j][i]*(p[j]==i) for j in range(n))
                f*=av%2
            value=0
            for i,j in enumerate(p):value^=lab[i][j]
            for b in range(k):f*=1^((value>>b)&1)^((target>>b)&1)
            assert bool(f)==valid(a,lab,p,target)
            counts['polynomial_evaluations']+=1
        if feasible:assert min(sum(i!=j for i,j in enumerate(p)) for p in feasible)<=min(n,2*(k+q)+1)
        got=solve(a,lab,k,target,C)
        assert (got is not None)==bool(feasible),(a,lab,k,target,C,got,feasible)
        if got is not None:assert valid(a,lab,got,target)
        root=root_solve(lab,k,target,a,[(('r' if side==0 else 'c'),i) for side,i in C])
        assert (root is not None)==bool(feasible)
        if root is not None:assert valid(a,lab,root,target)
        counts['solver_cases']+=1
    if {s for s,i in C}=={0,1}:counts['mixed_covers']+=1

# Every allowed graph through n=3, min cover, k=0 and two random k=1 labels.
for n in range(4):
    for bits in range(1<<(n*n)):
        a=[[bool(bits&(1<<(i*n+j))) for j in range(n)] for i in range(n)]
        C=mincover(a)
        check(a,[[0]*n for _ in range(n)],0,C)
        for _ in range(2):check(a,[[rng.randrange(2) for _ in range(n)] for _ in range(n)],1,C)
# Explicit mixed/nonminimum covers, sparse and dense graphs, forbidden diagonal labels arbitrary.
for n in range(2,8):
    for _ in range(30):
        C=tuple((s,i) for s in range(2) for i in range(n) if rng.random()<.25)
        a=[[not ((0,i) in C or (1,j) in C) or rng.random()<.5 for j in range(n)] for i in range(n)]
        k=rng.randrange(4); lab=[[rng.randrange(1<<k) for _ in range(n)] for _ in range(n)]
        check(a,lab,k,C)
# Mutation controls each produce an invalid accepted witness.
a=[[True]*3 for _ in range(3)];a[0][0]=False;a[0][2]=False;lab=[[0]*3 for _ in range(3)]
p=one_coloring(a,lab,0,0,(0,0,1),reserve=False)
assert p is not None and not valid(a,lab,p,0)
p=one_coloring(a,lab,0,0,(0,1,2),mandatory=False)
assert p is not None and not valid(a,lab,p,0)
a=[[False,True],[False,True]];lab=[[0]*2 for _ in range(2)]
p=one_coloring(a,lab,0,0,(0,1),closecheck=False)
assert p is not None and not valid(a,lab,p,0)
counts['mutation_controls']=3
print(json.dumps(counts,indent=2));print('PASS')
