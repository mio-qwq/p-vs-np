#!/usr/bin/env python3
"""Exact, dependency-free depth-five XOR-matching obstruction certificate.

Run ordinary Python 3.10+ (not python -O): python3 check_depth_five.py.
Recomputes every reported value. No external packages, randomness or network.
"""
from collections import Counter
from itertools import combinations
from math import comb
import json

M = 5
N = 1 << M
T = 3
K = T * M
MODULUS = 0b100101  # X^5 + X^2 + 1


def remainder(a, b):
    while a.bit_length() >= b.bit_length():
        a ^= b << (a.bit_length() - b.bit_length())
    return a


def irreducible(p):
    d = p.bit_length() - 1
    if d < 1:
        return False
    return all(remainder(p, (1 << e) | low) != 0
               for e in range(1, d // 2 + 1) for low in range(1 << e))


def multiply(a, b, m=M, modulus=MODULUS):
    z = 0
    while b:
        if b & 1:
            z ^= a
        b >>= 1
        a <<= 1
        if a & (1 << m):
            a ^= modulus
    return z


def power(a, n, m=M, modulus=MODULUS):
    z = 1
    while n:
        if n & 1:
            z = multiply(z, a, m, modulus)
        a = multiply(a, a, m, modulus)
        n >>= 1
    return z


def trace(a, m=M, modulus=MODULUS):
    z = 0
    for _ in range(m):
        z ^= a
        a = multiply(a, a, m, modulus)
    assert z in (0, 1)
    return z


def xor_sum(values):
    s = 0
    for v in values:
        s ^= v
    return s


def rank(values):
    pivots = {}
    for v in values:
        while v:
            j = v.bit_length() - 1
            if j in pivots:
                v ^= pivots[j]
            else:
                pivots[j] = v
                break
    return len(pivots)


def affine_rank(values):
    values = list(values)
    assert values
    return rank(v ^ values[0] for v in values[1:])


def vector(x, m=M, modulus=MODULUS):
    return x | (power(x, 3, m, modulus) << m) | (power(x, 5, m, modulus) << (2 * m))


def evaluate(mask, constant, v):
    return ((mask & v).bit_count() & 1) ^ constant


def verify():
    assert __debug__, 'Run without -O: this checker relies on assertions.'
    assert irreducible(MODULUS)
    vectors = [vector(x) for x in range(N)]
    assert len(set(vectors)) == N
    assert affine_rank(vectors) == K

    # All 906,192 possible special-column row sets, directly checked.
    six_sum_counts = Counter()
    for rows in combinations(range(N), 6):
        total = xor_sum(vectors[x] for x in rows)
        assert total != 0, ('Unexpected zero six-subset', rows)
        six_sum_counts[total] += 1
    assert sum(six_sum_counts.values()) == comb(N, 6) == 906192

    # An independent collision check: equality of two distinct triple sums
    # would give a nonempty zero even subset of size at most six.
    triple_sums = [xor_sum(vectors[x] for x in rows)
                   for rows in combinations(range(N), 3)]
    assert len(triple_sums) == len(set(triple_sums)) == 4960

    # All 65,536 ambient affine functionals, not only distinct evaluations.
    weight_counts = Counter()
    sharp = None
    for mask in range(1 << K):
        w = sum((mask & v).bit_count() & 1 for v in vectors)
        for c, weight in ((0, w), (1, N - w)):
            weight_counts[weight] += 1
            if (mask, c) != (0, 0):
                assert weight >= 8, (mask, c, weight)
                if weight == 8 and sharp is None:
                    sharp = (mask, c)
    expected_weights = {0: 1, 8: 620, 12: 13888, 16: 36518,
                        20: 13888, 24: 620, 32: 1}
    assert weight_counts == expected_weights, weight_counts
    assert sum(weight_counts.values()) == 1 << (K + 1)
    assert sharp is not None
    sharp_rows = [x for x in range(N) if evaluate(*sharp, vectors[x])]
    assert len(sharp_rows) == 8
    sharp_remaining = [vectors[x] for x in range(N) if x not in sharp_rows]
    assert affine_rank(sharp_remaining) == 14

    # A separate small check of the actual subset-exchange directions for
    # every size 1 through 6 on the full row set. The proof applies this same
    # argument to every deletion set using the certified support bound.
    exchange_ranks = {}
    for r in range(1, 7):
        directions = [vectors[i] ^ vectors[j]
                      for i in range(r) for j in range(r, N)]
        exchange_ranks[r] = rank(directions)
        assert exchange_ranks[r] == K

    # Finite sanity checks of the disjoint-orbit lemma used by the general
    # self-contained proof. These supplement, not replace, its argument.
    orbit_parameter_checks = 0
    for t in range(1, 65):
        L = (2 * t - 1).bit_length()
        for m in range(2 * L, 2 * L + 3):
            modulus_exp = (1 << m) - 1
            occupied = set()
            for odd_exponent in range(1, 2 * t, 2):
                orbit = {(odd_exponent * (1 << r)) % modulus_exp for r in range(m)}
                assert len(orbit) == m
                assert not (orbit & occupied)
                assert 0 not in orbit
                occupied.update(orbit)
            assert (1 << (m - L)) >= 2 * t
            orbit_parameter_checks += 1
    assert orbit_parameter_checks == 192

    # Negative controls and explicit boundary witnesses.
    assert not irreducible(0b100011)
    without_fifth = [v & ((1 << (2 * M)) - 1) for v in vectors]
    zero_without_fifth = next(rows for rows in combinations(range(N), 6)
                             if xor_sum(without_fifth[x] for x in rows) == 0)
    assert xor_sum(vectors[x] for x in zero_without_fifth) != 0
    repeats = [0, 0, 1, 1, 2, 2]
    assert xor_sum(vectors[x] for x in repeats) == 0
    fixed_rows = list(range(6))
    fixed_total = xor_sum(vectors[x] for x in fixed_rows)
    assert fixed_total != 0

    # Small fields can have genuine cyclotomic trace degeneracies. GF(16),
    # with X^4+X+1, has Tr(x^5)=0 for every x and row affine rank only 10.
    m_small, modulus_small = 4, 0b10011
    assert irreducible(modulus_small)
    small_vectors = [vector(x, m_small, modulus_small) for x in range(1 << m_small)]
    assert all(trace(power(x, 5, m_small, modulus_small), m_small, modulus_small) == 0
               for x in range(1 << m_small))
    small_rank = affine_rank(small_vectors)
    assert small_rank == 10 < 3 * m_small

    return {
        'status': 'PASS',
        'field': {'size': N, 'degree': M, 'modulus_integer': MODULUS,
                  'modulus_polynomial': 'X^5 + X^2 + 1', 'irreducible': True},
        'graph': {'rows': N, 'columns': N, 'special_columns': list(range(6)),
                  'label_dimension': K, 'target': 0},
        'label_encoding': 'x | (x^3 << 5) | (x^5 << 10); field powers, integer bit shifts',
        'row_labels_in_integer_order': vectors,
        'row_affine_rank': K,
        'six_subsets_checked': sum(six_sum_counts.values()),
        'zero_six_subset_sums': 0,
        'distinct_six_subset_sums': len(six_sum_counts),
        'six_subset_sum_multiplicity_histogram': dict(sorted(Counter(six_sum_counts.values()).items())),
        'triple_subsets_checked': len(triple_sums),
        'distinct_triple_subset_sums': len(set(triple_sums)),
        'affine_functionals_checked': sum(weight_counts.values()),
        'affine_functional_weight_histogram': dict(sorted(weight_counts.items())),
        'minimum_nonzero_affine_functional_support': 8,
        'certified_row_deletion_robustness': 7,
        'certified_matching_conditioning_depth': 5,
        'subset_exchange_ranks_on_full_row_set': exchange_ranks,
        'general_lemma_orbit_parameter_sanity_checks': orbit_parameter_checks,
        'negative_controls': {
            'reducible_modulus_rejected': 0b100011,
            'zero_six_subset_after_dropping_fifth_power': list(zero_without_fifth),
            'zero_sum_with_illegal_repetitions': repeats,
            'depth_six_fixed_rows': fixed_rows,
            'depth_six_conditioned_hull_singleton': [fixed_total],
            'sharp_eight_deletion_mask': sharp[0],
            'sharp_eight_deletion_constant': sharp[1],
            'sharp_eight_deletion_rows': sharp_rows,
            'sharp_eight_deletion_remaining_affine_rank': affine_rank(sharp_remaining),
            'small_field': {'size': 16, 'modulus_integer': modulus_small,
                            'trace_of_fifth_power_identically_zero': True,
                            'actual_affine_rank': small_rank, 'ambient_dimension': 12},
        },
    }


if __name__ == '__main__':
    print(json.dumps(verify(), indent=2))
