#!/usr/bin/env python3
"""Standalone exact certificates; no third-party libraries or project imports."""
from itertools import permutations, product, combinations
from math import comb, factorial
from pathlib import Path
from random import Random
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def parity(p):
    return -1 if sum(p[i] > p[j] for i in range(len(p))
                     for j in range(i + 1, len(p))) % 2 else 1


def padd(a, b):
    c = [0] * max(len(a), len(b))
    for i, x in enumerate(a):
        c[i] += x
    for i, x in enumerate(b):
        c[i] += x
    while len(c) > 1 and c[-1] == 0:
        c.pop()
    return c


def pmul(a, b):
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] += x * y
    while len(c) > 1 and c[-1] == 0:
        c.pop()
    return c


def peval(a, z):
    answer = 0
    for x in reversed(a):
        answer = answer * z + x
    return answer


def det_permutations(a):
    n = len(a)
    total = 0
    for p in permutations(range(n)):
        term = parity(p)
        for i, j in enumerate(p):
            term *= a[i][j]
        total += term
    return total


def det_bareiss(a):
    n = len(a)
    if n == 0:
        return 1
    a = [row[:] for row in a]
    old, sign = 1, 1
    for k in range(n - 1):
        pivot_row = next((i for i in range(k, n) if a[i][k]), None)
        if pivot_row is None:
            return 0
        if pivot_row != k:
            a[k], a[pivot_row] = a[pivot_row], a[k]
            sign *= -1
        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = pivot * a[i][j] - a[i][k] * a[k][j]
                require(numerator % old == 0, "Bareiss division not exact")
                a[i][j] = numerator // old
        for i in range(k + 1, n):
            a[i][k] = 0
        old = pivot
    return sign * a[-1][-1]


def interpolate_integers(values):
    """Return n! times all coefficients, at sample nodes 0,...,n."""
    n = len(values) - 1
    out = [0] * (n + 1)
    for j, value in enumerate(values):
        basis = [1]
        for h in range(n + 1):
            if h != j:
                basis = pmul(basis, [-h, 1])
        scale = (-1) ** (n - j) * comb(n, j) * value
        for t, c in enumerate(basis):
            out[t] += scale * c
    return out


def fibers(n, edges):
    polys = [[0] for _ in range(n + 1)]
    witnesses = [[] for _ in range(n + 1)]
    for p in permutations(range(n)):
        if any((i, j) not in edges for i, j in enumerate(p)):
            continue
        target = sum(edges[i, j] for i, j in enumerate(p))
        term = [parity(p)]
        for i, j in enumerate(p):
            term = pmul(term, [comb(j, h) * i ** (j - h)
                               for h in range(j + 1)])
        polys[target] = padd(polys[target], term)
        witnesses[target].append(p)
    return polys, witnesses


def matrix(rows, cols, edges, x, ell):
    return [[x ** edges[i, j] * (ell + i) ** j
             if (i, j) in edges else 0 for j in cols] for i in rows]


def coefficient(rows, cols, edges, ell, target):
    m = len(rows)
    if target < 0 or target > m:
        return 0
    values = [det_bareiss(matrix(rows, cols, edges, x, ell))
              for x in range(m + 1)]
    numerator = interpolate_integers(values)[target]
    denominator = factorial(m)
    require(numerator % denominator == 0, "nonintegral coefficient")
    return numerator // denominator


def extract(n, edges, ell, target):
    rows, cols, result = list(range(n)), list(range(n)), []
    while rows:
        i = rows[0]
        current = coefficient(rows, cols, edges, ell, target)
        require(current != 0, "lost nonzero residual invariant")
        for pos, j in enumerate(cols):
            if (i, j) not in edges:
                continue
            newcols = cols[:pos] + cols[pos + 1:]
            residual = coefficient(rows[1:], newcols, edges, ell,
                                   target - edges[i, j])
            if (ell + i) ** j * residual:
                result.append((i, j))
                target -= edges[i, j]
                rows, cols = rows[1:], newcols
                break
        else:
            raise RuntimeError("no nonzero Laplace term")
    require(target == 0, "incorrect final target")
    return result


