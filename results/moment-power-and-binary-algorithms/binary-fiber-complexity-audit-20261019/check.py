#!/usr/bin/env python3
"""Finite exact regression tests. Universal claims are proved in AUDIT.md."""
from fractions import Fraction
from itertools import permutations, product
from math import lcm


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def rank(rows):
    rows = [[Fraction(x) for x in row] for row in rows]
    if not rows:
        return 0
    r = 0
    for c in range(len(rows[0])):
        pivot = next((i for i in range(r, len(rows)) if rows[i][c]), None)
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        q = rows[r][c]
        rows[r] = [v / q for v in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c]:
                q = rows[i][c]
                rows[i] = [a - q * b for a, b in zip(rows[i], rows[r])]
        r += 1
        if r == len(rows):
            break
    return r


def integer_nullspace(rows, width):
    a = [[Fraction(v) for v in row] for row in rows]
    pivot_columns = []
    r = 0
    for c in range(width):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        q = a[r][c]
        a[r] = [v / q for v in a[r]]
        for i in range(len(a)):
            if i != r and a[i][c]:
                q = a[i][c]
                a[i] = [u - q * v for u, v in zip(a[i], a[r])]
        pivot_columns.append(c)
        r += 1
        if r == len(a):
            break
    out = []
    for free in range(width):
        if free in pivot_columns:
            continue
        v = [Fraction(0)] * width
        v[free] = Fraction(1)
        for i, pivot in enumerate(pivot_columns):
            v[pivot] = -a[i][free]
        denominator = lcm(*(x.denominator for x in v))
        out.append([int(x * denominator) for x in v])
    return out


def check_succinct_reduction():
    count = 0
    for r in range(3):
        k = r + 2
        choices = list(product((0, 1), repeat=k))
        for truth_table in range(1 << (1 << r)):
            def member(z):
                x = sum(z[j] << j for j in range(r))
                return z[-2:] != (1, 1) or not ((truth_table >> x) & 1)

            family = {z for z in choices if member(z)}
            require((0,) * k in family, "zero missing")
            for j in range(k):
                require(tuple(int(i == j) for i in range(k)) in family,
                        "affine basis missing")
            feasible = False
            for delta in product(range(-2, 3), repeat=k):
                fiber = {z for z in choices if dot(z, delta) == 0}
                if fiber == family:
                    feasible = True
                    break
            require(feasible == (truth_table == 0), "UNSAT reduction failed")
            require(len(family) >= 3 * (1 << r), "padding cardinality")
            count += 1
    return count


def determinant(matrix, p):
    a = [row[:] for row in matrix]
    out = 1
    for j in range(len(a)):
        pivot = next((i for i in range(j, len(a)) if a[i][j] % p), None)
        if pivot is None:
            return 0
        if pivot != j:
            a[pivot], a[j] = a[j], a[pivot]
            out = -out
        pivot_value = a[j][j] % p
        out = out * pivot_value % p
        inv = pow(pivot_value, -1, p)
        for i in range(j + 1, len(a)):
            q = a[i][j] * inv % p
            for k in range(j, len(a)):
                a[i][k] = (a[i][k] - q * a[j][k]) % p
    return out % p


def interpolate(values, p):
    """Polynomial coefficients from values at 0,...,len(values)-1."""
    out = [0] * len(values)
    for i, value in enumerate(values):
        term = [1]
        den = 1
        for j in range(len(values)):
            if j == i:
                continue
            nxt = [0] * (len(term) + 1)
            for k, coefficient in enumerate(term):
                nxt[k] = (nxt[k] - j * coefficient) % p
                nxt[k + 1] = (nxt[k + 1] + coefficient) % p
            term = nxt
            den = den * (i - j) % p
        scale = value * pow(den, -1, p) % p
        out = [(a + scale * b) % p for a, b in zip(out, term)]
    return out


def sign(perm):
    return (-1) ** sum(perm[i] > perm[j]
                       for i in range(len(perm)) for j in range(i + 1, len(perm)))


def monomial(perm, xs, n):
    out = 1
    for i, j in enumerate(perm):
        out *= xs[n * i + j]
    return out


