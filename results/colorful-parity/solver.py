"""Exact complete-bipartite parity matching via explicit color coding.

Research prototype. The all-field support-radius theorem is a dependency.
No claim of practical parameter constants or literature novelty.
"""
from itertools import combinations


def colorings(n, t):
    if not 0 <= t <= n:
        raise ValueError('require 0 <= t <= n')
    if t <= 1:
        yield (0,) * n
        return
    length = (n - 1).bit_length()
    r = min(length, t - 1)
    for positions in combinations(range(length), r):
        projected = [sum(((v >> b) & 1) << j
                         for j, b in enumerate(positions)) for v in range(n)]
        for chosen in combinations(range(1 << r), t):
            rank = {x: j for j, x in enumerate(chosen)}
            yield tuple(rank.get(x, 0) for x in projected)


def colorful_cycles(delta, colors):
    n = len(colors)
    cycles = {}
    for start in range(n):
        frontier = {(1 << colors[start], start, 0): (start,)}
        for size in range(1, len(set(colors)) + 1):
            nxt = {}
            for (mask, end, value), path in frontier.items():
                if size >= 2:
                    key = (mask, value ^ delta[end][start])
                    cycles.setdefault(key, path)
                for vertex in range(n):
                    bit = 1 << colors[vertex]
                    if not mask & bit:
                        key = (mask | bit, vertex, value ^ delta[end][vertex])
                        nxt.setdefault(key, path + (vertex,))
            frontier = nxt
            if not frontier:
                break
    return cycles


def pack_cycles(cycles, target, t):
    # Every transition adds at least two colors, so increasing integer masks
    # give a topological order. Store a concrete disjoint-color witness.
    states = {0: {0: ()}}
    entries = list(cycles.items())
    for mask in range(1 << t):
        for value, witness in list(states.get(mask, {}).items()):
            if value == target:
                return witness
            for (cmask, cvalue), cycle in entries:
                if not mask & cmask:
                    dest = states.setdefault(mask | cmask, {})
                    dest.setdefault(value ^ cvalue, witness + (cycle,))
    return None


def solve(labels, k, target):
    if type(k) is not int or k < 0:
        raise ValueError('nonnegative integer bit count required')
    n = len(labels)
    if type(target) is not int or not 0 <= target < 1 << k:
        raise ValueError('target out of range')
    if any(len(row) != n for row in labels):
        raise ValueError('square complete label matrix required')
    if any(type(x) is not int or not 0 <= x < 1 << k
           for row in labels for x in row):
        raise ValueError('label out of range')
    initial = 0
    for i in range(n):
        initial ^= labels[i][i]
    desired = target ^ initial
    if desired == 0:
        return tuple(range(n))
    if n <= 1:
        return None
    t = min(n, 2 * k + 1)
    delta = [[labels[i][j] ^ labels[i][i] for j in range(n)] for i in range(n)]
    for colors in colorings(n, t):
        witness = pack_cycles(colorful_cycles(delta, colors), desired, t)
        if witness is not None:
            permutation = list(range(n))
            for cycle in witness:
                for i, vertex in enumerate(cycle):
                    permutation[vertex] = cycle[(i + 1) % len(cycle)]
            assert sorted(permutation) == list(range(n))
            actual = 0
            for i, j in enumerate(permutation):
                actual ^= labels[i][j]
            assert actual == target
            return tuple(permutation)
    return None
