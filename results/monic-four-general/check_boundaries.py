#!/usr/bin/env python3
"""Exact scope controls, not evidence by sampling for the unbounded theorem."""
from itertools import combinations
import sympy as s

x, w = s.symbols('x w')


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def determinant(rows, exponents, offsets):
    return s.expand(s.Matrix([
        [(x + offsets[i]) ** exponents[j] if rows[i] >> j & 1 else 0
         for j in range(4)] for i in range(4)]).det())


def main():
    offsets = (0, 1, w, -1-w)
    quadratic = w*w + w + 1
    polynomial = determinant((6, 15, 15, 15), (0, 1, 2, 3), offsets)
    require(all(s.rem(a, quadratic, w) == 0 for a in s.Poly(polynomial, x).all_coeffs()),
            'complex-offset counterexample is not zero')
    distinctness = s.prod(offsets[j] - offsets[i] for i, j in combinations(range(4), 2))
    require(s.degree(s.gcd(distinctness, quadratic), w) == 0,
            'complex counterexample offsets are not distinct')
    print('PASS: unrestricted complex-offset extension is false over Q[w]/(w^2+w+1).')
    require(determinant((15,)*4, (0, 1, 2, 4), (0, 1, 0, 2)) == 0,
            'repeated-offset control failed')
    print('PASS: dropping offset distinctness can give a zero determinant.')
    require(determinant((15,)*4, (0, 1, 1, 3), (0, 1, 2, 3)) == 0,
            'repeated-exponent control failed')
    print('PASS: dropping exponent distinctness can give a zero determinant.')
    require(determinant((0, 15, 15, 15), (0, 1, 2, 3), (0, 1, 2, 3)) == 0,
            'missing-matching control failed')
    print('PASS: dropping the perfect-matching hypothesis can give a zero determinant.')
    require(determinant((15,)*4, (0, 1, 2, 3), (0, 1, 2, 3)) == 12,
            'nonzero calibration failed')
    print('PASS: exact nonzero Vandermonde calibration equals 12.')


if __name__ == '__main__':
    main()
