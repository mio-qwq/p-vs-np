from itertools import product, permutations
import json

def require(b):
    if not b: raise RuntimeError('exact set equality failed')
result={}
for n in range(1,4):
    ps=list(permutations(range(n)))
    cases=checks=0
    for edges in product((-1,0,1),repeat=n*n):
        match=[(p,sum(edges[i*n+p[i]] for i in range(n))) for p in ps if all(edges[i*n+p[i]]>=0 for i in range(n))]
        if not match: continue
        cases+=1
        for t in (min(c for p,c in match),max(c for p,c in match)):
            expected={p for p,c in match if c==t}
            union={(i,p[i]) for p in expected for i in range(n)}
            actual={p for p in ps if all((i,p[i]) in union for i in range(n))}
            require(actual==expected); checks+=1
    result[n]={'nonempty_graph_colorings':cases,'extremal_checks':checks}
print(json.dumps(result,sort_keys=True))
