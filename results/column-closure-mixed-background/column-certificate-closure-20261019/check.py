#!/usr/bin/env python3
"""Exact, assertion-safe checks for the three-row closure classification."""

from fractions import Fraction as Q
from itertools import permutations, product
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return tuple(p)


def add(p, q):
    return trim(tuple((p[i] if i < len(p) else 0)
                      + (q[i] if i < len(q) else 0)
                      for i in range(max(len(p), len(q)))))


def scale(p, c):
    return trim(tuple(c * x for x in p))


def mul(p, q):
    out = [0] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            out[i + j] += x * y
    return trim(out)


def power(p, n):
    out = (1,)
    for _ in range(n):
        out = mul(out, p)
    return out


def evaluate(p, t):
    out = Q(0)
    for x in reversed(p):
        out = out * t + x
    return out


def coefficient(p, i):
    return p[i] if i < len(p) else 0


def sign(perm):
    inversions = sum(perm[i] > perm[j]
                     for i in range(len(perm))
                     for j in range(i + 1, len(perm)))
    return (-1) ** inversions


# The A, B, C, D, E, F order in the proof, not lexicographic order.
PERMS = ((0, 1, 2), (0, 2, 1), (1, 0, 2),
         (2, 0, 1), (1, 2, 0), (2, 1, 0))


def matching_terms(h, k, exponent_shift=0):
    x = ((-h, 1), (0, 1), (k, 1))
    terms = []
    for perm in PERMS:
        p = (sign(perm),)
        for i, j in enumerate(perm):
            p = mul(p, power(x[i], j + exponent_shift))
        terms.append(p)
    return tuple(terms)


def weighted_sum(terms, weights):
    out = (0,)
    for p, w in zip(terms, weights):
        out = add(out, scale(p, w))
    return out


def matching_weights(w):
    out = []
    for perm in PERMS:
        p = 1
        for i, j in enumerate(perm):
            p *= w[i][j]
        out.append(p)
    return tuple(out)


def polynomial_matrix(h, k, w, exponent_shift=0):
    x = ((-h, 1), (0, 1), (k, 1))
    return [[scale(power(x[i], j + exponent_shift), w[i][j])
             for j in range(3)] for i in range(3)]


def recursive_determinant(m):
    if not m:
        return (1,)
    out = (0,)
    for j in range(len(m)):
        minor = [[m[i][k] for k in range(len(m)) if k != j]
                 for i in range(1, len(m))]
        out = add(out, scale(mul(m[0][j], recursive_determinant(minor)),
                             (-1) ** j))
    return out


def gaussian_determinant(m):
    a = [[Q(x) for x in row] for row in m]
    out = Q(1)
    for i in range(len(a)):
        pivot = next((j for j in range(i, len(a)) if a[j][i]), None)
        if pivot is None:
            return Q(0)
        if pivot != i:
            a[pivot], a[i] = a[i], a[pivot]
            out = -out
        d = a[i][i]
        out *= d
        for j in range(i + 1, len(a)):
            ratio = a[j][i] / d
            for k in range(i + 1, len(a)):
                a[j][k] -= ratio * a[i][k]
            a[j][i] = 0
    return out


def column_contributions(terms, w, c):
    coeffs = matching_weights(w)
    return tuple(weighted_sum(terms,
                              tuple(coeffs[j] if PERMS[j][i] == c else 0
                                    for j in range(6)))
                 for i in range(3))


def weights_for_pair(pair, u, v):
    w = [[1, 1, 1] for _ in range(3)]
    for i in range(3):
        w[i][pair[0]] = u[i]
        w[i][pair[1]] = v[i]
    return w


def predicted_feasible_zero(pair, u, v, h, k):
    if pair == (0, 1):
        return (u[0] > 0 and v[1] > 0 and u[1] == 0
                and h * h * u[2] == k * k * u[0]
                and k * v[0] == (h + k) * v[1]
                and h * v[2] == (h + k) * v[1])
    if pair == (0, 2):
        return (u[0] > 0 and v[2] > 0 and u[1] == 0
                and h * u[2] == k * u[0]
                and h * v[0] == k * v[2]
                and h * v[1] == (h + k) * v[2])
    require(pair == (1, 2), "Unknown pair")
    return False


