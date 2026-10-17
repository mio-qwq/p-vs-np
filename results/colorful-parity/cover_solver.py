"""Forbidden-edge-cover extension. See separate audit for mathematical scope."""
from solver import colorings


def cycles_for_coloring(delta, allowed, colors, mandatory):
    owners = {colors[v]: v for v in mandatory}
    if len(owners) != len(mandatory):
        return None
    vertices = [v for v in range(len(colors))
                if colors[v] not in owners or owners[colors[v]] == v]
    cycles = {}
    for start in vertices:
        frontier = {(1 << colors[start], start, 0): (start,)}
        for size in range(1, len(set(colors)) + 1):
            nxt = {}
            for (mask, end, value), path in frontier.items():
                if size >= 2 and allowed[end][start]:
                    cycles.setdefault((mask, value ^ delta[end][start]), path)
                for vertex in vertices:
                    bit = 1 << colors[vertex]
                    if allowed[end][vertex] and not mask & bit:
                        nxt.setdefault((mask | bit, vertex, value ^ delta[end][vertex]),
                                       path + (vertex,))
            frontier = nxt
            if not frontier:
                break
    return cycles


def pack(cycles, target, t, required):
    states = {0: {0: ()}}
    entries = list(cycles.items())
    for mask in range(1 << t):
        for value, witness in list(states.get(mask, {}).items()):
            if value == target and mask & required == required:
                return witness
            for (cmask, cvalue), cycle in entries:
                if not mask & cmask:
                    states.setdefault(mask | cmask, {}).setdefault(
                        value ^ cvalue, witness + (cycle,))
    return None


def solve(labels, k, target, allowed, cover):
    if type(k) is not int or k < 0:
        raise ValueError('nonnegative integer bit count required')
    n = len(labels)
    if type(target) is not int or not 0 <= target < 1 << k:
        raise ValueError('target out of range')
    if any(len(row) != n for row in labels) or len(allowed) != n or any(len(row) != n for row in allowed):
        raise ValueError('square label and allowed matrices required')
    if any(type(x) is not int or not 0 <= x < 1 << k for row in labels for x in row):
        raise ValueError('label out of range')
    if any(type(x) is not bool for row in allowed for x in row):
        raise ValueError('allowed entries must be bool')
    cover = set(cover)
    if any(side not in ('r','c') or type(v) is not int or not 0 <= v < n for side,v in cover):
        raise ValueError('invalid cover vertex')
    if any(not allowed[i][j] and ('r',i) not in cover and ('c',j) not in cover
           for i in range(n) for j in range(n)):
        raise ValueError('cover misses forbidden edge')
    initial = 0
    for i in range(n):
        initial ^= labels[i][i]
    mandatory = {i for i in range(n) if not allowed[i][i]}
    desired = target ^ initial
    if not mandatory and desired == 0:
        return tuple(range(n))
    if n <= 1:
        return None
    t = min(n, 2 * (k + len(cover)) + 1)
    delta = [[labels[i][j] ^ labels[i][i] for j in range(n)] for i in range(n)]
    for colors in colorings(n, t):
        cycles = cycles_for_coloring(delta, allowed, colors, mandatory)
        if cycles is None:
            continue
        required = sum(1 << colors[v] for v in mandatory)
        witness = pack(cycles, desired, t, required)
        if witness is not None:
            permutation = list(range(n))
            for cycle in witness:
                for i, v in enumerate(cycle):
                    permutation[v] = cycle[(i + 1) % len(cycle)]
            assert sorted(permutation) == list(range(n))
            actual = 0
            for i,j in enumerate(permutation):
                assert allowed[i][j]
                actual ^= labels[i][j]
            assert actual == target
            return tuple(permutation)
    return None
