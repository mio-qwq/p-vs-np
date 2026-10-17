from itertools import combinations, permutations, product
from random import Random
from solver import solve, colorings, colorful_cycles, pack_cycles


def possible(labels):
    out = set()
    for permutation in permutations(range(len(labels))):
        value = 0
        for i, j in enumerate(permutation):
            value ^= labels[i][j]
        out.add(value)
    return out


checks = 0
for n in range(0, 4):
    for flat in product(range(2), repeat=n*n):
        labels = [list(flat[n*i:n*(i+1)]) for i in range(n)]
        expected = possible(labels)
        for target in range(2):
            result = solve(labels, 1, target)
            assert (result is not None) == (target in expected)
            checks += 1
rng = Random(20261017)
for n in range(2, 8):
    for k in (1, 2, 3):
        for trial in range(12):
            labels = [[rng.randrange(1 << k) for j in range(n)] for i in range(n)]
            expected = possible(labels)
            for target in range(1 << k):
                result = solve(labels, k, target)
                assert (result is not None) == (target in expected), (n,k,target,labels)
                checks += 1
cover_tests = 0
for n in range(2, 17):
    for t in range(2, min(n, 5) + 1):
        uncovered = set(combinations(range(n), t))
        for colors in colorings(n, t):
            uncovered = {s for s in uncovered if len({colors[v] for v in s}) < t}
            if not uncovered:
                break
        assert not uncovered, (n,t)
        cover_tests += 1
# Genuine negative targets force the full family, not merely first-color success.
for n in range(2, 9):
    labels = [[0] * n for _ in range(n)]
    assert solve(labels, 2, 1) is None
    checks += 1
for args in [([[0,1]],1,0), ([[2]],1,0), ([[0]],-1,0), ([[0]],1,2)]:
    try:
        solve(*args)
    except ValueError:
        pass
    else:
        raise AssertionError('malformed accepted')
print({'bruteforce_target_comparisons': checks, 'perfect_hash_cover_cases': cover_tests,
       'malformed_controls':4, 'status':'PASS'})