def check_named_certificates():
    terms = matching_terms(1, 1)
    full = [[1, 1, 1] for _ in range(3)]
    expected = (
        ((0, 1, 1), (2, 0, -2), (0, -1, 1)),
        ((1, 1, -2), (0, 0, 4), (1, -1, -2)),
        ((1, -2, 1), (0, 0, -2), (1, 2, 1)),
    )
    functionals = ((Q(3, 2), 1), (Q(3, 2), Q(1, 4)),
                   (Q(3, 2), Q(-1, 2)))
    for c in range(3):
        got = column_contributions(terms, full, c)
        require(got == expected[c], f"Full column {c} polynomial mismatch")
        a, b = functionals[c]
        require(all(a * coefficient(p, 0) + b * coefficient(p, 2) == 1
                    for p in got), f"Full column {c} functional fails")

    first = [[1, 1, 1], [0, 1, 1], [1, 1, 1]]
    s = column_contributions(terms, first, 1)
    require(s == ((0, 0, -1, 1), (0, 0, 4), (0, 0, -1, -1)),
            "Masked column-one polynomial mismatch")
    require(weighted_sum(s, (2, 1, 2)) == (0,), "Positive kernel fails")
    require(weighted_sum(s, (Q(2, 5), Q(1, 5), Q(2, 5))) == (0,),
            "Normalized positive kernel fails")
    require(weighted_sum(s, (1, 1, 1)) == (0, 0, 2),
            "First mask determinant fails")
    counts = tuple(sum(1 for perm, weight in zip(PERMS, matching_weights(first))
                       if perm[i] == 1 and weight > 0) for i in range(3))
    require(counts == (1, 2, 1), "Matching-extendability counts fail")
    for binary in product((0, 1), repeat=3):
        if any(binary):
            require(weighted_sum(s, binary) != (0,),
                    f"Unexpected binary subset cancellation: {binary}")
    only_second = weights_for_pair((0, 1), (1, 1, 1), (2, 1, 2))
    require(weighted_sum(terms, matching_weights(only_second)) == (4, 0, -4),
            "Second operation alone determinant mismatch")

    examples = [
        weights_for_pair((0, 1), (1, 0, 1), (2, 1, 2)),
        weights_for_pair((0, 2), (1, 0, 1), (1, 2, 1)),
        first, only_second, full,
    ]
    for w in examples:
        p = weighted_sum(terms, matching_weights(w))
        matrix = polynomial_matrix(1, 1, w)
        require(recursive_determinant(matrix) == p,
                "Independent recursive determinant disagrees")
        for t in (Q(-3), Q(-1), Q(0), Q(1), Q(3, 2), Q(4)):
            require(gaussian_determinant([[evaluate(e, t) for e in row]
                                          for row in matrix]) == evaluate(p, t),
                    "Independent rational Gaussian determinant disagrees")
    return {"full_column_functionals": 3, "new_column_matching_counts": counts,
            "positive_kernel": [2, 1, 2], "binary_column_subsets_checked": 7,
            "named_matrices_checked_independently": len(examples)}


def check_relation_and_subsets():
    gaps = ((Q(1), Q(1)), (Q(1), Q(2)), (Q(3), Q(1)),
            (Q(2, 3), Q(5, 7)), (Q(11, 4), Q(7, 6)))
    for h, k in gaps:
        terms = matching_terms(h, k)
        ray = (h * h, h * (h + k), 0, 0, k * (h + k), k * k)
        require(weighted_sum(terms, ray) == (0,), "General relation fails")
        for bits in product((0, 1), repeat=6):
            if any(bits):
                require(weighted_sum(terms, bits) != (0,),
                        f"Binary matching subset vanished at gaps {h,k}: {bits}")
        # Exact examples of each possible cancellation type, including unequal gaps.
        pairs = (
            ((0, 1), (h * h, 0, k * k),
             (h * (h + k), h * k, k * (h + k))),
            ((0, 2), (h, 0, k), (k, h + k, h)),
        )
        for pair, u, v in pairs:
            w = weights_for_pair(pair, u, v)
            require(any(matching_weights(w)), "General example lost feasibility")
            require(weighted_sum(terms, matching_weights(w)) == (0,),
                    "General two-column example fails")
            require(predicted_feasible_zero(pair, u, v, h, k),
                    "General example not recognized by classification")
        # Check that consecutive exponent shifts multiply every matching equally.
        for r in (1, 2):
            factor = mul(mul(power((-h, 1), r), power((0, 1), r)),
                         power((k, 1), r))
            shifted = matching_terms(h, k, r)
            require(shifted == tuple(mul(factor, p) for p in terms),
                    "Consecutive-exponent factorization fails")
    return {"positive_gap_pairs_checked": len(gaps),
            "binary_matching_subsets_checked": len(gaps) * 63,
            "general_cancellation_examples": len(gaps) * 2}


def check_bounded_classification():
    checked = 0
    feasible_zeros = {"0,1": 0, "0,2": 0, "1,2": 0}
    masks = tuple(product(range(3), repeat=3))
    for h, k in ((1, 1), (1, 2), (2, 1)):
        terms = matching_terms(h, k)
        for pair in ((0, 1), (0, 2), (1, 2)):
            for u in masks:
                for v in masks:
                    w = weights_for_pair(pair, u, v)
                    products = matching_weights(w)
                    feasible = any(products)
                    zero = weighted_sum(terms, products) == (0,)
                    expected = (not feasible or
                                predicted_feasible_zero(pair, u, v, h, k))
                    require(zero == expected,
                            f"Classification disagrees: gaps={h,k}, pair={pair},"
                            f" u={u}, v={v}, feasible={feasible}, zero={zero}")
                    if zero and feasible:
                        feasible_zeros[f"{pair[0]},{pair[1]}"] += 1
                    checked += 1
    return {"integer_weight_matrices_checked": checked,
            "weight_values": [0, 1, 2],
            "gap_pairs": [[1, 1], [1, 2], [2, 1]],
            "feasible_zero_counts": feasible_zeros}


def check_negative_controls():
    terms = matching_terms(1, 1)
    require(weighted_sum(terms, (1, 2, 0, 0, 2, 2)) != (0,),
            "Corrupted relation was not detected")
    wrong = ((0, 0, -1, 1), (0, 0, 5), (0, 0, -1, -1))
    require(weighted_sum(wrong, (2, 1, 2)) != (0,),
            "Corrupted middle cofactor was not detected")
    require(not predicted_feasible_zero((0, 1), (1, 0, 1), (1, 1, 1), 1, 1),
            "All-ones second mask incorrectly classified as a zero")
    return {"corruption_controls": 3}


def main():
    results = {"status": "PASS", "arithmetic": "exact integers and fractions",
               "named_certificates": check_named_certificates(),
               "general_identities": check_relation_and_subsets(),
               "bounded_classification": check_bounded_classification(),
               "negative_controls": check_negative_controls(),
               "scope": "Three-row consecutive-exponent classification; no general ASNC claim."}
    target = Path(__file__).with_name("results.json")
    target.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
