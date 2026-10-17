"""Read-only integration with the independently written graphic gadget."""
import hashlib
import importlib.util
import random
from pathlib import Path
from itertools import combinations
from blossom import maximum_matching, verify_matching

path = Path(__file__).resolve().parents[1]/'base'/'graphic.py'
spec = importlib.util.spec_from_file_location('graphic', path)
graphic = importlib.util.module_from_spec(spec); spec.loader.exec_module(graphic)
rng = random.Random(8641027)
max_n = 0
feasible = 0
for trial in range(1200):
    n = rng.randrange(1,8)
    possibilities = list(combinations(range(n),2)); rng.shuffle(possibilities)
    edges = possibilities[:rng.randrange(min(len(possibilities),12)+1)]
    available = list(range(len(edges))); rng.shuffle(available)
    pairs=[]
    while available:
        i=available.pop()
        partners = [j for j in available if set(edges[i]) & set(edges[j])]
        if partners and rng.random()<0.8:
            j=rng.choice(partners);available.remove(j);pairs.append((i,j))
    target=rng.randrange(1<<n)
    N, gadget_edges, external = graphic.gadget(n,edges,pairs,target)
    max_n=max(max_n,N)
    mate=maximum_matching(N,gadget_edges)
    assert verify_matching(N,gadget_edges,mate)
    perfect=verify_matching(N,gadget_edges,mate,True)
    expected=graphic.brute_join(edges,pairs,target)
    oracle_pm=graphic.brute_pm(N,gadget_edges)
    assert perfect == (expected is not None) == (oracle_pm is not None), (trial,n,edges,pairs,target)
    if perfect:
        mask=sum((mate[u]==v)<<i for i,(u,v) in enumerate(external))
        assert graphic.valid(edges,pairs,target,mask)
        feasible+=1
print(f'PASS integration=1200 feasible={feasible} max_gadget_vertices={max_n}')
print('graphic.py SHA256',hashlib.sha256(path.read_bytes()).hexdigest())
