"""Independent auditor checks; no imports from the checkpoint's other code."""
from fractions import Fraction
from itertools import combinations
from math import factorial, prod
import json
import random


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def det(matrix):
    a = [list(map(Fraction, row)) for row in matrix]
    n = len(a)
    value = Fraction(1)
    for k in range(n):
        pivot = next((i for i in range(k, n) if a[i][k]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            value = -value
        p = a[k][k]
        value *= p
        for i in range(k + 1, n):
            ratio = a[i][k] / p
            for j in range(k + 1, n):
                a[i][j] -= ratio * a[k][j]
    return value


def vand(values):
    return prod(values[j] - values[i] for i in range(len(values)) for j in range(i + 1, len(values)))


def multiply(a, b):
    c = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, u in enumerate(a):
        for j, v in enumerate(b):
            c[i+j] += u*v
    return c


def root_polynomial(values):
    f = [Fraction(1)]
    for x in values:
        f = multiply(f, [-x, 1])
    return f


def remainder_power(h, roots):
    f = root_polynomial(roots)
    s = len(roots)
    coeff = [Fraction(0)] * max(h + 1, s)
    coeff[h] = 1
    for d in range(h, s-1, -1):
        lead = coeff[d]
        for j in range(s+1):
            coeff[d-s+j] -= lead * f[j]
    return coeff[:s]


def interpolate(values):
    """Power coefficients from exact values at x = 0, 1, ..., degree."""
    degree = len(values) - 1
    output = [Fraction(0)] * (degree+1)
    differences = list(map(Fraction, values))
    falling = [Fraction(1)]
    for k in range(degree+1):
        factor = differences[0] / factorial(k)
        for j, c in enumerate(falling):
            output[j] += factor*c
        differences = [differences[j+1]-differences[j] for j in range(len(differences)-1)]
        falling = multiply(falling, [-k, 1])
    while len(output) > 1 and output[-1] == 0:
        output.pop()
    return output


def st_direct(exponents, chosen, r):
    n = len(exponents)
    S = T = Fraction(0)
    for B in combinations(chosen, r):
        rest = [i for i in range(n) if i not in B]
        w = (-1)**sum(B) * vand([exponents[i] for i in B]) * vand([exponents[i] for i in rest])
        S += w
        T += w * sum(exponents[i] for i in B)
    return S, T


def quotient_matrix(exponents, chosen, r):
    X = [exponents[i] for i in chosen]
    Y = [exponents[i] for i in range(len(exponents)) if i not in chosen]
    K = []
    for h in range(r, len(exponents)-r):
        cx = remainder_power(h, X)
        cy = remainder_power(h, Y)
        K.append(cx[r:] + cy[r:])
    return K, X, Y


def elementary2(values):
    return sum(u*v for u, v in combinations(values, 2))


rng = random.Random(20261018)
quotient_cases = 0
weighted_cases = 0
for n in range(3, 13):
    for r in range(1, (n-1)//2 + 1):
        for s in range(r+1, n-r+1):
            exponents = rng.sample(range(0, 3*n+4), n)
            chosen = sorted(rng.sample(range(n), s))
            S, T = st_direct(exponents, chosen, r)
            K, X, Y = quotient_matrix(exponents, chosen, r)
            p = s-r
            predicted = (-1)**(sum(chosen)+p*(p-1)//2)*vand(X)*vand(Y)*det(K)
            require(S == predicted, ('quotient', n, r, s, exponents, chosen, S, predicted))
            quotient_cases += 1
            if n == 2*r+2 and s == r+1:
                predicted_T = (-1)**sum(chosen)*vand(X)*vand(Y)*(elementary2(Y)-elementary2(X))
                require(T == predicted_T, ('weighted', n, r, exponents, chosen, T, predicted_T))
                weighted_cases += 1
for r in range(1, 6):
    n = 2*r+2
    for _ in range(10):
        exponents = rng.sample(range(0, 4*n+3), n)
        chosen = sorted(rng.sample(range(n), r+1))
        _, T = st_direct(exponents, chosen, r)
        X = [exponents[i] for i in chosen]
        Y = [exponents[i] for i in range(n) if i not in chosen]
        predicted_T = (-1)**sum(chosen)*vand(X)*vand(Y)*(elementary2(Y)-elementary2(X))
        require(T == predicted_T, ('weighted extra', r, T, predicted_T))
        weighted_cases += 1

minor_cases = 0
for m in range(1, 6):
    for _ in range(3):
        offsets = [Fraction(v, 3) for v in rng.sample(range(-12, 13), m)]
        exponents = rng.sample(range(0, m+5), m)
        E = sum(exponents)
        values = [det([[(Fraction(x)+b)**e for e in exponents] for b in offsets]) for x in range(E+1)]
        coeff = interpolate(values)
        d = E-m*(m-1)//2
        leading = vand(offsets)*vand(exponents)/prod(factorial(k) for k in range(m))
        require(len(coeff)-1 == d, ('minor degree', m, offsets, exponents, coeff))
        require(coeff[d] == leading, ('minor leading', m))
        next_coefficient = leading * sum(offsets) * d / m
        require((coeff[d-1] if d > 0 else 0) == next_coefficient, ('minor next', m, offsets, exponents))
        minor_cases += 1

# Recover ALL n=8 fiber coefficients using numeric determinants and interpolation.
# This uses neither signed-permutation enumeration nor a Laplace recurrence.
n = 8
I = {0, 1, 2}
J = {0, 1, 6, 7}
values_by_target = [[] for _ in range(4)]
for x in range(29):
    z_values = [det([[(x+i)**j * (z if i in I and j in J else 1) for j in range(n)] for i in range(n)]) for z in range(4)]
    z_coeff = interpolate(z_values) + [Fraction(0)]*4
    for t in range(4):
        values_by_target[t].append(z_coeff[t])
fibers = [interpolate(v) for v in values_by_target]
expected = [-967680, 2903040, -2903040, 967680]
require([len(p)-1 for p in fibers] == [14]*4, 'n8 degrees')
require([p[-1] for p in fibers] == expected, 'n8 leading coefficients')
require(all(c.denominator == 1 for p in fibers for c in p), 'nonintegral n8 coefficient')

out = {
    'method': 'Independent exact numeric determinant evaluation plus power-basis interpolation; direct subset sums versus constructed remainders.',
    'quotient_identity_cases': quotient_cases,
    'weighted_identity_cases': weighted_cases,
    'translated_minor_first_two_coefficients_cases': minor_cases,
    'n8_source_standard': {
        'I': sorted(I), 'J': sorted(J),
        'degrees_by_target': [len(p)-1 for p in fibers],
        'leading_coefficients_by_target': expected,
        'fiber_coefficients_ascending_lambda': [[int(c) for c in p] for p in fibers]
    }
}
print(json.dumps(out, indent=2))