def check_determinant_verifier():
    n, p = 3, 11
    all_matchings = list(permutations(range(n)))
    fibers_checked = missing_checked = 0
    for w in product((0, 1), repeat=n * n):
        costs = {perm: sum(w[n * i + j] for i, j in enumerate(perm))
                 for perm in all_matchings}
        for xs in (list(range(1, 10)), [1] * 9):
            evaluations = []
            for z in range(n + 1):
                matrix = [[xs[n * i + j] * pow(z, w[n * i + j], p) % p
                           for j in range(n)] for i in range(n)]
                evaluations.append(determinant(matrix, p))
            coefficients = interpolate(evaluations, p)
            for t in range(n + 1):
                family = [perm for perm in all_matchings if costs[perm] == t]
                expected = sum(sign(perm) * monomial(perm, xs, n)
                               for perm in family) % p
                require(coefficients[t] == expected, "det coefficient mismatch")
                fibers_checked += 1
                if len(family) > 1:
                    removed = family[0]
                    remainder = sum(sign(perm) * monomial(perm, xs, n)
                                    for perm in family[1:]) % p
                    q = (coefficients[t] - remainder) % p
                    require(q == sign(removed) * monomial(removed, xs, n) % p,
                            "subtraction did not leave missing monomial")
                    require(q != 0, "single missing monomial unexpectedly vanished")
                    missing_checked += 1
    return fibers_checked, missing_checked


def components(n, edges):
    adj = [set() for _ in range(2 * n)]
    for a, b in edges:
        adj[a].add(n + b)
        adj[n + b].add(a)
    seen, count = set(), 0
    for start in range(2 * n):
        if start in seen:
            continue
        count += 1
        todo = [start]
        seen.add(start)
        while todo:
            a = todo.pop()
            for b in adj[a] - seen:
                seen.add(b)
                todo.append(b)
    return count


def check_dimension_and_selector():
    n = 3
    universe = [(i, j) for i in range(n) for j in range(n)]
    perms = list(permutations(range(n)))
    graphs = selector_fibers = 0
    for support in product((0, 1), repeat=n * n):
        edges = {e for e, bit in zip(universe, support) if bit}
        matchings = [p for p in perms if all((i, j) in edges for i, j in enumerate(p))]
        if not matchings:
            continue
        allowed = set().union(*({(i, j) for i, j in enumerate(p)} for p in matchings))
        d = len(allowed) - 2 * n + components(n, allowed)
        incidence = [[int(p[i] == j) for i, j in universe] for p in matchings]
        differences = [[a - b for a, b in zip(v, incidence[0])] for v in incidence]
        require(rank(differences) == d, "affine dimension formula")
        require(len(matchings) <= 2 ** d, "Boolean cardinality bound")
        graphs += 1
        for a in range(n):
            if len({p[a] for p in matchings}) != len(matchings):
                continue
            for mask in range(1, 1 << len(matchings)):
                family = {p for j, p in enumerate(matchings) if mask >> j & 1}
                chosen = {p[a] for p in family}
                reds = {(a, b) for b in chosen}
                fiber = {p for p in matchings
                         if sum((i, j) in reds for i, j in enumerate(p)) == 1}
                require(fiber == family, "selector coloring failed")
                selector_fibers += 1
    return graphs, selector_fibers


def check_large_radix_closure():
    n = 3
    perms = list(permutations(range(n)))
    vectors = [[int(p[i] == j) for i in range(n) for j in range(n)] for p in perms]
    tests = 0
    for mask in range(1, 1 << len(perms)):
        family = [v for j, v in enumerate(vectors) if mask >> j & 1]
        reference = family[0]
        differences = [[a - b for a, b in zip(v, reference)] for v in family]
        rho = rank(differences)
        basis = integer_nullspace(differences, n * n)
        h = max(1, *(abs(x) for row in basis for x in row))
        s = 2 * n * h + 2
        w = [sum(s ** i * row[j] for i, row in enumerate(basis)) for j in range(n * n)]
        shift = max(0, -min(w, default=0))
        nonnegative = [x + shift for x in w]
        for v in vectors:
            difference = [a - b for a, b in zip(v, reference)]
            in_closure = rank(differences + [difference]) == rho
            require((dot(w, difference) == 0) == in_closure,
                    "large-radix affine closure failure")
            require((dot(nonnegative, difference) == 0) == in_closure,
                    "uniform-shift closure failure")
            tests += 1
    return tests


def main():
    require({2, 0} == {sum(int(i == j) for i, j in enumerate(p))
                      for p in permutations(range(2))}, "min/max gap")
    print("succinct reduction truth tables:", check_succinct_reduction())
    print("determinant coefficient checks, missing-member checks:",
          check_determinant_verifier())
    print("supported graphs, selector-vertex fibers:", check_dimension_and_selector())
    print("large-radix affine-closure checks:", check_large_radix_closure())
    print("PASS: all exact finite regression checks")


if __name__ == "__main__":
    main()
