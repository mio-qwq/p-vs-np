"""Exact standard-library regression tests for matching-fiber geometry."""
from fractions import Fraction
from itertools import permutations, product
from math import gcd
from functools import reduce


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def rref(rows, cols):
    a = [[Fraction(x) for x in row] for row in rows]
    pivots = []
    for c in range(cols):
        pivot = next((r for r in range(len(pivots), len(a)) if a[r][c]), None)
        if pivot is None:
            continue
        r = len(pivots)
        a[r], a[pivot] = a[pivot], a[r]
        scale = a[r][c]
        a[r] = [x / scale for x in a[r]]
        for s in range(len(a)):
            if s != r and a[s][c]:
                scale = a[s][c]
                a[s] = [x - scale * y for x, y in zip(a[s], a[r])]
        pivots.append(c)
    return a, pivots


def rank(rows, cols):
    return len(rref(rows, cols)[1])


def integer_null_basis(rows, cols):
    a, pivots = rref(rows, cols)
    result = []
    for f in range(cols):
        if f in pivots:
            continue
        b = [Fraction(0) for _ in range(cols)]
        b[f] = Fraction(1)
        for r, p in enumerate(pivots):
            b[p] = -a[r][f]
        lcm = reduce(lambda x, y: x * y // gcd(x, y), (x.denominator for x in b), 1)
        result.append([int(x * lcm) for x in b])
    return result


def sub(x, y):
    return [a-b for a, b in zip(x, y)]


def dot(x, y):
    return sum(a*b for a, b in zip(x, y))


def affine_closed(points, chosen):
    base = points[min(chosen)]
    rows = [sub(points[i], base) for i in sorted(chosen)]
    d = len(base)
    r = rank(rows, d)
    return all(i in chosen or rank(rows + [sub(p, base)], d) > r
               for i, p in enumerate(points))


def construct_cost(points, chosen):
    base = points[min(chosen)]
    rows = [sub(points[i], base) for i in sorted(chosen)]
    outside = [sub(p, base) for i, p in enumerate(points) if i not in chosen]
    if not outside:
        return [0] * len(base)
    basis = integer_null_basis(rows, len(base))
    require(basis, 'nonempty outside requires positive normal dimension')
    for s in range(len(outside) * (len(basis) - 1) + 1):
        w = [sum(s**j * b[e] for j, b in enumerate(basis)) for e in range(len(base))]
        if all(dot(w, v) != 0 for v in outside):
            shift = max(0, -min(w, default=0))
            return [x + shift for x in w]
    raise RuntimeError('finite-hyperplane construction did not find cost')


def main():
    n = 3
    ps = list(permutations(range(n)))
    points = [[int(j == p[i]) for i in range(n) for j in range(n)] for p in ps]
    ids = {p: i for i, p in enumerate(ps)}
    positive = [(0,1,2), (1,2,0), (2,0,1)]
    negative = [(0,2,1), (1,0,2), (2,1,0)]
    for e in range(n*n):
        require(sum(points[ids[p]][e] for p in positive) == 1, 'positive factorization')
        require(sum(points[ids[p]][e] for p in negative) == 1, 'negative factorization')
    target = ids[(2,1,0)]
    chosen = set(range(6)) - {target}
    require(all(any(points[i][e] for i in chosen) for e in range(9)), 'union graph is K3,3')
    require(not affine_closed(points, chosen), 'five-matching set must be obstructed')
    coef = [1,-1,-1,1,1]
    require(sum(coef) == 1, 'certificate affine normalization')
    require([sum(coef[k] * points[i][e] for k, i in enumerate(sorted(chosen)))
             for e in range(9)] == points[target], 'explicit affine certificate')

    fiber_masks = set()
    for coloring in range(1 << 9):
        w = [(coloring >> e) & 1 for e in range(9)]
        by_cost = {}
        for i, p in enumerate(points):
            t = dot(w, p)
            by_cost[t] = by_cost.get(t, 0) | (1 << i)
        fiber_masks.update(by_cost.values())
    require(len(fiber_masks) == 57, 'K3,3 binary fiber count')
    for mask in range(1, 1 << 6):
        subset = {i for i in range(6) if mask & (1 << i)}
        is_closed = affine_closed(points, subset)
        require(is_closed == (mask in fiber_masks), 'bounded affine/binary equivalence')
        if is_closed:
            w = construct_cost(points, subset)
            require(all(isinstance(x, int) and x >= 0 for x in w), 'integer nonnegative costs')
            t = dot(w, points[min(subset)])
            actual = {i for i, p in enumerate(points) if dot(w, p) == t}
            require(actual == subset, 'constructed complete fiber')
    # Binary witnesses on the realizable side of the sharp cycle-family boundary.
    for r, w in [(1, [0,0,0,0]), (2, [0,1,0,0, 1,0,0,0]),
                 (3, [0,1,0,0, 0,1,0,0, 1,0,0,1])]:
        costs = []
        for choice in range(1 << r):
            p = []
            for block in range(r):
                p.extend([0,1,1,0] if choice & (1 << block) else [1,0,0,1])
            costs.append(dot(w, p))
        require(all(x in (0,1) for x in w), 'small-cycle binary witness')
        require({i for i, c in enumerate(costs) if c == costs[0]} == {0,(1 << r)-1},
                'small-cycle endpoint fiber')
    # Four disjoint K2,2 blocks: exact real-cost fiber and binary obstruction.
    block_points = []
    for choice in range(16):
        v = []
        for r in range(4):
            v.extend([0,1,1,0] if choice & (1 << r) else [1,0,0,1])
        block_points.append(v)
    w = [0,1,0,0] * 3 + [3,0,0,0]
    require(affine_closed(block_points, {0,15}), 'two-endpoint affine closure')
    require(all(block_points[0][e] + block_points[15][e] == 1 for e in range(16)),
            'two-endpoint union includes every graph edge')
    require({i for i, p in enumerate(block_points) if dot(w,p) == 3} == {0,15},
            'four-block integer cost fiber')
    for delta in product(range(-2,3), repeat=4):
        if sum(delta) != 0:
            continue
        require(any(sum(delta[r] for r in range(4) if subset & (1 << r)) == 0
                    for subset in range(1,15)), 'binary difference proper zero subsum')
    # Zero-dimensional and one-matching cases require no exceptional convention.
    require(construct_cost([[]], {0}) == [], 'empty matching case')
    require(affine_closed([[]], {0}), 'empty matching affine closure')
    print('PASS: exact affine certificate; union graph; all 63 nonempty K3,3 subsets;')
    print('      all 512 binary colorings; all 57 constructive integer fibers; empty matching.')
    print('      Four-cycle strict boundary: 16 matchings and 625 binary difference vectors.')


if __name__ == '__main__':
    main()
