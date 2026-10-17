from itertools import product
from random import Random
from general_solver import solve


def matchings(vertices):
    if not vertices:
        yield ()
        return
    first,*rest = vertices
    for j,other in enumerate(rest):
        for tail in matchings(rest[:j]+rest[j+1:]):
            yield ((first,other),)+tail


def feasible(labels,allowed):
    values=set()
    for edges in matchings(list(range(len(labels)))):
        if all(allowed[u][v] for u,v in edges):
            value=0
            for u,v in edges:
                value ^= labels[u][v]
            values.add(value)
    return values


rng=Random(20261017)
checks=0
for size in (0,2,4):
    edges=[(u,v) for u in range(size) for v in range(u+1,size)]
    for bits in product((False,True),repeat=len(edges)):
        allowed=[[False]*size for _ in range(size)]
        labels=[[0]*size for _ in range(size)]
        for (u,v),bit in zip(edges,bits):
            allowed[u][v]=allowed[v][u]=bit
            labels[u][v]=labels[v][u]=rng.randrange(4)
        expected=feasible(labels,allowed)
        for target in range(4):
            assert (solve(labels,2,target,allowed,range(size)) is not None)==(target in expected)
            checks+=1
for size,trials in ((4,50),(6,100),(8,50),(10,20),(12,4)):
    for trial in range(trials):
        k=rng.randrange(4)
        cover=rng.sample(range(size),rng.randrange(min(size,4)+1))
        labels=[[0]*size for _ in range(size)]
        allowed=[[False]*size for _ in range(size)]
        for u in range(size):
            for v in range(u+1,size):
                labels[u][v]=labels[v][u]=rng.randrange(1<<k)
                allowed[u][v]=allowed[v][u]=not ((u in cover or v in cover) and rng.randrange(2))
        expected=feasible(labels,allowed)
        for target in range(1<<k):
            result=solve(labels,k,target,allowed,cover)
            assert (result is not None)==(target in expected),(size,k,target)
            checks+=1
for bits in product(range(2),repeat=6):
    labels=[[0]*4 for _ in range(4)]
    for (u,v),bit in zip([(u,v) for u in range(4) for v in range(u+1,4)],bits):
        labels[u][v]=labels[v][u]=bit
    expected=feasible(labels,[[u!=v for v in range(4)] for u in range(4)])
    for target in range(2):
        assert (solve(labels,1,target) is not None)==(target in expected)
        checks+=1
try:
    solve([[0]],0,0)
except ValueError:
    pass
else:
    raise AssertionError('odd vertex count accepted')
print({'target_comparisons':checks,'max_vertices':12,'odd_size_control':1,'status':'PASS'})
