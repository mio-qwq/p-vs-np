#!/usr/bin/env python3
"""Exact checks for the general quadratic-base power obstruction.

These are implementation checks, not the source of the universal quantifiers.
No Python assert is used, so python -O performs the same checks.
"""
from fractions import Fraction
from math import comb, prod
import sympy as S


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


n, c, z, t, L = S.symbols('n c z t L')


def check_formal_recurrence(s):
    # Scale covariance permits c=1; all degree-j terms acquire the factor c^j.
    b = [S.Integer(1)]
    for j in range(1, s + 1):
        b.append(S.expand(b[-1] * (n + 2*j - 2) * (n + 2*j - 1)
                          / (2*j*(2*s - 2*j + 1))))
    r = [S.Integer(0)]
    for j in range(1, s + 1):
        r.append(S.expand(j*b[j] - sum(r[i]*b[j-i] for i in range(1, j))))
    for j in range(1, s + 1):
        rhs = sum(r[i]*r[j-i] for i in range(1, j))
        rhs += (j-1+n+S.Rational(1,2))*r[j-1]
        rhs += sum(r[i]*r[j-1-i] for i in range(1, j-1))
        if j == 1:
            rhs += n*(n+1)/4
        require(S.expand((s+S.Rational(1,2)-j)*r[j]-rhs) == 0,
                f'Logarithmic recurrence fails at s={s},j={j}')
        require(all(a >= 0 for a in S.Poly(r[j], n).all_coeffs()),
                f'Unexpected nonpositive symbolic power-sum coefficient s={s},j={j}')
    difference = S.Poly(S.expand(2*r[s] - 4*r[1]*r[s-1]), n)
    require(all(a >= 0 for a in difference.all_coeffs()) and difference.eval(1) > 0,
            f'Final contradiction is not strict at s={s}')


def check_exact_scaled_recurrence(s, count, scale):
    b = [Fraction(1)]
    for j in range(1, s+1):
        b.append(b[-1]*scale*Fraction((count+2*j-2)*(count+2*j-1),
                                     2*j*(2*s-2*j+1)))
    r = [Fraction(0)]
    for j in range(1, s+1):
        r.append(j*b[j]-sum(r[i]*b[j-i] for i in range(1,j)))
        rhs = sum(r[i]*r[j-i] for i in range(1,j))
        rhs += scale*((j-1+count+Fraction(1,2))*r[j-1]
                      +sum(r[i]*r[j-1-i] for i in range(1,j-1))
                      +(Fraction(count*(count+1),4) if j==1 else 0))
        require((s+Fraction(1,2)-j)*r[j] == rhs,
                'Scaled recurrence failed')
    require(2*r[s] > 4*r[1]*r[s-1], 'Required real-knot inequality not contradicted')


def homogeneous_coefficients(knots, degree):
    h = [S.Integer(1)] + [S.Integer(0)]*degree
    for a in knots:
        for j in range(1, degree+1):
            h[j] = S.expand(h[j] + a*h[j-1])
    return h


def check_translation(knots, d):
    count = len(knots)
    offsets_h = homogeneous_coefficients(knots,d)
    direct = homogeneous_coefficients([L+a for a in knots],d)[d]
    transformed = sum(S.binomial(count+d-1,d-j)*offsets_h[j]*L**(d-j)
                      for j in range(d+1))
    require(S.expand(direct-transformed)==0, 'Translation moment formula failed')
    monic = S.Poly(direct,L).monic().as_expr()
    require(S.expand(monic.coeff(L,d-2)
                     -S.binomial(d,2)*2*offsets_h[2]/(count*(count+1)))==0,
            'Variance coefficient normalization failed')


for s in range(2,13):
    check_formal_recurrence(s)
for s in range(2,31):
    for count in (2,3,9,31):
        for scale in (Fraction(1), Fraction(3,7)):
            check_exact_scaled_recurrence(s,count,scale)
for knots in ((-1,1),(-2,-1,3),(-3,-1,1,3),(-30,-3,-2,-1,0,1,2,3,30)):
    for d in (4,6,10):
        check_translation(knots,d)
print('PASS: symbolic recurrence, exact scaled recurrence, strict moment obstruction, translation formula')
