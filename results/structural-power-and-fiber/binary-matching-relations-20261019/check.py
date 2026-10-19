#!/usr/bin/env python3
"""Exact, standard-library certificate for canonical four-row binary noncancellation.

No assertion statements, floating point, optimizer, or third-party dependencies.
The two meet-in-middle checks construct terms independently: one from polynomial
convolution, the other from values at seven distinct integer points.
"""

from collections import defaultdict
from itertools import permutations
from math import comb, prod
from pathlib import Path
import hashlib
import json


HERE = Path(__file__).resolve().parent
N = 4
DEGREE = 6
PERMS = list(permutations(range(N)))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def parity(p):
    return (-1) ** sum(p[i] > p[j] for i in range(N) for j in range(i + 1, N))


def multiply(a, b):
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] += x * y
    return tuple(c)


def coefficient_vector(p):
    v = (1,)
    for row, exponent in enumerate(p):
        v = multiply(v, tuple(comb(exponent, j) * row ** (exponent - j)
                              for j in range(exponent + 1)))
    return v


def subset_sums(vectors):
    sums = [(0,) * len(vectors[0])]
    for vector in vectors:
        sums += [tuple(a + b for a, b in zip(s, vector)) for s in sums]
    return sums


def meet_in_middle(vectors, label):
    positive_indices = [i for i, p in enumerate(PERMS) if parity(p) == 1]
    negative_indices = [i for i, p in enumerate(PERMS) if parity(p) == -1]
    require(len(positive_indices) == len(negative_indices) == 12,
            label + ': incorrect parity partition')
    positive_sums = subset_sums([vectors[i] for i in positive_indices])
    negative_sums = subset_sums([vectors[i] for i in negative_indices])
    negative_lookup = defaultdict(list)
    for mask, vector in enumerate(negative_sums):
        negative_lookup[vector].append(mask)
    hits = [(pm, nm) for pm, vector in enumerate(positive_sums)
            for nm in negative_lookup.get(vector, [])]
    require(hits == [(0, 0)], label + ': unexpected binary relation ' + repr(hits))
    payload = json.dumps([positive_sums, negative_sums], separators=(',', ':')).encode()
    return {
        'positive_subset_count': len(positive_sums),
        'negative_subset_count': len(negative_sums),
        'distinct_positive_sums': len(set(positive_sums)),
        'distinct_negative_sums': len(set(negative_sums)),
        'equal_subset_mask_pairs': hits,
        'ordered_subset_vectors_sha256': hashlib.sha256(payload).hexdigest(),
    }


def chosen_permutations(mask):
    return [p for i, p in enumerate(PERMS) if (mask >> i) & 1]


def coefficient_branching(signed):
    states = [(0, (0,) * (DEGREE + 1))]
    report = []
    expected_masks = [[0, 23], [0, 1303], [0], [0, 6029312], [0], [0], [0]]
    for r in range(N):
        indices = [i for i, p in enumerate(PERMS) if p[0] == r]
        require(len(indices) == 6, 'incorrect valuation group')
        group_sums = [(0, (0,) * (DEGREE + 1))]
        for i in indices:
            require(all(signed[i][j] == 0 for j in range(r)),
                    'valuation condition failed')
            group_sums += [(mask | (1 << i), tuple(x + y for x, y in zip(v, signed[i])))
                           for mask, v in group_sums]
        states = [(mask | submask, tuple(x + y for x, y in zip(v, w)))
                  for mask, v in states for submask, w in group_sums
                  if v[r] + w[r] == 0]
        require(sorted(mask for mask, _ in states) == expected_masks[r],
                'unexpected partial subsets at coefficient ' + str(r))
        report.append({
            'coefficient': r,
            'processed_row_zero_exponents': list(range(r + 1)),
            'survivors': [{'mask': m, 'permutations': chosen_permutations(m),
                           'signed_coefficient_sum': v} for m, v in states],
        })
    for r in range(N, DEGREE + 1):
        states = [(mask, v) for mask, v in states if v[r] == 0]
        require(sorted(mask for mask, _ in states) == expected_masks[r],
                'unexpected final subsets at coefficient ' + str(r))
        report.append({
            'coefficient': r,
            'processed_row_zero_exponents': list(range(N)),
            'survivors': [{'mask': m, 'permutations': chosen_permutations(m),
                           'signed_coefficient_sum': v} for m, v in states],
        })
    require(states == [(0, (0,) * (DEGREE + 1))], 'branching did not exclude every nonempty subset')
    return report


