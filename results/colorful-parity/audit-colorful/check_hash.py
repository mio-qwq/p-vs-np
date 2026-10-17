from itertools import combinations
import json

def family(n,t):
    L=(n-1).bit_length(); r=min(L,t-1); q=1<<r
    for bits in combinations(range(L),r):
        codes=[sum(((v>>b)&1)<<j for j,b in enumerate(bits)) for v in range(n)]
        for subset in combinations(range(q),t):
            ranks={v:i for i,v in enumerate(subset)}
            yield tuple(ranks.get(v,0) for v in codes)

cases=0; tested_subsets=0
for n in range(2,13):
    for t in range(2,min(n,5)+1):
        remaining=set(combinations(range(n),t))
        tested_subsets+=len(remaining)
        for h in family(n,t):
            remaining={s for s in remaining if len({h[v] for v in s})<t}
            if not remaining: break
        assert not remaining,(n,t,remaining)
        cases+=1
print(json.dumps({'status':'PASS','n_t_pairs':cases,'subsets_checked':tested_subsets,'n_max':12,'t_max':5},indent=2))