def check_interpolation_and_extraction():
    cases = []
    # All ternary masks/colors on 2x2.
    for values in product(range(3), repeat=4):
        cases.append((2, {(i, j): values[2 * i + j] - 1
                          for i in range(2) for j in range(2)
                          if values[2 * i + j]}))
    # All binary colorings on K3,3.
    for values in product(range(2), repeat=9):
        cases.append((3, {(i, j): values[3 * i + j]
                          for i in range(3) for j in range(3)}))
    rng = Random(20261019)
    for n in [3, 4]:
        for _ in range(48):
            values = [rng.randrange(3) for _ in range(n * n)]
            cases.append((n, {(i, j): values[n * i + j] - 1
                              for i in range(n) for j in range(n)
                              if values[n * i + j]}))
    evaluations = extractions = 0
    for n, edges in cases:
        polys, witnesses = fibers(n, edges)
        seen = [None] * (n + 1)
        for ell in range(n * (n - 1) // 2 + 1):
            vals = []
            for x in range(n + 1):
                a = matrix(range(n), range(n), edges, x, ell)
                value = det_bareiss(a)
                require(value == det_permutations(a), "determinant disagreement")
                vals.append(value)
                evaluations += 1
            nums = interpolate_integers(vals)
            for t in range(n + 1):
                require(nums[t] == factorial(n) * peval(polys[t], ell),
                        "interpolation disagreement")
                if nums[t] and seen[t] is None:
                    seen[t] = ell
        for t, poly in enumerate(polys):
            require((seen[t] is not None) == any(poly), "grid root bound failure")
            # Only a finite corroboration; no general ASNC assertion follows.
            require(any(poly) == bool(witnesses[t]), "small-instance ASNC failure")
            if seen[t] is not None:
                matching = extract(n, edges, seen[t], t)
                require(len(matching) == n and len({j for _, j in matching}) == n,
                        "extraction did not produce a matching")
                require(sum(edges[e] for e in matching) == t, "wrong extracted color")
                extractions += 1
    return {"graphs": len(cases), "determinant_evaluations": evaluations,
            "extracted_matchings": extractions}


def enumerate_labeled(rows, cols, records):
    """Each record is (edge_id,row,column,color), with no parallel test edges."""
    pairs = {(r, c): (eid, color) for eid, r, c, color in records}
    result = []
    for perm in permutations(cols):
        if all((r, c) in pairs for r, c in zip(rows, perm)):
            chosen = [pairs[r, c] for r, c in zip(rows, perm)]
            result.append({"ids": sorted(e for e, _ in chosen),
                           "red": sum(color for _, color in chosen)})
    return result


def check_cut():
    original = [(0, "a0", "b0", 1), (1, "a1", "b0", 0),
                (2, "a1", "b1", 0), (3, "a2", "b1", 0),
                (4, "a2", "b2", 1), (5, "a0", "b2", 0)]
    shore = {"a0", "b0", "a1"}
    cut = {eid for eid, r, c, _ in original if (r in shore) != (c in shore)}
    require(cut == {2, 5}, "wrong tight cut")
    matchings = enumerate_labeled(["a0", "a1", "a2"], ["b0", "b1", "b2"], original)
    require({m["red"] for m in matchings} == {0, 2}, "wrong true count set")
    require(len(matchings) == 2, "six-cycle should have two matchings")
    for m in matchings:
        require(len(set(m["ids"]) & cut) == 1, "cut is not tight")
    require(set().union(*(set(m["ids"]) for m in matchings)) == set(range(6)),
            "not matching-covered")
    left = [(eid, r, c if c in shore else "starB", color)
            for eid, r, c, color in original if r in shore]
    right = [(eid, r if r not in shore else "starA", c, color)
             for eid, r, c, color in original if c not in shore]
    lm = enumerate_labeled(["a0", "a1"], ["b0", "starB"], left)
    rm = enumerate_labeled(["starA", "a2"], ["b1", "b2"], right)
    require(len(left) == len(right) == 4, "contractions not four-cycles")
    require({m["red"] for m in lm} == {0, 1}, "wrong left count set")
    require({m["red"] for m in rm} == {0, 1}, "wrong right count set")
    naive = {l["red"] + r["red"] for l in lm for r in rm}
    good, bad = set(), []
    for l in lm:
        for r in rm:
            le = set(l["ids"]) & cut
            re = set(r["ids"]) & cut
            if le == re:
                merged = set(l["ids"]) | set(r["ids"])
                require(any(merged == set(m["ids"]) for m in matchings), "bad gluing")
                good.add(l["red"] + r["red"])
            else:
                bad.append([l, r])
    require(naive == {0, 1, 2} and good == {0, 2}, "recurrence check failed")
    neighbors = {r: {c for _, rr, c, _ in original if rr == r}
                 for r in ["a0", "a1", "a2"]}
    for size in [1, 2]:
        for subset in combinations(neighbors, size):
            require(len(set().union(*(neighbors[r] for r in subset))) > size,
                    "there is a balanced proper Hall block")
    return {"matchings": matchings, "cut_edge_ids": sorted(cut),
            "left_block": lm, "right_block": rm,
            "naive_counts": sorted(naive), "compatible_counts": sorted(good),
            "incompatible_pairs": bad, "strict_proper_Hall": True,
            "side_size_sum": 4, "original_side_size": 3}


def check_subset_sum():
    samples = [(1,), (2, 3), (2, 5, 9), (1, 1, 2, 7), (1, 2**80, 2**81 + 3)]
    output = []
    for weights in samples:
        r = len(weights)
        records = []
        for h, weight in enumerate(weights):
            for i in range(2):
                for j in range(2):
                    records.append((4*h+2*i+j, 2*h+i, 2*h+j,
                                    weight if i == j == 0 else 0))
        matches = enumerate_labeled(range(2*r), range(2*r), records)
        subsets = [sum(weights[h] for h, bit in enumerate(bits) if bit)
                   for bits in product([0, 1], repeat=r)]
        require(sorted(m["red"] for m in matches) == sorted(subsets),
                "subset-sum matching bijection failure")
        require(len(matches) == 2**r, "wrong number of component choices")
        output.append({"weights": list(weights), "subset_totals": sorted(subsets),
                       "vertices_per_side": 2*r, "edges": 4*r,
                       "weight_input_bits": sum(w.bit_length() for w in weights),
                       "path_gadget_internal_vertices": 2*sum(weights)})
    return output


def main():
    report = {"status": "PASS", "scope": "finite certificates, not universal ASNC",
              "tight_cut": check_cut(),
              "subset_sum": check_subset_sum(),
              "interpolation_and_extraction": check_interpolation_and_extraction()}
    target = Path(__file__).with_name("results.json")
    target.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": report["status"],
                      "tight_cut_counts": report["tight_cut"]["compatible_counts"],
                      "naive_counts": report["tight_cut"]["naive_counts"],
                      **report["interpolation_and_extraction"]}, sort_keys=True))


if __name__ == "__main__":
    main()
