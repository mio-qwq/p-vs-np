"""Independent exhaustive projection check; Python standard library only."""
from collections import deque
from functools import lru_cache
import json
from pathlib import Path

@lru_cache(None)
def matchings(vertices):
    if not vertices:
        return ((),)
    a, *rest = vertices
    out = []
    for b in rest:
        remaining = tuple(x for x in rest if x != b)
        for tail in matchings(remaining):
            out.append(tuple(sorted(((a,b),) + tail)))
    return tuple(out)

def cycle_distance(M,n):
    parent=list(range(n))
    def root(x):
        while parent[x]!=x:
            x=parent[x]
        return x
    for a,b in M:
        x,y=root(a//2),root(b//2)
        parent[x]=y
    return n-len({root(x) for x in range(n)})

def neighbors(M):
    for i,(a,b) in enumerate(M):
        for j in range(i+1,len(M)):
            c,d=M[j]
            rest=M[:i]+M[i+1:j]+M[j+1:]
            for edges in (((a,c),(b,d)),((a,d),(b,c))):
                yield tuple(sorted(rest+tuple(tuple(sorted(e)) for e in edges)))

results={"bfs_distance_checks": [], "projection_checks": []}
minima={}
for n in range(8):
    ms=matchings(tuple(range(2*n)))
    if n <= 5:
        baseline=tuple((2*i,2*i+1) for i in range(n))
        dist={baseline:0}
        queue=deque([baseline])
        while queue:
            cur=queue.popleft()
            for nxt in neighbors(cur):
                if nxt not in dist:
                    dist[nxt]=dist[cur]+1
                    queue.append(nxt)
        assert len(dist)==len(ms)
        assert all(dist[M]==cycle_distance(M,n) for M in ms)
        results['bfs_distance_checks'].append({'n':n,'matchings':len(ms),'passed':True})
    for m in range(min(n,4)+1):
        md={}
        for M in ms:
            signature=tuple(e for e in M if e[1]<2*m)
            d=cycle_distance(M,n)
            md[signature]=min(d,md.get(signature,100))
        minima[n,m]=md
for m in range(5):
    for r in range(4):
        finite_n=m+r
        target={s for s,d in minima[finite_n,m].items() if d<=r}
        counts=[]
        for ambient_n in range(m,8):
            observed={s for s,d in minima[ambient_n,m].items() if d<=r}
            # Every ambient projection embeds into m+r. Once enough auxiliary
            # pairs exist, the projection sets coincide in both directions.
            assert observed <= target,(m,r,ambient_n,'unexpected projection')
            if ambient_n>=finite_n:
                assert observed == target,(m,r,ambient_n,'missing projection')
            counts.append({'ambient_n':ambient_n,'projections':len(observed)})
        results['projection_checks'].append({'m':m,'r':r,'finite_n':finite_n,'finite_projections':len(target),'ambient_counts':counts,'passed':True})
Path(__file__).with_name('results.json').write_text(json.dumps(results,indent=2)+'\n')
print('PASS: BFS verifies cycle distance for every matching on 0–5 pairs.')
print('PASS: all m=0–4, r=0–3 and ambient m–7 pairs satisfy exact projection containment; equality once ambient >= m+r.')
print('Enumerated counts:',{n:len(matchings(tuple(range(2*n)))) for n in range(8)})
