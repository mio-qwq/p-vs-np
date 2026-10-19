#!/usr/bin/env python3
"""Independent finite checks; Python standard library; assertions not required."""
from collections import Counter
from itertools import product
import json
import random


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def perfect_signatures(order, edges):
    """Generic exact matching enumeration, independent of gadget semantics."""
    adjacency = [[] for _ in range(order)]
    seen = set()
    for row, col, label in edges:
        require(0 <= row < order and 0 <= col < order, "vertex range")
        require((row, col) not in seen, "simple graph required")
        seen.add((row, col))
        adjacency[row].append((col, label))
    signatures = Counter()

    def visit(rows, used, signature):
        if not rows:
            signatures[signature] += 1
            return
        choices = [(sum(not ((used >> c) & 1) for c, _ in adjacency[r]), r)
                   for r in rows]
        degree, row = min(choices)
        if degree == 0:
            return
        rest = tuple(r for r in rows if r != row)
        for col, label in adjacency[row]:
            if not ((used >> col) & 1):
                visit(rest, used | (1 << col), signature ^ label)

    visit(tuple(range(order)), 0, 0)
    return signatures


def triples_to_simple(n, triples, reduced_dimension=False):
    """Each parallel x-y edge becomes x-b_e-a_e-y, with b_e-a_e middle."""
    edges = []
    for index, (x, y, z) in enumerate(triples):
        label = 0 if reduced_dimension and z == n - 1 else 1 << z
        internal = n + index
        edges += [(x, internal, label), (internal, internal, 0), (internal, y, 0)]
    return n + len(triples), edges


def direct_triple_signatures(n, triples):
    by_x = [[] for _ in range(n)]
    for x, y, z in triples:
        by_x[x].append((y, z))
    signatures = Counter()
    three_dm = 0

    def visit(x, ys, zs, sig):
        nonlocal three_dm
        if x == n:
            signatures[sig] += 1
            three_dm += len(zs) == n
            return
        for y, z in by_x[x]:
            if y not in ys:
                visit(x + 1, ys | {y}, zs | {z}, sig ^ (1 << z))

    visit(0, set(), set(), 0)
    return signatures, three_dm


def path_graph(k, accept_zero=False):
    """Acyclic two-state bit automaton, with a private subdivision per arc."""
    require(k >= 1, "positive dimension")
    states = {(0, 0): 0}
    next_id = 1
    for i in range(1, k + 1):
        for seen in (0, 1):
            states[i, seen] = next_id
            next_id += 1
    source = states[0, 0]
    sink = next_id
    next_id += 1
    arcs = []
    for i in range(k):
        for seen in (0, 1):
            if (i, seen) not in states:
                continue
            for bit in (0, 1):
                intermediate = next_id
                next_id += 1
                dest = states[i + 1, seen | bit]
                arcs += [(states[i, seen], intermediate, bit << i),
                         (intermediate, dest, 0)]
    arcs.append((states[k, 1], sink, 0))
    if accept_zero:
        arcs.append((states[k, 0], sink, 0))
    rows = {v: i for i, v in enumerate(v for v in range(next_id) if v != sink)}
    cols = {v: i for i, v in enumerate(v for v in range(next_id) if v != source)}
    edges = [(rows[u], cols[v], label) for u, v, label in arcs]
    edges += [(rows[v], cols[v], 0) for v in range(next_id)
              if v not in (source, sink)]
    return next_id - 1, edges


def project(x, rows):
    value = 0
    for i, row in enumerate(rows):
        value |= ((x & row).bit_count() % 2) << i
    return value


