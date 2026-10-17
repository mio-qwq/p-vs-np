import itertools, random, json, time
from functools import reduce
from operator import xor

def dp(a, k, colors):
    n=len(a); t=max(colors,default=-1)+1
    delta=[[a[i][j]^a[i][i] for j in range(n)] for i in range(n)]
    cycles=[{} for _ in range(1<<t)]
    # One start at a time; a stored path is a witness for the state.
    for start in range(n):
        paths=[{} for _ in range(1<<t)]
        paths[1<<colors[start]][(start,0)]=(start,)
        for mask in range(1<<t):
            for (end,z),path in list(paths[mask].items()):
                if len(path)>=2:
                    cycles[mask].setdefault(z^delta[end][start],path)
                for v in range(n):
                    bit=1<<colors[v]
                    if not mask&bit:
                        paths[mask|bit].setdefault((v,z^delta[end][v]),path+(v,))
    packs=[{} for _ in range(1<<t)]; packs[0][0]=()
    for mask in range(1<<t):
        if not packs[mask]: continue
        unused=((1<<t)-1)^mask
        sub=unused
        while sub:
            for z,cycle in cycles[sub].items():
                for old,pack in list(packs[mask].items()):
                    packs[mask|sub].setdefault(old^z,pack+(cycle,))
            sub=(sub-1)&unused
    result={}
    baseline=reduce(xor,(a[i][i] for i in range(n)),0)
    for packdict in packs:
        for z,pack in packdict.items():
            p=list(range(n))
            for cycle in pack:
                for i,v in enumerate(cycle): p[v]=cycle[(i+1)%len(cycle)]
            assert sorted(p)==list(range(n))
            assert reduce(xor,(a[i][p[i]] for i in range(n)),0)==baseline^z
            support=[i for i in range(n) if p[i]!=i]
            assert len({colors[i] for i in support})==len(support)
            result[baseline^z]=tuple(p)
    return result

def brute(a,colors):
    n=len(a); result=set()
    for p in itertools.permutations(range(n)):
        support=[i for i in range(n) if p[i]!=i]
        if len({colors[i] for i in support})==len(support):
            result.add(reduce(xor,(a[i][p[i]] for i in range(n)),0))
    return result

def run():
    start=time.time(); tests=0; rng=random.Random(20261017)
    # Exhaust all binary 3x3 label matrices and all 2/3-colorings.
    for n,k in [(0,0),(1,1),(2,2),(3,1)]:
        for flat in itertools.product(range(1<<k),repeat=n*n):
            a=[list(flat[i*n:(i+1)*n]) for i in range(n)]
            colorings=[()] if n==0 else itertools.chain.from_iterable(itertools.product(range(t),repeat=n) for t in range(1,n+1))
            for colors in colorings:
                got=dp(a,k,colors); expected=brute(a,colors)
                assert set(got)==expected,(a,colors,got,expected)
                tests+=1
    for n in range(4,8):
        for _ in range(60):
            k=rng.randrange(1,5); t=rng.randrange(1,min(n,2*k+1)+1)
            a=[[rng.randrange(1<<k) for j in range(n)] for i in range(n)]
            colors=tuple(rng.randrange(t) for _ in range(n))
            assert set(dp(a,k,colors))==brute(a,colors)
            tests+=1
    print(json.dumps({'status':'PASS','per_coloring_tests':tests,'seed':20261017,'seconds':round(time.time()-start,3),'coverage':'exhaustive labels n<=3 as specified; every coloring; random n=4..7; every returned witness verified'},indent=2))
if __name__=='__main__': run()
