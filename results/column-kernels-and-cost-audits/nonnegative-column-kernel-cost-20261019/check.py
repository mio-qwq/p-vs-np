#!/usr/bin/env python3
"""Verify the exact positive-functional example, without an LP library."""
from fractions import Fraction
from itertools import permutations
from math import comb
from pathlib import Path
import json


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def multiply(a, b):
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] += x*y
    return c


def main():
    offsets, exponents, column = (-3, -1, 1, 3), (0, 1, 2, 4), 1
    degree_bound = sum(exponents)
    terms = [[0] * (degree_bound + 1) for _ in offsets]
    for p in permutations(range(4)):
        inversions = sum(p[i] > p[j] for i in range(4) for j in range(i+1, 4))
        polynomial = [(-1) ** inversions]
        for row, col in enumerate(p):
            exponent, offset = exponents[col], offsets[row]
            polynomial = multiply(polynomial,
                                  [comb(exponent, h) * offset**(exponent-h)
                                   for h in range(exponent + 1)])
        chosen_row = p.index(column)
        for h, coefficient in enumerate(polynomial):
            terms[chosen_row][h] += coefficient
    expected = [[0, 768, 896, 0, -128], [0, 768, -1152, 0, 384],
                [0, 768, 1152, 0, -384], [0, 768, -896, 0, 128]]
    for actual, wanted in zip(terms, expected):
        require(actual == wanted + [0] * (degree_bound + 1 - len(wanted)),
                "Laplace polynomial mismatch")
    signed_kernel = [1, -1, -1, 1]
    for h in range(degree_bound + 1):
        require(sum(signed_kernel[s] * terms[s][h] for s in range(4)) == 0,
                "signed relation mismatch")
    y = [Fraction(0)] * (degree_bound + 1)
    y[1] = Fraction(1, 768)
    values = [sum(y[h] * t[h] for h in range(degree_bound + 1)) for t in terms]
    require(values == [1] * 4, "positive-functional certificate mismatch")
    # Generic linear-algebra control; not claimed to come from a Vandermonde mask.
    control_columns = [[1], [-1]]
    control_u = [Fraction(1, 2), Fraction(1, 2)]
    require(sum(control_u) == 1 and all(u >= 0 for u in control_u), "bad control")
    require(sum(control_u[i] * control_columns[i][0] for i in range(2)) == 0,
            "negative-control kernel failed")
    report = {"status": "PASS", "offsets": offsets, "exponents": exponents,
              "distinguished_column": column, "laplace_polynomials": terms,
              "signed_kernel": signed_kernel,
              "positive_functional": {"coefficient_index": 1, "weight": "1/768"},
              "positive_values": [str(v) for v in values],
              "scope": "one exact certificate plus a generic linear-algebra control"}
    Path(__file__).with_name("results.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "functional_values": report["positive_values"]}))


if __name__ == "__main__":
    main()
