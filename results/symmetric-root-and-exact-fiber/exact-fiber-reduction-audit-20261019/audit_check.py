#!/usr/bin/env python3
"""Independent exact checks of singleton reduction and prefix-oracle reduction.
No imported partner code, no floating point, no assertion-dependent checks.
"""
from itertools import product, permutations
from random import Random
from collections import Counter
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def original_matchings(n, edges):
    return [(p, sum(edges[i, p[i]] for i in range(n)))
            for p in permutations(range(n))
            if all((i, p[i]) in edges for i in range(n))]


def expanded(n, edges, k):
    """Build directly on labelled left/right vertices, without multiedges."""
    C, T = n + 1, n * (n + 1) + k
    require(n >= 1 and 0 <= k <= n, 'domain')
    L = [('a', i) for i in range(n)]
    R = [('b', j) for j in range(n)]
    color = {}
    dummy = set()
    def add(u, v, w, in_dummy=False):
        require((u, v) not in color, 'parallel edge')
        color[u, v] = w
        if in_dummy:
            dummy.add((u, v))
    for i in range(n):
        add(('a', i), ('b', i), 0, True)
    for ei, ((i, j), w) in enumerate(sorted(edges.items())):
        q = C + w
        path = [('a', i)]
        for h in range(1, 2 * q - 1):
            v = ('path', ei, h)
            (R if h % 2 else L).append(v)
            path.append(v)
        path.append(('b', j))
        for h, (u, v) in enumerate(zip(path, path[1:]), 1):
            if h % 2:
                add(u, v, 1)
            else:
                add(v, u, 0, True)
    for j in range(T):
        L.append(('cl', j))
        R.append(('cr', j))
        add(('cl', j), ('cr', j), 1, True)
        add(('cl', j), ('cr', (j + 1) % T), 0)
    N = n + n * len(edges) + sum(edges.values()) + T
    M = n + (2 * n + 1) * len(edges) + 2 * sum(edges.values()) + 2 * T
    require(len(L) == len(R) == N and len(color) == M, 'size formula')
    require(len(dummy) == N, 'dummy cardinality')
    require(len({u for u, v in dummy}) == len({v for u, v in dummy}) == N, 'dummy matching')
    require(sum(color[e] for e in dummy) == T, 'dummy target')
    return L, R, color, dummy, T


def enumerate_expanded(L, R, color):
    """Enumerate actual expanded-graph perfect matchings by min-degree branching."""
    rid = {v: i for i, v in enumerate(R)}
    adj = {u: tuple((rid[v], v, w) for (a, v), w in color.items() if a == u) for u in L}
    full = (1 << len(R)) - 1
    chosen = []
    def rec(rows, free, cost):
        if not rows:
            yield frozenset(chosen), cost
            return
        options = [(tuple(x for x in adj[u] if free >> x[0] & 1), u) for u in rows]
        opts, u = min(options, key=lambda p: len(p[0]))
        if not opts:
            return
        rest = tuple(v for v in rows if v != u)
        for bi, v, w in opts:
            chosen.append((u, v))
            yield from rec(rest, free ^ (1 << bi), cost + w)
            chosen.pop()
    return rec(tuple(L), full, 0)


def check_expansion(n, edges, k):
    originals = original_matchings(n, edges)
    L, R, color, dummy, T = expanded(n, edges, k)
    actual = list(enumerate_expanded(L, R, color))
    fiber = [M for M, cost in actual if cost == T]
    require(frozenset(dummy) in fiber, 'missing dummy')
    expected = 1 + sum(cost == k for p, cost in originals)
    require(len(fiber) == expected, ('fiber mismatch', n, edges, k, len(fiber), expected))
    # Stronger check: every nontarget total cost agrees with the combinatorial
    # principal-subpermutation model of the entire augmented graph.
    hist = Counter(cost for M, cost in actual)
    expected_hist = Counter()
    for state in product(range(-1, n), repeat=n):
        selected = [i for i, j in enumerate(state) if j != -1]
        if {state[i] for i in selected} != set(selected) or len({state[i] for i in selected}) != len(selected):
            continue
        if any((i, state[i]) not in edges for i in selected):
            continue
        cost = (n + 1) * len(selected) + sum(edges[i, state[i]] for i in selected)
        expected_hist[cost] += 1
        expected_hist[cost + T] += 1
    require(hist == expected_hist, ('full histogram mismatch', n, edges, k))
    return len(actual)


def prefix_algorithm(n, edges, t, F):
    """Return completeness using only exact-count residual queries."""
    if not F or any(len(p) != n or len(set(p)) != n or any((i, p[i]) not in edges for i in range(n)) for p in F):
        return False, 0
    if any(sum(edges[i, p[i]] for i in range(n)) != t for p in F):
        return False, 0
    prefixes = {p[:i] for p in F for i in range(n + 1)}
    queries = 0
    for pre in sorted(prefixes, key=lambda p: (len(p), p)):
        d = len(pre)
        if d == n:
            continue
        used = set(pre)
        for j in range(n):
            if j in used or (d, j) not in edges or pre + (j,) in prefixes:
                continue
            candidate = pre + (j,)
            remcols = sorted(set(range(n)) - set(candidate))
            remrows = list(range(d + 1, n))
            remaining_t = t - sum(edges[i, v] for i, v in enumerate(candidate))
            queries += 1
            if remaining_t < 0 or remaining_t > len(remrows):
                continue
            for p in permutations(remcols):
                if all((i, v) in edges for i, v in zip(remrows, p)) and sum(edges[i, v] for i, v in zip(remrows, p)) == remaining_t:
                    return False, queries
    return True, queries


def main():
    cases = outputs = 0
    for n in (1, 2):
        for choices in product((-1, 0, 1), repeat=n*n):
            edges = {(i, j): choices[i*n+j] for i in range(n) for j in range(n) if choices[i*n+j] != -1}
            for k in range(n + 1):
                outputs += check_expansion(n, edges, k)
                cases += 1
    rng = Random(20261019)
    for n, samples in ((3, 80), (4, 30), (5, 3)):
        for sample in range(samples):
            density = (0.25, 0.6, 1.0)[sample % 3]
            edges = {(i, j): rng.randrange(2) for i in range(n) for j in range(n) if rng.random() < density}
            for k in range(n + 1):
                outputs += check_expansion(n, edges, k)
                cases += 1
    prefix_cases = queries = 0
    n = 3
    all_p = list(permutations(range(n)))
    for bits in product((0, 1), repeat=n*n):
        edges = {(i, j): bits[i*n+j] for i in range(n) for j in range(n)}
        X = original_matchings(n, edges)
        for mask in range(1, 1 << len(all_p)):
            F = {p for i, p in enumerate(all_p) if mask >> i & 1}
            for t in range(n + 1):
                actual, q = prefix_algorithm(n, edges, t, F)
                expected = {p for p, w in X if w == t} == F
                require(actual == expected, ('prefix mismatch', bits, t, F))
                require(q <= (1 + len(F)*n)*n, 'query bound')
                prefix_cases += 1
                queries += q
    result = {'expanded_graph_cases': cases, 'expanded_perfect_matchings_enumerated': outputs,
              'prefix_completeness_cases': prefix_cases, 'residual_queries': queries,
              'status': 'PASS'}
    Path(__file__).with_name('audit_results.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, sort_keys=True))

if __name__ == '__main__':
    main()
