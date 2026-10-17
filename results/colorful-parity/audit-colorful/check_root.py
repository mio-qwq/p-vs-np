from pathlib import Path
import sys, random, json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from solver import colorful_cycles, pack_cycles
from check import brute
rng=random.Random(20261018); count=0
for n in range(2,8):
    for trial in range(50):
        k=rng.randrange(1,5); t=rng.randrange(1,n+1)
        colors=tuple(rng.randrange(t) for _ in range(n))
        a=[[rng.randrange(1<<k) for _ in range(n)] for _ in range(n)]
        initial=0
        for i in range(n): initial^=a[i][i]
        delta=[[a[i][j]^a[i][i] for j in range(n)] for i in range(n)]
        cycles=colorful_cycles(delta,colors); expected=brute(a,colors)
        for target in range(1<<k):
            witness=pack_cycles(cycles,target^initial,t)
            assert (witness is not None)==(target in expected),(n,k,t,colors,target)
            if witness is not None:
                p=list(range(n))
                for cycle in witness:
                    for i,v in enumerate(cycle): p[v]=cycle[(i+1)%len(cycle)]
                assert sorted(p)==list(range(n))
                actual=0
                for i in range(n): actual^=a[i][p[i]]
                assert actual==target
            count+=1
print(json.dumps({'status':'PASS','root_per_coloring_target_comparisons':count,'seed':20261018},indent=2))
