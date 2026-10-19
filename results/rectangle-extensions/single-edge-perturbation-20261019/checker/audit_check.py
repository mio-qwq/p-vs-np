#!/usr/bin/env python3
"""Independent exact regression checker for the single-edge proof.

Standard library only. Tests 32 deterministic samples (seed 1019) by full
signed-permutation expansion, independently of checker/check.py and of the
moment/Schur formulas. Every check is explicit and remains active under -O.
The cases vary original index order, sparse exponents, and separation direction.
These finite tests supplement the proof; they are not an exhaustive argument.
"""
from itertools import permutations
from math import comb
from fractions import Fraction
import random

def mul(a, b):
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] += x * y
    return c

def trim(a):
    while a and a[-1] == 0:
        a.pop()
    return a

def determinant(a, e, I, J, p=None, c=None):
    n = len(a)
    out = [[] for _ in range(len(I) + 2)]
    V = [[[comb(ex, k) * ai ** (ex - k) for k in range(ex + 1)] for ex in e] for ai in a]
    for sig in permutations(range(n)):
        parity = sum((sig[i] > sig[j] for i in range(n) for j in range(i + 1, n))) % 2
        t = sum((i in I and sig[i] in J or (p is not None and (i, sig[i]) == (p, c)) for i in range(n)))
        v = [1]
        for i, j in enumerate(sig):
            v = mul(v, V[i][j])
        if len(out[t]) < len(v):
            out[t] += [0] * (len(v) - len(out[t]))
        for k, x in enumerate(v):
            out[t][k] += (-1) ** parity * x
    return [trim(v) for v in out]

def coeff(f, d):
    return [v[d] if len(v) > d else 0 for v in f]

def degree(f):
    return max(map(len, f)) - 1

def binomial_coeffs(r):
    return [(-1) ** (r - t) * comb(r, t) for t in range(r + 1)]
rng = random.Random(1019)
cases = []
for n, r, q in [(3, 1, 1), (4, 1, 2), (5, 1, 3), (4, 1, 1), (5, 1, 2), (5, 2, 1), (6, 2, 1), (6, 2, 2)]:
    for repeat in range(4):
        I = set(rng.sample(range(n), r))
        J = set(rng.sample(range(n), r + q))
        p = rng.choice(sorted(set(range(n)) - I))
        c = rng.choice(sorted(set(range(n)) - J))
        lo = rng.sample(range(-11, 0), r)
        hi = rng.sample(range(1, 15), n - r)
        rng.shuffle(lo)
        rng.shuffle(hi)
        a = []
        for i in range(n):
            a.append(lo.pop() if i in I else hi.pop())
        if repeat % 2:
            a = [-v for v in a]
        e = rng.sample(range(n + 3), n)
        R = determinant(a, e, I, J)
        F = determinant(a, e, I, J, p, c)
        aa = [v for i, v in enumerate(a) if i != p]
        ee = [v for j, v in enumerate(e) if j != c]
        II = {i - (i > p) for i in I}
        JJ = {j - (j > c) for j in J}
        minor = determinant(aa, ee, II, JJ)
        D = sum(e) - comb(r, 2) - comb(n - r, 2)
        mono = [comb(e[c], k) * a[p] ** (e[c] - k) for k in range(e[c] + 1)]
        C = [mul(v, mono) if v else [] for v in minor]
        for t in range(r + 2):
            expected = R[t][:] if t < len(R) else []
            for j, sgn in [(t - 1, 1), (t, -1)]:
                if 0 <= j < len(C):
                    if len(expected) < len(C[j]):
                        expected += [0] * (len(C[j]) - len(expected))
                    for k, v in enumerate(C[j]):
                        expected[k] += (-1) ** (p + c) * sgn * v
            if not trim(expected) == F[t]:
                raise RuntimeError(('cofactor', n, r, q, a, e, I, J, p, c, t))
        if n >= 2 * r + q + 1:
            L = degree(minor) + e[c]
            top = coeff(F, L)
            CR = coeff(R, degree(R))[r]
            Cm = coeff(minor, degree(minor))[r]
            if not (degree(F) == L and top == [(-1) ** (p + c) * Cm * v for v in binomial_coeffs(r + 1)]):
                raise RuntimeError('Independent exact audit check failed: degree(F) == L and top == [(-1) ** (p + c) * Cm * v for v in binomial_coeffs(r + 1)]')
            if not L - degree(R) >= n - r - q - 1:
                raise RuntimeError('Independent exact audit check failed: L - degree(R) >= n - r - q - 1')
            if not all((len(v) == L + 1 for v in F)):
                raise RuntimeError('Independent exact audit check failed: all((len(v) == L + 1 for v in F))')
        elif r >= 2:
            L = D + r - 1
            Cm = coeff(minor, degree(minor))[r]
            if not (degree(F) == L and coeff(F, L) == [0] + [(-1) ** (p + c) * Cm * v for v in binomial_coeffs(r)]):
                raise RuntimeError('Independent exact audit check failed: degree(F) == L and coeff(F, L) == [0] + [(-1) ** (p + c) * Cm * v for v in binomial_coeffs(r)]')
            if not (len(F[0]) == D + 1 and F[0] == R[0]):
                raise RuntimeError('Independent exact audit check failed: len(F[0]) == D + 1 and F[0] == R[0]')
            if not all((len(v) == L + 1 for v in F[1:])):
                raise RuntimeError('Independent exact audit check failed: all((len(v) == L + 1 for v in F[1:]))')
        else:
            CR = coeff(R, D)[1]
            CE = (-1) ** (p + c) * coeff(minor, degree(minor))[1]
            ratio = Fraction(1)
            i = next(iter(I))
            for s in range(n):
                if s not in (i, p):
                    ratio *= Fraction(a[s] - a[i], a[s] - a[p])
            if not Fraction(CE, CR) == ratio:
                raise RuntimeError('Independent exact audit check failed: Fraction(CE, CR) == ratio')
            if not coeff(F, D) == [-CR, CR - CE, CE]:
                raise RuntimeError('Independent exact audit check failed: coeff(F, D) == [-CR, CR - CE, CE]')
        cases.append((n, r, q, repeat))
print('PASS:', len(cases), 'independent exact permutation-expansion cases; reordered indices, sparse exponents, forward and reverse separation; cofactor identity and all applicable leading formulas.')
