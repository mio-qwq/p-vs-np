from itertools import permutations, product
from random import Random
from cover_solver import solve


def possible(labels, allowed):
    values = set()
    for p in permutations(range(len(labels))):
        if all(allowed[i][j] for i,j in enumerate(p)):
            value = 0
            for i,j in enumerate(p):
                value ^= labels[i][j]
            values.add(value)
    return values


rng = Random(202610171415)
checks = 0
for n in range(4):
    for bits in product((False, True), repeat=n*n):
        allowed = [list(bits[i*n:(i+1)*n]) for i in range(n)]
        cover = [('r',i) for i in range(n)]
        labels = [[rng.randrange(4) for _ in range(n)] for _ in range(n)]
        expected = possible(labels, allowed)
        for target in range(4):
            assert (solve(labels,2,target,allowed,cover) is not None) == (target in expected)
            checks += 1
for n in range(2,8):
    for trial in range(25):
        k = rng.randrange(4)
        vertices = [('r',i) for i in range(n)] + [('c',i) for i in range(n)]
        cover = rng.sample(vertices, rng.randrange(min(4,2*n)+1))
        allowed = [[not ((('r',i) in cover or ('c',j) in cover) and rng.randrange(2))
                    for j in range(n)] for i in range(n)]
        labels = [[rng.randrange(1<<k) for _ in range(n)] for _ in range(n)]
        expected = possible(labels,allowed)
        for target in range(1<<k):
            result = solve(labels,k,target,allowed,cover)
            assert (result is not None) == (target in expected), (n,k,target)
            checks += 1
# A zero parity target cannot excuse an illegal fixed diagonal.
assert solve([[0]],0,0,[[False]],[('r',0)]) is None
assert solve([[0,0],[0,0]],0,0,[[False,True],[True,True]],[('r',0)]) == (1,0)
try:
    solve([[0]],0,0,[[False]],[])
except ValueError:
    pass
else:
    raise AssertionError('invalid cover accepted')
print({'target_comparisons':checks,'mandatory_controls':2,'bad_cover_controls':1,'status':'PASS'})
