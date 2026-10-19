#!/usr/bin/env python3
"""Independent, exact finite audit. No source-worker code or results imported.
Checks canonical n<=4 with evaluation vectors, cycle-count signs, and parity MITM.
Only Python standard library; all checks survive python -O.
"""
from itertools import permutations
from math import prod
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def sign_by_cycles(p):
    visited = set()
    cycles = 0
    for i in range(len(p)):
        if i in visited:
            continue
        cycles += 1
        j = i
        while j not in visited:
            visited.add(j)
            j = p[j]
        require(j == i, 'Input is not a permutation')
    return (-1) ** (len(p) - cycles)

def evaluation_vector(p):
    # Degree E is the sum of all exponents. E+1 distinct evaluations
    # identify every polynomial of degree <= E, over Q or R.
    degree = sum(p)
    return tuple(prod((x + i) ** exponent for i, exponent in enumerate(p))
                 for x in range(degree + 1))

def all_subset_sums(vectors, dimension):
    sums = [(0,) * dimension]
    for vector in vectors:
        sums.extend(tuple(a + b for a, b in zip(s, vector)) for s in sums[:])
    return sums

def digest(rows):
    return hashlib.sha256(json.dumps(rows, separators=(',', ':')).encode()).hexdigest()

def audit(n):
    ps = list(permutations(range(n)))
    require(len(ps) == len(set(ps)), 'Duplicate matching enumerated')
    degree = n * (n - 1) // 2
    rows = [{'matching': list(p), 'sign': sign_by_cycles(p),
             'evaluations': list(evaluation_vector(p))} for p in ps]
    signatures = [tuple(r['evaluations']) for r in rows]
    require(len(signatures) == len(set(signatures)), 'Two permutation polynomials coincide')
    even = [tuple(r['evaluations']) for r in rows if r['sign'] == 1]
    odd = [tuple(r['evaluations']) for r in rows if r['sign'] == -1]
    e_sums = all_subset_sums(even, degree + 1)
    o_sums = all_subset_sums(odd, degree + 1)
    e_set, o_set = set(e_sums), set(o_sums)
    common = e_set & o_set
    zero = (0,) * (degree + 1)
    require(common == {zero}, 'Nonempty cross-parity relation exists')
    require(e_sums.count(zero) == o_sums.count(zero) == 1,
            'Zero vector has a nonempty subset representation')
    # A second global determinant-sign test, not used to rule out relations.
    determinant = tuple(sum(r['sign'] * r['evaluations'][x] for r in rows)
                        for x in range(degree + 1))
    vandermonde = prod(j - i for i in range(n) for j in range(i + 1, n))
    require(determinant == (vandermonde,) * (degree + 1),
            'Cycle parity has inconsistent determinant orientation')
    return {'n': n, 'degree_bound': degree, 'evaluation_points': list(range(degree + 1)),
            'even_matchings': len(even), 'odd_matchings': len(odd),
            'even_subsets': len(e_sums), 'odd_subsets': len(o_sums),
            'distinct_even_subset_sums': len(e_set),
            'distinct_odd_subset_sums': len(o_set),
            'cross_parity_common_vectors': [list(v) for v in sorted(common)],
            'even_zero_subset_multiplicity': e_sums.count(zero),
            'odd_zero_subset_multiplicity': o_sums.count(zero),
            'even_subset_sums_sha256': digest(e_sums),
            'odd_subset_sums_sha256': digest(o_sums),
            'signed_full_sum_evaluations': list(determinant),
            'matchings': rows}

if __name__ == '__main__':
    report = {'status': 'PASS',
              'scope': 'Canonical offsets and exponents 0,...,n-1, n=1,2,3,4 only. No general progress.',
              'method': 'Exact integer evaluation at E+1 points; cycle-count parity; parity meet-in-the-middle.',
              'cases': [audit(n) for n in range(1, 5)]}
    (HERE / 'results.json').write_text(json.dumps(report, indent=2) + '\n')
    for c in report['cases']:
        print('n=%d: %d even subsets, %d odd subsets; intersection={zero}; only empty represents zero.'
              % (c['n'], c['even_subsets'], c['odd_subsets']))
    print('PASS: no nonempty canonical signed-matching subset relation for n<=4.')
    print('This is finite verification only. No claim for n>=5, arbitrary offsets/exponents, or P versus NP.')