def leading_subset_tables(signed):
    tables = []
    expected_intersections = [[0, 126], [0], [0], [0, 21]]
    for r in range(N):
        p = [v[r] for p, v in zip(PERMS, signed) if p[0] == r and v[r] > 0]
        n = [-v[r] for p, v in zip(PERMS, signed) if p[0] == r and v[r] < 0]
        ps = sorted(x[0] for x in subset_sums([(x,) for x in p]))
        ns = sorted(x[0] for x in subset_sums([(x,) for x in n]))
        equal = sorted(set(ps) & set(ns))
        require(equal == expected_intersections[r], 'incorrect scalar subset table')
        if r == 1:
            require(sorted(set(ps) & {x + 18 for x in ns}) == [27],
                    'incorrect group-one completion of first nonempty branch')
        if r == 2:
            require(not (set(ps) & {x - 9 for x in ns}),
                    'nonempty branch should die in group two')
        tables.append({'row_zero_exponent': r, 'positive_values': p,
                       'negative_magnitudes': n, 'positive_subset_sums': ps,
                       'negative_subset_sums': ns, 'equal_subset_values': equal})
    return tables


def main():
    unsigned = [coefficient_vector(p) for p in PERMS]
    require(all(len(v) == DEGREE + 1 and v[-1] == 1 for v in unsigned),
            'wrong degree or leading coefficient')
    signed = [tuple(parity(p) * x for x in v) for p, v in zip(PERMS, unsigned)]
    full_sum = tuple(sum(v[j] for v in signed) for j in range(DEGREE + 1))
    require(full_sum == (12, 0, 0, 0, 0, 0, 0), 'Vandermonde normalization failed')

    # Independent construction: direct products, no polynomial arithmetic.
    evaluation_vectors = [tuple(prod((t + i) ** p[i] for i in range(N))
                                for t in range(DEGREE + 1)) for p in PERMS]
    for coeffs, values in zip(unsigned, evaluation_vectors):
        require(values == tuple(sum(c * t ** j for j, c in enumerate(coeffs))
                                for t in range(DEGREE + 1)),
                'coefficient/evaluation construction mismatch')

    result = {
        'definition': 'sgn(p) * product((L+i)**p[i] for i in range(4)); p maps rows to exponents',
        'offsets': [0, 1, 2, 3],
        'exponents': [0, 1, 2, 3],
        'coefficient_order': 'ascending powers L^0 through L^6',
        'terms': [{'index': i, 'permutation': p, 'sign': parity(p), 'signed_coefficients': v}
                  for i, (p, v) in enumerate(zip(PERMS, signed))],
        'coefficient_meet_in_middle': meet_in_middle(unsigned, 'coefficients'),
        'truncated_coefficient_meet_in_middle': meet_in_middle([v[:5] for v in unsigned], 'L0..L4'),
        'seven_point_evaluation_meet_in_middle': meet_in_middle(evaluation_vectors, 'evaluations'),
        'leading_subset_tables': leading_subset_tables(signed),
        'coefficient_branching': coefficient_branching(signed),
        'scope': 'Canonical n=4; affine equally-spaced offsets and consecutive exponents follow by algebraic substitution. No claim for arbitrary offsets or arbitrary n.',
        'status': 'PASS: only the empty binary relation exists',
    }
    path = HERE / 'results.json'
    path.write_text(json.dumps(result, indent=2) + '\n')
    print(result['status'])
    print('Parity meet-in-middle: 4096 + 4096 exact sums; empty/empty is the only equality.')
    print('Independent seven-point check: same result.')
    print('Valuation-branching survivor counts:',
          [len(s['survivors']) for s in result['coefficient_branching']])
    print('Exact terms and certificate:', path)


if __name__ == '__main__':
    main()
