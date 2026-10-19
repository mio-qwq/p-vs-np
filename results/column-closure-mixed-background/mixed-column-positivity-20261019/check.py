#!/usr/bin/env python3
"""Exact implementation checks; universal claims are proved in PROOF.md."""
from fractions import Fraction as F
from itertools import permutations
from math import comb, prod


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def trim(p):
    p = list(map(F, p))
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def add(p, q):
    return trim([(p[i] if i < len(p) else 0)
                 + (q[i] if i < len(q) else 0)
                 for i in range(max(len(p), len(q)))])


def scale(p, c):
    return trim([c * z for z in p])


def mul(p, q):
    z = [F(0)] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            z[i + j] += x * y
    return trim(z)


def power(p, r):
    z = [F(1)]
    for _ in range(r):
        z = mul(z, p)
    return z


def derivative(p):
    return trim([i * p[i] for i in range(1, len(p))] or [0])


def homogeneous(nodes, degree):
    hs = [[F(1)]] + [[F(0)] for _ in range(degree)]
    for node in nodes:
        for r in range(1, degree + 1):
            hs[r] = add(hs[r], mul(node, hs[r - 1]))
    return hs[degree]


def parity(perm):
    return (-1) ** sum(perm[i] > perm[j]
                       for i in range(len(perm))
                       for j in range(i + 1, len(perm)))


def determinant(matrix):
    n = len(matrix)
    out = [F(0)]
    for perm in permutations(range(n)):
        term = [F(parity(perm))]
        for i, j in enumerate(perm):
            term = mul(term, matrix[i][j])
        out = add(out, term)
    return out


def laplace(a, exponents, column):
    n = len(a)
    matrix = [[power([x, 1], e) for e in exponents] for x in a]
    return [scale(mul(matrix[s][column], determinant(
        [[matrix[t][j] for j in range(n) if j != column]
         for t in range(n) if t != s])), (-1) ** (s + column))
        for s in range(n)]


def rank(polynomials):
    nr = max(map(len, polynomials))
    nc = len(polynomials)
    rows = [[p[i] if i < len(p) else F(0) for p in polynomials]
            for i in range(nr)]
    r = 0
    for c in range(nc):
        pivot = next((j for j in range(r, nr) if rows[j][c]), None)
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        pivot_value = rows[r][c]
        rows[r] = [v / pivot_value for v in rows[r]]
        for j in range(nr):
            if j != r and rows[j][c]:
                value = rows[j][c]
                rows[j] = [v - value * w for v, w in zip(rows[j], rows[r])]
        r += 1
    return r


def check_instance(a, h, d, k):
    n = len(a)
    m = n - 1
    background = [h + j for j in range(n - 2)] + [h + n - 2 + d]
    require(k not in background, "distinguished exponent repeated")
    # Put the distinguished exponent last so the common cofactor sign is +1.
    ts = laplace(a, background + [k], m)
    nodes = [[F(x), F(1)] for x in a]
    delta = prod(a[j] - a[i] for i in range(n) for j in range(i + 1, n))
    H = homogeneous(nodes, d)
    B = homogeneous(nodes, d - 1)
    require(derivative(H) == scale(B, m + d), "translation derivative identity")
    for s in range(n):
        others = [nodes[t] for t in range(n) if t != s]
        hs = homogeneous(others, d)
        require(hs == add(H, scale(mul(nodes[s], B), -1)),
                "excluded-variable identity")
        gp = prod(a[s] - a[t] for t in range(n) if t != s)
        expected = scale(mul(power(nodes[s], k), hs), F(delta, gp))
        for node in others:
            expected = mul(expected, power(node, h))
        require(expected == ts[s], "alternant/cofactor identity")
        ell = k - h
        if ell >= 0:
            y = power(nodes[s], ell + 1)
            ode = add(mul(H, derivative(y)),
                      scale(mul(derivative(H), y), -F(ell + 1, m + d)))
            expected_ode = scale(mul(power(nodes[s], ell), hs), ell + 1)
            require(ode == expected_ode, "individual ODE identity")
    require(rank(ts) == n, "representative theorem instance rank")


def main():
    # Checks include ell=-1 and ell<-1, mixed signs, a zero node, rational
    # offsets, an arithmetic-resonance case, and the high-exponent branch.
    cases = [
        ((-3, -1, 1, 3), 0, 3, 3),
        ((-3, -1, 1, 3), 0, 3, 4),
        ((-4, -1, 0, 2), 2, 3, 1),
        ((-4, -1, 0, 2), 4, 3, 1),
        ((-5, -2, 0, 1, 4), 0, 5, 5),
        ((-5, -2, 0, 1, 4), 2, 3, 1),
        ((-2, 0, 3), 0, 3, 2),
        ((F(-5, 3), F(-1, 2), F(2, 3), F(7, 2)), 0, 3, 3),
        ((-3, -1, 1, 3), 0, 2, 9),
        ((-3, -1, 1, 3), 0, 2, 2),
        ((-3, -1, 1, 3), 0, 4, 3),
        ((-3, -1, 1, 3), 0, 6, 2),
        ((-5, -2, 0, 1, 4), 0, 10, 6),
    ]
    for args in cases:
        check_instance(*args)

    a = (-3, -1, 1, 3)
    ts = laplace(a, [0, 1, 3, 5], 2)
    expected = [
        [-12960, -8640, 4320, 1920, 800, -960, 160],
        [480, 960, -5280, 5760, -2400, 960, -480],
        [-480, 960, 5280, 5760, 2400, 960, 480],
        [12960, -8640, -4320, 1920, -800, -960, -160],
    ]
    require(ts == list(map(trim, expected)), "displayed example expansion")
    require(all(t[3] / 5376 - t[1] / 13440 == 1 for t in ts),
            "explicit strictly positive coefficient functional")

    hook_ts = laplace((-3, -2, -1, 1, 2, 3), [0, 1, 2, 3, 4, 6], 1)
    hook_u = (80, -30, 48, 48, -30, 80)
    hook_sum = [F(0)]
    for u, t in zip(hook_u, hook_ts):
        hook_sum = add(hook_sum, scale(t, u))
    require(hook_sum == [0] and sum(hook_u) == 196,
            "equal-output functional obstruction")

    # Exact polynomial-in-n check of the sixth-moment obstruction identity.
    # N6 - N4*n*(n+1) is the positive numerator displayed in PROOF.md.
    N6 = [375, 470, 202, 34, 2]
    N4 = [15, 11, 1]
    difference = add(N6, scale(mul(N4, [0, 1, 1]), -1))
    require(difference == trim([375, 455, 176, 22, 1]),
            "sixth-moment rational-function numerator")
    print("PASS: exact cofactor/ODE identities, representative ranks, "
          "and positive-functional certificate.")


if __name__ == "__main__":
    main()
