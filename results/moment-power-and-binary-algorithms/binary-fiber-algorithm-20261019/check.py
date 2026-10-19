#!/usr/bin/env python3
"""Exact, deterministic regression checks for two binary-fiber algorithms."""
from bisect import bisect_left
from collections import deque
from itertools import permutations, product
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def matching(n, edges, excluded_a=None, excluded_b=None):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        if a != excluded_a and b != excluded_b:
            adj[a].append(b)
    owner = [-1] * n

    def augment(a, seen):
        for b in adj[a]:
            if b in seen:
                continue
            seen.add(b)
            if owner[b] < 0 or augment(owner[b], seen):
                owner[b] = a
                return True
        return False

    for a in range(n):
        if a != excluded_a and not augment(a, set()):
            return None
    ans = [-1] * n
    for b, a in enumerate(owner):
        if a >= 0:
            ans[a] = b
    return tuple(ans)


def has_alternating_cycle(n, edges, pm, excluded_a=None, excluded_b=None):
    inverse = {b: a for a, b in enumerate(pm) if b >= 0}
    vertices = [a for a in range(n) if a != excluded_a]
    adj = {a: [] for a in vertices}
    indegree = {a: 0 for a in vertices}
    for a, b in edges:
        if a == excluded_a or b == excluded_b or pm[a] == b:
            continue
        c = inverse[b]
        adj[a].append(c)
        indegree[c] += 1
    queue = deque(a for a in vertices if indegree[a] == 0)
    processed = 0
    while queue:
        a = queue.popleft()
        processed += 1
        for c in adj[a]:
            indegree[c] -= 1
            if indegree[c] == 0:
                queue.append(c)
    return processed != len(vertices)


def classify_edges(n, edges):
    """Return 0 / 1 / 2 (multiple), with one extending PM when present."""
    out = {}
    for a, b in edges:
        pm = matching(n, edges, a, b)
        if pm is None:
            out[a, b] = (0, None)
            continue
        multiple = has_alternating_cycle(n, edges, pm, a, b)
        pm = list(pm)
        pm[a] = b
        out[a, b] = (2 if multiple else 1, tuple(pm))
    return out


def distinguishing_vertex(n, edges, classes=None):
    classes = classes if classes is not None else classify_edges(n, edges)
    for a in range(n):
        incident = [e for e in edges if e[0] == a]
        if any(classes[e][0] == 1 for e in incident) and all(classes[e][0] < 2 for e in incident):
            return a, sorted(classes[e][1] for e in incident if classes[e][0] == 1)
    return None


def star_coloring(n, edges, family, vertex):
    chosen = {pm[vertex] for pm in family}
    return tuple(int(a == vertex and b in chosen) for a, b in edges), 1


