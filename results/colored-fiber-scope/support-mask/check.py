#!/usr/bin/env python3
"""Exact, bounded structural certificates. Python standard library only."""
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edges(p):
    return frozenset(enumerate(p))


def union(family):
    return frozenset().union(*(edges(p) for p in family))


def matching_set(n, support):
    return tuple(p for p in permutations(range(n)) if edges(p) <= support)


def cost(p, red):
    return len(edges(p) & red)


def parity(p):
    return (-1) ** sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p)))


def mul(p, q):
    out = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return out


def polynomial(family):
    n = len(family[0])
    out = [0] * (n * (n - 1) // 2 + 1)
    for p in family:
        term = [parity(p)]
        for i, exponent in enumerate(p):
            for _ in range(exponent):
                term = mul(term, [i, 1])
        for d, coefficient in enumerate(term):
            out[d] += coefficient
    return out


def potentials(n, support, red):
    adjacency = [[] for _ in range(2 * n)]
    for i, j in support:
        w = int((i, j) in red)
        adjacency[i].append((n + j, w))
        adjacency[n + j].append((i, w))
    values = [None] * (2 * n)
    for root in range(2 * n):
        if values[root] is not None:
            continue
        values[root] = 0
        queue = [root]
        for v in queue:
            for w, c in adjacency[v]:
                candidate = c - values[v]
                if values[w] is None:
                    values[w] = candidate
                    queue.append(w)
                elif values[w] != candidate:
                    return None
    return values[:n], values[n:]


def main():
    p3 = tuple(permutations(range(3)))
    full3 = frozenset((i, j) for i in range(3) for j in range(3))
    red = frozenset((i, i) for i in range(3))
    f = tuple(p for p in p3 if cost(p, red) == 1)
    require(len(f) == 3 and all(parity(p) == -1 for p in f), 'fiber is three transpositions')
    require(union(f) == full3, 'fiber union is full')
    require(len(matching_set(3, union(f))) == 6, 'union has six matchings')
    require(sorted(cost(p, red) for p in p3) == [0, 0, 1, 1, 1, 3], 'full costs')
    require(potentials(3, full3, red) is None, 'negative potential certificate')
    require(polynomial(f) == [-2, -9, -9, -3], 'displayed P1 polynomial')
    require(polynomial(p3) == [2, 0, 0, 0], 'union-mask determinant')

    binary_determinants = set()
    for mask in range(1 << 9):
        support = frozenset((i, j) for i in range(3) for j in range(3) if mask >> (3 * i + j) & 1)
        binary_determinants.add(sum(parity(p) for p in matching_set(3, support)))
    require(binary_determinants == {-2, -1, 0, 1, 2}, 'no accidental mask polynomial equality')

    for pair in combinations(f, 2):
        require(set(matching_set(3, union(pair))) == set(pair), 'pairwise closure')

    # Explicit private-edge certificate for every maximal proper 3x3 support.
    private_certificates = []
    for missing in sorted(full3):
        allowed = matching_set(3, full3 - {missing})
        require(len(allowed) == 4, 'one missing edge leaves four matchings')
        for p in allowed:
            others = union(tuple(q for q in allowed if q != p))
            private = sorted(edges(p) - others)
            require(bool(private), 'every allowed matching has a private edge')
            private_certificates.append({'missing': missing, 'matching': p, 'private': private})

    # This is a new support-closure check over families, not an ASNC coloring test.
    proper_family_count = 0
    full_union_by_size = {}
    for mask in range(1, 1 << len(p3)):
        family = tuple(p for k, p in enumerate(p3) if mask >> k & 1)
        support = union(family)
        if support != full3:
            require(set(matching_set(3, support)) == set(family), 'proper support closure')
            proper_family_count += 1
        else:
            size = str(len(family))
            full_union_by_size[size] = full_union_by_size.get(size, 0) + 1
    require(proper_family_count == 48, 'proper family count')
    require(full_union_by_size == {'3': 2, '4': 6, '5': 6, '6': 1}, 'full union family counts')

    for n in (1, 2):
        pn = tuple(permutations(range(n)))
        for mask in range(1, 1 << len(pn)):
            family = tuple(p for k, p in enumerate(pn) if mask >> k & 1)
            require(set(matching_set(n, union(family))) == set(family), 'n<=2 minimality')

    partial_count = 0
    for size in (0, 1, 2):
        for partial in combinations(sorted(full3), size):
            if len({i for i, j in partial}) != size or len({j for i, j in partial}) != size:
                continue
            partial_count += 1
            require(any(set(partial) <= edges(p) for p in p3), 'two-extendability')
    require(partial_count == 28, 'partial matching count')

    identity = (0, 1, 2)
    cycle = (1, 2, 0)
    edge_support = edges(identity) | edges(cycle)
    require(set(matching_set(3, edge_support)) == {identity, cycle}, 'Birkhoff edge support')
    x = [[Fraction(int(j == identity[i]) + 2 * int(j == cycle[i]), 3)
          for j in range(3)] for i in range(3)]
    require(all(sum(row) == 1 for row in x), 'fractional row sums')
    require(all(sum(x[i][j] for i in range(3)) == 1 for j in range(3)), 'fractional column sums')
    require(sum(x[i][i] for i in range(3)) == 1, 'fractional point count')
    require(any(v.denominator != 1 for row in x for v in row), 'fractionality')
    require(not any(edges(p) <= edge_support for p in f), 'slice point outside fiber hull')
    require(Fraction(1, 3) * cost(identity, red) + Fraction(2, 3) * cost(cycle, red) == 1,
            'unique edge-slice interpolation')

    blocks = frozenset((i, j) for i in range(4) for j in range(4) if i // 2 == j // 2)
    red4 = frozenset((i, i) for i in range(4))
    p4 = matching_set(4, blocks)
    f4 = tuple(p for p in p4 if cost(p, red4) == 2)
    require(len(blocks) == 8 and len(p4) == 4 and len(f4) == 2, 'eight-edge example sizes')
    require(union(f4) == blocks, 'eight-edge fiber union')
    require(sorted(cost(p, red4) for p in p4) == [0, 2, 2, 4], 'eight-edge costs')
    require(potentials(4, blocks, red4) is None, 'eight-edge potential obstruction')

    red_interior = frozenset({(0, 0), (1, 1)})
    interior_fiber = tuple(p for p in p3 if cost(p, red_interior) == 1)
    interior_support = union(interior_fiber)
    interior_potentials = potentials(3, interior_support, red_interior)
    require(len(interior_fiber) == 2 and len(interior_support) == 6, 'interior positive example')
    require(set(matching_set(3, interior_support)) == set(interior_fiber), 'interior representation')
    require(interior_potentials is not None, 'interior potentials exist')
    require(sum(interior_potentials[0]) + sum(interior_potentials[1]) == 1, 'potential total')
    require({cost(p, red_interior) for p in p3} == {0, 1, 2}, 'target genuinely interior')

    result = {
        'status': 'PASS',
        'scope': 'Support representation and explicit geometric certificates; no ASNC enumeration.',
        'smallest_order': 3,
        'smallest_support_edges_at_order_three': 9,
        'minimum_support_edges_over_all_orders': 8,
        'diagonal_red_fiber': f,
        'P1_coefficients_ascending': polynomial(f),
        'binary_3x3_determinants': sorted(binary_determinants),
        'K33_partial_matchings_extended': partial_count,
        'proper_support_family_checks': proper_family_count,
        'full_support_family_counts': full_union_by_size,
        'private_edge_certificates': private_certificates,
        'fractional_slice_vertex': [[str(v) for v in row] for row in x],
        'eight_edge_fiber': f4,
        'representable_interior_fiber': interior_fiber,
        'representable_interior_potentials': interior_potentials,
    }
    target = Path(__file__).with_name('results.json')
    target.write_text(json.dumps(result, indent=2) + '\n')
    print('PASS: exact criterion examples, minimality certificates, intended brace, and fractional slice vertex.')
    print('P1 coefficients:', polynomial(f))
    print('Results SHA256:', sha256(target.read_bytes()).hexdigest())


if __name__ == '__main__':
    main()
