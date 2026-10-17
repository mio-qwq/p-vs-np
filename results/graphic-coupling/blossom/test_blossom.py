"""Independent subset-DP exhaustive oracle and reproducible backend tests."""
from functools import lru_cache
from itertools import combinations
import random
import time
from blossom import maximum_matching, maximum_matching_edges, verify_matching


def oracle(n, edges):
    adjacency = [0] * n
    for a,b in edges:
        adjacency[a] |= 1 << b
        adjacency[b] |= 1 << a
    @lru_cache(None)
    def solve(mask):
        if not mask:
            return 0
        vbit = mask & -mask
        v = vbit.bit_length()-1
        rest = mask ^ vbit
        best = solve(rest)
        options = adjacency[v] & rest
        while options:
            wbit = options & -options
            options ^= wbit
            best = max(best, 1 + solve(rest ^ wbit))
        return best
    return solve((1 << n)-1)


counts = {'exhaustive': 0, 'random': 0, 'structured': 0, 'malformed': 0, 'negative_matching': 0}
def check(n, edges, category):
    expected = oracle(n, edges)
    mate = maximum_matching(n, edges)
    assert verify_matching(n, edges, mate), (n, edges, mate)
    actual = sum(u != -1 for u in mate)//2
    assert actual == expected, (n, edges, expected, mate)
    assert verify_matching(n, edges, mate, require_perfect=True) == (2*expected == n)
    assert len(maximum_matching_edges(n, edges)) == expected
    counts[category] += 1


start = time.monotonic()
for n in range(6):
    possible = list(combinations(range(n), 2))
    for mask in range(1 << len(possible)):
        check(n, [edge for i,edge in enumerate(possible) if mask >> i & 1], 'exhaustive')

rng = random.Random(20261017)
for n in range(13):
    for _ in range(200):
        p = rng.choice([0.05, 0.15, 0.3, 0.5, 0.7, 0.9])
        edges = [e for e in combinations(range(n),2) if rng.random() < p]
        check(n, edges, 'random')

# Odd cycles, linked odd cycles, an odd cycle enclosing a smaller odd-cycle
# contraction, a blossom with alternating stems, and disconnected controls.
# Relabeling changes BFS order and exercises different contraction orders.
fixtures = [
 (3, [(0,1),(1,2),(2,0)]),
 (5, [(i,(i+1)%5) for i in range(5)]),
 (7, [(i,(i+1)%7) for i in range(7)]),
 (8, [(0,1),(1,2),(2,0),(2,3),(3,4),(4,5),(5,3),(5,6),(6,7)]),
 (9, [(0,1),(1,2),(2,0),(2,3),(3,4),(4,5),(5,6),(6,0),(3,7),(7,8)]),
 (10, [(0,1),(1,2),(2,0),(0,3),(3,4),(4,5),(5,6),(6,0),(2,7),(7,8),(8,9)]),
 (12, [(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(2,3),(5,6),(6,7)]),
 (12, []),
 (12, [(i,i+1) for i in range(0,12,2)]),
 (11, list(combinations(range(11),2))),
]
for n, edges in fixtures:
    for _ in range(60):
        perm = list(range(n)); rng.shuffle(perm)
        check(n, [(perm[u],perm[v]) for u,v in edges], 'structured')

bad_graphs = [(-1, []),(True, []),(3.0, []),(3,None),(3,[(0,0)]),
 (3,[(0,3)]),(3,[(-1,2)]),(3,[(False,1)]),(3,[(0,1.0)]),(3,[(0,)]),
 (3,[(0,1,2)]),(3,[None]),(3,['01']),(3,[1])]
for n, edges in bad_graphs:
    for fn in (maximum_matching, maximum_matching_edges):
        try: fn(n,edges)
        except ValueError: counts['malformed'] += 1
        else: raise AssertionError((fn.__name__,n,edges))

for matching in [(1,0), (1,0,-1,-1,-1), (1,-1,-1,-1), (0,-1,-1,-1),
                 (2,-1,0,-1), (4,-1,-1,-1), (-2,-1,-1,-1),
                 (True,0,-1,-1), (1.0,0,-1,-1), None]:
    assert not verify_matching(4,[(0,1),(2,3)], matching)
    counts['negative_matching'] += 1
assert verify_matching(4,[(0,1),(2,3)],[-1]*4)
assert not verify_matching(4,[(0,1),(2,3)],[-1]*4,True)
assert maximum_matching(2,[(0,1),(1,0),(0,1)]) == (1,0)
assert maximum_matching(0,[]) == ()
assert verify_matching(0,[],(),True)
print('PASS', counts, 'seconds=',round(time.monotonic()-start,3))