def check():
    cycle = [(0, 0, 1), (1, 0, 0), (1, 1, 0),
             (2, 1, 0), (2, 2, 2), (0, 2, 0)]
    original_counts = {s.bit_count() for s in perfect_signatures(3, cycle)}
    # Red occupies bit 0; crossing identities e_A/e_B occupy bits 1/2.
    block1 = [(0, 0, 1), (1, 0, 0), (1, 1, 2), (0, 1, 4)]
    block2 = [(0, 0, 2), (1, 0, 0), (1, 1, 1), (0, 1, 4)]
    sig1, sig2 = perfect_signatures(2, block1), perfect_signatures(2, block2)
    naive_counts = {(a & 1) + (b & 1) for a in sig1 for b in sig2}
    compatible_counts = {(a & 1) + (b & 1) for a in sig1 for b in sig2
                         if (a & 6) == (b & 6)}
    require(original_counts == {0, 2}, "C6 count support")
    require(naive_counts == {0, 1, 2}, "C6 false convolution")
    require(compatible_counts == original_counts, "C6 crossing compatibility")
    reduction_instances = 0
    full = list(product(range(2), repeat=3))
    instances = [(2, [t for i, t in enumerate(full) if (bits >> i) & 1])
                 for bits in range(1 << len(full))]
    rng = random.Random(20261019)
    for _ in range(100):
        triples = [t for t in product(range(3), repeat=3) if rng.randrange(3) == 0]
        instances.append((3, triples))
    instances += [(1, []), (1, [(0, 0, 0)]),
                  (3, list(product(range(3), repeat=3)))]
    for n, triples in instances:
        expected, three_dm = direct_triple_signatures(n, triples)
        order, edges = triples_to_simple(n, triples)
        actual = perfect_signatures(order, edges)
        require(expected == actual, "length-three matching bijection")
        require(actual[(1 << n) - 1] == three_dm, "3DM equivalence")
        reduced_order, reduced_edges = triples_to_simple(n, triples, True)
        reduced = perfect_signatures(reduced_order, reduced_edges)
        reduced_expected = Counter()
        mask = (1 << (n - 1)) - 1
        for signature, count in expected.items():
            reduced_expected[signature & mask] += count
        require(reduced == reduced_expected, "coordinate deletion")
        require(reduced[mask] == three_dm, "n-1 coordinate reduction")
        reduction_instances += 1

    path_certificates = []
    for k in range(1, 8):
        order, edges = path_graph(k)
        nonzero = perfect_signatures(order, edges)
        require(nonzero == Counter({x: 1 for x in range(1, 1 << k)}),
                "nonzero signature automaton")
        order_all, edges_all = path_graph(k, True)
        all_signatures = perfect_signatures(order_all, edges_all)
        require(all_signatures == Counter({x: 1 for x in range(1 << k)}),
                "all signature automaton")
        require(order == 6 * k - 1 and len(edges) == 14 * k - 5, "linear graph size")
        path_certificates.append({"dimension": k, "vertices_per_side": order,
                                  "edges": len(edges), "matchings": sum(nonzero.values())})

    projection_maps = 0
    # All k -> r binary linear maps for r < k through k=4.
    for k in range(1, 5):
        for r in range(k):
            for rows in product(range(1 << k), repeat=r):
                projected_nonzero = {project(x, rows) for x in range(1, 1 << k)}
                projected_all = {project(x, rows) for x in range(1 << k)}
                require(0 in projected_nonzero, "rank-deficient false positive")
                require(projected_nonzero == projected_all, "exact projection indistinguishability")
                projection_maps += 1

    # For n choices of one-hot labels, every parity-compatible vector occurs.
    # Any fixed map with fewer than n-1 output bits loses a nonzero even vector.
    onehot_cases = 0
    for n in range(1, 7):
        reachable = {0}
        for _ in range(n):
            reachable = {p ^ (1 << z) for p in reachable for z in range(n)}
        compatible = {p for p in range(1 << n) if p.bit_count() % 2 == n % 2}
        require(reachable == compatible, "all parity-compatible vectors reachable")
        if n <= 4:
            for r in range(max(0, n - 1)):
                for rows in product(range(1 << n), repeat=r):
                    target = (1 << n) - 1
                    false = [p for p in compatible if p != target
                             and project(p, rows) == project(target, rows)]
                    require(bool(false), "n-1 one-hot dimension lower bound")
                    onehot_cases += 1
    return {"status": "PASS", "three_dm_instances": reduction_instances,
            "c6_original_counts": sorted(original_counts),
            "c6_naive_counts": sorted(naive_counts),
            "linear_maps_checked": projection_maps,
            "onehot_compression_maps_checked": onehot_cases,
            "nonzero_support_graphs": path_certificates}


if __name__ == "__main__":
    print(json.dumps(check(), indent=2, sort_keys=True))