def forest_basis(n, edges):
    parent = list(range(2 * n))

    def root(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    tree, chords = [], []
    for i, (a, b) in enumerate(edges):
        u, v = a, n + b
        ru, rv = root(u), root(v)
        if ru == rv:
            chords.append(i)
        else:
            parent[ru] = rv
            tree.append(i)
    adj = [[] for _ in range(2 * n)]
    for i in tree:
        a, b = edges[i]
        adj[a].append((n + b, i))
        adj[n + b].append((a, i))
    basis = []
    for chord in chords:
        a, b = edges[chord]
        target = n + b
        previous = {a: None}
        stack = [a]
        while stack and target not in previous:
            v = stack.pop()
            for u, ei in adj[v]:
                if u not in previous:
                    previous[u] = (v, ei)
                    stack.append(u)
        require(target in previous, 'No fundamental path')
        path = []
        v = target
        while v != a:
            v, ei = previous[v]
            path.append(ei)
        path.reverse()
        require(len(path) % 2 == 1, 'Non-bipartite fundamental cycle')
        z = [0] * len(edges)
        z[chord] = 1
        for i, ei in enumerate(path):
            z[ei] = -1 if i % 2 == 0 else 1
        for vertex in range(2 * n):
            total = sum(z[i] for i, (u, v) in enumerate(edges) if u == vertex or n + v == vertex)
            require(total == 0, 'Cycle has nonzero incident sum')
        basis.append(tuple(z))
    return tree, chords, basis


def chord_enumeration(n, edges, tree, chords):
    out = []
    for bits in product((0, 1), repeat=len(chords)):
        residual = [1] * (2 * n)
        chosen = set()
        for i, bit in zip(chords, bits):
            if bit:
                a, b = edges[i]
                residual[a] -= 1
                residual[n + b] -= 1
                chosen.add(i)
        if any(r < 0 for r in residual):
            continue
        adj = [set() for _ in range(2 * n)]
        for i in tree:
            a, b = edges[i]
            adj[a].add(i)
            adj[n + b].add(i)
        queue = deque(v for v in range(2 * n) if len(adj[v]) <= 1)
        removed = set()
        valid = True
        while queue:
            v = queue.popleft()
            if v in removed:
                continue
            removed.add(v)
            if not adj[v]:
                if residual[v] != 0:
                    valid = False
                    break
                continue
            require(len(adj[v]) == 1, 'Forest peeling failure')
            ei = next(iter(adj[v]))
            a, b = edges[ei]
            u = n + b if v == a else a
            value = residual[v]
            if value not in (0, 1):
                valid = False
                break
            if value:
                chosen.add(ei)
            residual[v] = 0
            residual[u] -= value
            adj[v].remove(ei)
            adj[u].remove(ei)
            if len(adj[u]) <= 1:
                queue.append(u)
        if valid:
            require(len(removed) == 2 * n, 'Unprocessed forest vertex')
            pm = [-1] * n
            for i in chosen:
                a, b = edges[i]
                require(pm[a] == -1, 'Duplicate selected row')
                pm[a] = b
            require(sorted(pm) == list(range(n)), 'Bad enumerated matching')
            out.append(tuple(pm))
    out.sort()
    require(len(set(out)) == len(out), 'Duplicate matching')
    return out


def sorted_union(a, b):
    """Both inputs are sorted distinct tuple vectors."""
    out = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            out.append(a[i]); i += 1
        elif b[j] < a[i]:
            out.append(b[j]); j += 1
        else:
            out.append(a[i]); i += 1; j += 1
    out.extend(a[i:]); out.extend(b[j:])
    return out


def signature_dp(n, edges, basis):
    k = len(basis)
    layers = [[(0,) * k]]
    columns = [tuple(z[e] for z in basis) for e in range(len(edges))]
    for column in columns:
        previous = layers[-1]
        shifted = [tuple(sj + cj for sj, cj in zip(s, column)) for s in previous]
        current = sorted_union(previous, shifted)
        require(all(-n <= value <= n for s in current for value in s), 'Signature bound failure')
        layers.append(current)
    return columns, layers


def reconstruct(signature, columns, layers):
    s = signature
    weights = [0] * len(columns)
    for i in range(len(columns) - 1, -1, -1):
        previous = layers[i]
        position = bisect_left(previous, s)
        if position == len(previous) or previous[position] != s:
            weights[i] = 1
            s = tuple(sj - cj for sj, cj in zip(s, columns[i]))
            position = bisect_left(previous, s)
            require(position < len(previous) and previous[position] == s, 'Broken traceback')
    require(s == (0,) * len(s), 'Traceback does not end at zero')
    return tuple(weights)


def cost(pm, edges, weights):
    return sum(w for (a, b), w in zip(edges, weights) if pm[a] == b)


def all_fiber_masks_from_costs(costs):
    groups = {}
    for i, value in enumerate(costs):
        groups[value] = groups.get(value, 0) | (1 << i)
    return set(groups.values())


def dp_fibers(n, edges, pms, chords, basis):
    columns, layers = signature_dp(n, edges, basis)
    profiles = [tuple(int(pm[edges[e][0]] == edges[e][1]) for e in chords) for pm in pms]
    witnesses = {}
    for signature in layers[-1]:
        costs = [sum(a * b for a, b in zip(profile, signature)) for profile in profiles]
        for mask in all_fiber_masks_from_costs(costs):
            witnesses.setdefault(mask, signature)
    # Every retained family witness is reconstructed and checked on all PMs.
    for mask, signature in witnesses.items():
        weights = reconstruct(signature, columns, layers)
        actual = [cost(pm, edges, weights) for pm in pms]
        require(mask in all_fiber_masks_from_costs(actual), 'DP witness failed exact full fiber test')
    return witnesses, len(layers[-1])


def brute_fibers(n, edges, pms):
    out = set()
    for weights in product((0, 1), repeat=len(edges)):
        out.update(all_fiber_masks_from_costs([cost(pm, edges, weights) for pm in pms]))
    return out


def permutation_pms(n, edges):
    edge_set = set(edges)
    return [p for p in permutations(range(n)) if all((a, b) in edge_set for a, b in enumerate(p))]


def ladder(columns):
    cells = [(r, c) for r in range(2) for c in range(columns)]
    left = {v: i for i, v in enumerate(v for v in cells if sum(v) % 2 == 0)}
    right = {v: i for i, v in enumerate(v for v in cells if sum(v) % 2 == 1)}
    edges = []
    for (r, c), a in left.items():
        for neighbor in ((1-r, c), (r, c-1), (r, c+1)):
            if neighbor in right:
                edges.append((a, right[neighbor]))
    return len(left), sorted(edges)


def multitheta(internal_pairs):
    edges = []
    cursor = 1
    for h in internal_pairs:
        if h == 0:
            edges.append((0, 0))
            continue
        vertices = list(range(cursor, cursor + h))
        cursor += h
        edges.append((0, vertices[0]))
        for j, a in enumerate(vertices):
            edges.append((a, a))
            edges.append((a, vertices[j + 1] if j + 1 < len(vertices) else 0))
    require(len(edges) == len(set(edges)), 'Non-simple theta input')
    return cursor, sorted(edges)


def test_small(name, n, edges):
    classes = classify_edges(n, edges)
    allowed = [e for e in edges if classes[e][0] > 0]
    tree, chords, basis = forest_basis(n, allowed)
    pms = chord_enumeration(n, allowed, tree, chords)
    independent = permutation_pms(n, edges)
    require(pms == independent, name + ': enumeration differs from permutations')
    for e in edges:
        actual = sum(pm[e[0]] == e[1] for pm in pms)
        require(classes[e][0] == min(2, actual), name + ': edge classification mismatch')
    fibers, signatures = dp_fibers(n, allowed, pms, chords, basis)
    brute = brute_fibers(n, edges, pms)
    require(set(fibers) == brute, name + ': DP differs from exhaustive coloring')
    return {'name': name, 'n': n, 'm': len(edges), 'allowed_edges': len(allowed),
            'cycle_rank': len(chords), 'perfect_matchings': len(pms),
            'attainable_signatures': signatures, 'realizable_nonempty_families': len(fibers),
            'binary_colorings_checked': 1 << len(edges)}


def main():
    results = []
    results.append(test_small('K3,3', 3, list(product(range(3), repeat=2))))
    n, edges = ladder(5)
    results.append(test_small('five-rung ladder', n, edges))
    # A forbidden edge is correctly discarded before effective rank is computed.
    results.append(test_small('upper-triangular forced matching', 4,
                              [(a, b) for a in range(4) for b in range(a, 4)]))
    # Four independent squares: opposite cube corners cannot be a binary fiber.
    n = 8
    edges = [(2*j+a, 2*j+b) for j in range(4) for a in range(2) for b in range(2)]
    tree, chords, basis = forest_basis(n, edges)
    pms = chord_enumeration(n, edges, tree, chords)
    fibers, signatures = dp_fibers(n, edges, pms, chords, basis)
    first = tuple(range(n))
    opposite = tuple(a ^ 1 for a in range(n))
    target_mask = (1 << pms.index(first)) | (1 << pms.index(opposite))
    require(target_mask not in fibers, 'Four-square false positive')
    require(distinguishing_vertex(n, edges) is None, 'Four-square false distinguishing vertex')
    results.append({'name': 'four disjoint K2,2', 'n': n, 'm': len(edges),
                    'cycle_rank': len(chords), 'perfect_matchings': len(pms),
                    'attainable_signatures': signatures, 'opposite_pair_realizable': False})
    # Every family in a heterogeneous connected multi-theta graph.
    n, edges = multitheta([0, 1, 2, 3, 4])
    classes = classify_edges(n, edges)
    found = distinguishing_vertex(n, edges, classes)
    require(found is not None, 'No distinguishing vertex on theta graph')
    vertex, pms = found
    tree, chords, basis = forest_basis(n, edges)
    require(pms == chord_enumeration(n, edges, tree, chords), 'Theta enumeration mismatch')
    for mask in range(1, 1 << len(pms)):
        family = [pm for i, pm in enumerate(pms) if mask >> i & 1]
        weights, t = star_coloring(n, edges, family, vertex)
        actual = sum(1 << i for i, pm in enumerate(pms) if cost(pm, edges, weights) == t)
        require(actual == mask, 'Theta star construction failed')
    results.append({'name': 'heterogeneous multi-theta', 'n': n, 'm': len(edges),
                    'cycle_rank': len(chords), 'perfect_matchings': len(pms),
                    'families_constructed': (1 << len(pms)) - 1})
    # Unbounded-rank method does not enumerate 2^k chord assignments or colorings.
    n, edges = multitheta([0] + [1] * 40)
    found = distinguishing_vertex(n, edges)
    require(found is not None, 'Large theta recognition failed')
    vertex, pms = found
    require(len(pms) == 41, 'Large theta PM count wrong')
    families = [pms, pms[::2], pms[1::2], pms[:1], pms[-1:]]
    for family in families:
        weights, t = star_coloring(n, edges, family, vertex)
        require([pm for pm in pms if cost(pm, edges, weights) == t] == family,
                'Large theta coloring failed')
    results.append({'name': '41-branch multi-theta', 'n': n, 'm': len(edges),
                    'cycle_rank': len(edges) - 2*n + 1, 'perfect_matchings': len(pms),
                    'families_constructed': len(families),
                    'uses_chord_or_coloring_enumeration': False})
    output = {'status': 'all exact checks passed', 'instances': results}
    path = Path(__file__).with_name('results.json')
    path.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
