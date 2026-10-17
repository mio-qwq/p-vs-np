from itertools import combinations
from collections import Counter
from pathlib import Path
import json

def matchings(V):
    if not V:
        yield ()
        return
    a=V[0]
    for b in V[1:]:
        for rest in matchings(tuple(x for x in V[1:] if x!=b)):
            yield ((a,b),)+rest

def distance(M,n):
    adj={i:set() for i in range(n)}
    for a,b in M:
        adj[a//2].add(b//2); adj[b//2].add(a//2)
    unseen=set(adj); components=0
    while unseen:
        stack=[unseen.pop()]; components+=1
        while stack:
            for v in adj[stack.pop()] & unseen:
                unseen.remove(v); stack.append(v)
    return n-components

def value(M,d):
    M=set(M); val=1
    for i in range(d): val*=int((4*i,4*i+2) in M)-int((4*i+1,4*i+3) in M)
    return val

results=[]
for n in range(2,8):
    hist={d:Counter() for d in range(1,n//2+1)}
    total=0
    for M in matchings(tuple(range(2*n))):
        total+=1; dist=distance(M,n)
        for d in hist:
            if value(M,d): hist[d][dist]+=1
    for d,counts in hist.items():
        minimum=min(counts) if counts else None
        expected=None if (n,d)==(2,1) else (3*d+1)//2
        assert minimum==expected,(n,d,minimum,expected)
        results.append({'n':n,'d':d,'all_matchings':total,'minimum_nonzero_distance':minimum,'nonzero_histogram':dict(sorted(counts.items()))})
Path(__file__).with_name('results.json').write_text(json.dumps(results,indent=2)+'\n')
print('PASS: all admissible d>=1 and n=2,...,7; '+str(len(results))+' cases.')
