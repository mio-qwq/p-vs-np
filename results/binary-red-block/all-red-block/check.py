#!/usr/bin/env python3
"""Independent standard-library exact check of full-square red-block theorem."""
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, permutations
from math import comb, factorial, prod
from pathlib import Path
import hashlib
import json
import sys


def trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return tuple(p)


def plus(p, q):
    r = [Fraction(0)] * max(len(p), len(q))
    for i, x in enumerate(p):
        r[i] += x
    for i, x in enumerate(q):
        r[i] += x
    return trim(r)


def scale(p, c):
    return trim([c * x for x in p])


def times(p, q):
    r = [Fraction(0)] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            r[i + j] += x * y
    return trim(r)


def entry(a, e):
    return tuple(Fraction(comb(e, d)) * a ** (e - d)
                 for d in range(e + 1))


def permutation_sign(p):
    return (-1) ** sum(p[i] > p[j] for i in range(len(p))
                       for j in range(i + 1, len(p)))


def delta(xs):
    return prod((xs[j] - xs[i] for i in range(len(xs))
                 for j in range(i + 1, len(xs))), start=Fraction(1))


def verify_case(name, offsets, exponents, row_set, column_set):
    a = tuple(map(Fraction, offsets))
    e = tuple(exponents)
    n = len(a)
    I, J = tuple(sorted(row_set)), tuple(sorted(column_set))
    k = len(I)
    if not (len(e) == n and len(J) == k and 0 <= k <= n // 2):
        raise ValueError("Bad theorem dimensions")
    if len(set(a)) != n or len(set(e)) != n or min(e) < 0:
        raise ValueError("Bad labels")
    V = tuple(tuple(entry(a[i], e[j]) for j in range(n)) for i in range(n))
    fibers = [(Fraction(0),) for _ in range(k + 1)]
    counts = [[0, 0] for _ in range(k + 1)]
    for p in permutations(range(n)):
        t = sum(i in I and p[i] in J for i in range(n))
        sign = permutation_sign(p)
        term = (Fraction(sign),)
        for i in range(n):
            term = times(term, V[i][p[i]])
        fibers[t] = plus(fibers[t], term)
        counts[t][0 if sign == 1 else 1] += 1

    @lru_cache(None)
    def minor(rows, cols):
        if not rows:
            return (Fraction(1),)
        result = (Fraction(0),)
        for q, col in enumerate(cols):
            term = times(V[rows[0]][col], minor(rows[1:], cols[:q] + cols[q+1:]))
            result = plus(result, scale(term, (-1) ** q))
        return result

    laplace = [(Fraction(0),) for _ in range(k + 1)]
    summands = []
    for s in range(k + 1):
        expected_s_degree = sum(e) - comb(s, 2) - comb(n-s, 2)
        for A in combinations(I, s):
            for B in combinations(J, s):
                Ac = tuple(i for i in range(n) if i not in A)
                Bc = tuple(j for j in range(n) if j not in B)
                term = scale(times(minor(A, B), minor(Ac, Bc)),
                             (-1) ** (sum(A) + sum(B)))
                if term == (0,) or len(term)-1 != expected_s_degree:
                    raise RuntimeError((name, "wrong summand degree", A, B))
                for t in range(s + 1):
                    laplace[t] = plus(laplace[t], scale(term, (-1) ** (s-t) * comb(s, t)))
                summands.append({"s": s, "rows": A, "cols": B,
                                 "degree": len(term)-1, "leading_coefficient": str(term[-1])})
    if fibers != laplace:
        raise RuntimeError((name, "direct-permutation/Laplace mismatch"))

    Ic = tuple(i for i in range(n) if i not in I)
    Jc = tuple(j for j in range(n) if j not in J)
    predicted_degree = sum(e) - comb(k, 2) - comb(n-k, 2)
    core = (delta([a[i] for i in I]) * delta([e[j] for j in J])
            * delta([a[i] for i in Ic]) * delta([e[j] for j in Jc])
            / (prod(factorial(r) for r in range(k))
               * prod(factorial(r) for r in range(n-k))))
    targets = []
    for t, p in enumerate(fibers):
        predicted_lc = (-1) ** (sum(I)+sum(J)+k-t) * comb(k, t) * core
        if p == (0,) or len(p)-1 != predicted_degree or p[-1] != predicted_lc:
            raise RuntimeError((name, t, "theorem mismatch"))
        if n-k >= 2 and counts[t][0] != counts[t][1]:
            raise RuntimeError((name, t, "parity imbalance"))
        targets.append({"t": t, "degree": len(p)-1,
                        "leading_coefficient": str(p[-1]),
                        "even_count": counts[t][0], "odd_count": counts[t][1],
                        "coefficients_low_to_high": list(map(str, p))})
    return {"name": name, "n": n, "k": k, "a": list(map(str, a)), "e": e,
            "I": I, "J": J, "predicted_degree": predicted_degree,
            "targets": targets, "laplace_summands": summands}


CASES = [
    ("standard_4_by_4_red_2_block", range(4), range(4), (0, 1), (0, 1)),
    ("odd_order_nonprincipal_gapped_exponents", (3, -2, 5, 0, 7), (4, 0, 7, 1, 3), (0, 3), (1, 3)),
    ("standard_6_by_6_red_3_block", range(6), range(6), (0, 1, 2), (0, 1, 2)),
    ("even_order_below_half_nonprincipal", (-3, 2, 7, 0, 5, -1), (6, 2, 0, 5, 1, 8), (1, 5), (0, 3)),
    ("rational_offsets_reordered_exponents", ("1/2", "-2/3", "7/4", "-5/2"), (3, 0, 5, 1), (0, 2), (1, 2)),
    ("empty_red_block", (-1, 4, 0, 2), (5, 0, 2, 1), (), ()),
    ("one_red_edge_order_two", (-2, 3), (4, 1), (1,), (0,)),
    ("order_one_empty_block", (3,), (2,), (), ()),
]


def main():
    results = [verify_case(*case) for case in CASES]
    boundary = results[0]["targets"][1]["coefficients_low_to_high"]
    if boundary != list(map(str, (-24, -60, -38, -12, -2))):
        raise RuntimeError("Original singular 2x2 boundary polynomial mismatch")
    report = {"checks": "All exact checks passed", "case_count": len(results),
              "target_count": sum(len(r["targets"]) for r in results),
              "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "results": results}
    output = Path(sys.argv[1] if len(sys.argv) > 1 else "results.json")
    output.write_text(json.dumps(report, indent=2) + "\n")
    for r in results:
        print(r["name"], "degree", r["predicted_degree"],
              "leading coefficients", [t["leading_coefficient"] for t in r["targets"]])
    print(f"PASS: {len(results)} cases, {report['target_count']} target fibers")


if __name__ == "__main__":
    main()
