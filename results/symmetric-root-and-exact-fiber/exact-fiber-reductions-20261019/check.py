#!/usr/bin/env python3
"""Finite independent checks. No assert statements, so python -O runs all checks."""
from itertools import product, permutations, combinations
from collections import Counter
from pathlib import Path
import json
import random


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def original_matchings(n, colors):
    return [tuple((i, p[i]) for i in range(n)) for p in permutations(range(n))
            if all((i, p[i]) in colors for i in range(n))]


def build(n, colors, k):
    """Construct an actual simple binary-colored graph, with separate side IDs."""
    edges = []
    def add(u, v, red):
        edges.append((u, v, red))
        return len(edges) - 1
    if not (n >= 1 and 0 <= k <= n):
        if n == 0 and k == 0:
            ids = [add(i, j, 0) for i in range(2) for j in range(2)]
            return 2, edges, 0, frozenset([ids[0], ids[3]]), None
        e = add(0, 0, 0)
        return 1, edges, 0, frozenset([e]), None
    C = n + 1
    T = C * n + k
    next_left = next_right = n
    states = {}
    for e, red in sorted(colors.items()):
        u, v = e
        q = C + red
        # A path left-old, right-new, left-new, ..., right-old.
        vertices = [('L', u)]
        for _ in range(q - 1):
            vertices.append(('R', next_right)); next_right += 1
            vertices.append(('L', next_left)); next_left += 1
        vertices.append(('R', v))
        odd, even = [], []
        for j, (x, y) in enumerate(zip(vertices, vertices[1:]), start=1):
            left, right = (x[1], y[1]) if x[0] == 'L' else (y[1], x[1])
            idx = add(left, right, j % 2)
            (odd if j % 2 else even).append(idx)
        states[e] = (frozenset(odd), frozenset(even))
    dummy = {add(i, i, 0) for i in range(n)}
    for odd, even in states.values():
        dummy.update(even)
    cycle_red, cycle_blue = set(), set()
    for j in range(T):
        cycle_red.add(add(next_left + j, next_right + j, 1))
        cycle_blue.add(add(next_left + j, next_right + ((j + 1) % T), 0))
    next_left += T; next_right += T
    require(next_left == next_right, 'Unbalanced construction')
    dummy.update(cycle_red)
    def lift(matching):
        original = set(matching)
        chosen = set(cycle_blue)
        for e, (odd, even) in states.items():
            chosen.update(odd if e in original else even)
        return frozenset(chosen)
    R = sum(colors.values())
    require(next_left == n + len(colors)*n + R + T, 'Vertex formula failed')
    require(len(edges) == len(colors)*(2*n+1) + 2*R + n + 2*T,
            'Edge formula failed')
    return next_left, edges, T, frozenset(dummy), lift


def enumerate_actual(n, edges):
    """Enumerate PMs in the actual expanded graph, without using gadget states."""
    adj = [[] for _ in range(2*n)]
    pairs = set()
    for idx, (a, b, red) in enumerate(edges):
        require(0 <= a < n and 0 <= b < n and red in (0, 1), 'Invalid edge')
        require((a, b) not in pairs, 'Parallel edges in final graph')
        pairs.add((a, b))
        adj[a].append((n+b, idx)); adj[n+b].append((a, idx))
    result = []
    def visit(mask, selected):
        if not mask:
            result.append(frozenset(selected)); return
        best_vertex = None; best = None
        scan = mask
        while scan:
            bit = scan & -scan; scan ^= bit
            v = bit.bit_length()-1
            choices = [(u, e) for u, e in adj[v] if mask & (1 << u)]
            if not choices:
                return
            if best is None or len(choices) < len(best):
                best_vertex, best = v, choices
                if len(best) == 1:
                    break
        for u, e in best:
            visit(mask & ~(1 << best_vertex) & ~(1 << u), selected + (e,))
    visit((1 << (2*n))-1, ())
    require(len(set(result)) == len(result), 'Enumerator duplicated PMs')
    return result


def check_actual(n, colors, k):
    N, edges, T, dummy, lift = build(n, colors, k)
    original = original_matchings(n, colors)
    solutions = [M for M in original if sum(colors[e] for e in M) == k]
    all_actual = enumerate_actual(N, edges)
    fiber = {M for M in all_actual if sum(edges[e][2] for e in M) == T}
    require(dummy in fiber, 'Known dummy not in target fiber')
    require(len(fiber) == len(solutions) + 1, 'Wrong target fiber cardinality')
    if lift is not None:
        expected = {dummy} | {lift(M) for M in solutions}
        require(fiber == expected, 'Target fiber does not match explicit bijection')
    return len(all_actual)


def partial_cover_costs(n, colors):
    """Enumerate partial original matchings that admit direct-diagonal completion."""
    result = []
    def visit(i, used, chosen, r):
        if i == n:
            rows = {a for a, b in chosen}; cols = {b for a, b in chosen}
            if rows == cols:
                result.append((len(chosen), r))
            return
        visit(i+1, used, chosen, r)
        for j in range(n):
            if j not in used and (i, j) in colors:
                visit(i+1, used | {j}, chosen + ((i, j),), r+colors[i,j])
    visit(0, set(), (), 0)
    return result


def trie_extra(n, colors, k, F):
    trie = {}
    for M in F:
        node = trie
        for i, j in M:
            node = node.setdefault(j, {})
    answers = []
    def visit(node, prefix):
        i = len(prefix)
        if i == n:
            return
        used = set(prefix)
        for j in range(n):
            if j in used or (i,j) not in colors:
                continue
            if j in node:
                visit(node[j], prefix + (j,))
            else:
                p = prefix + (j,)
                unused_cols = set(range(n)) - set(p)
                residual_target = k - sum(colors[a, b] for a,b in enumerate(p))
                yes = False
                for tail in permutations(unused_cols):
                    entries = tuple((a,b) for a,b in zip(range(len(p),n), tail))
                    if all(e in colors for e in entries) and sum(colors[e] for e in entries) == residual_target:
                        yes = True; break
                answers.append(yes)
    visit(trie, ())
    return any(answers)


def cycle_count_dp(n, colors, cap):
    """Count target costs for max-degree-two input using only connected components."""
    adj = [[] for _ in range(2*n)]
    for (a,b),r in colors.items():
        adj[a].append((n+b,r)); adj[n+b].append((a,r))
    require(all(len(v) <= 2 for v in adj), 'Degree-two promise violated')
    seen=set(); factors=[]; base=0
    for start in range(2*n):
        if start in seen: continue
        stack=[start]; comp=[]
        while stack:
            v=stack.pop()
            if v in seen: continue
            seen.add(v); comp.append(v)
            stack.extend(u for u,r in adj[v] if u not in seen)
        endpoints=[v for v in comp if len(adj[v]) <= 1]
        if endpoints:
            if len(comp) % 2: return [0]*(n+1)
            seq=[]; prev=None; cur=endpoints[0]
            while True:
                nxt=[(u,r) for u,r in adj[cur] if u != prev]
                if not nxt: break
                u,r=nxt[0]; seq.append(r); prev,cur=cur,u
            base += sum(seq[::2])
        else:
            seq=[]; prev=None; cur=comp[0]
            while True:
                u,r=next((u,r) for u,r in adj[cur] if u != prev)
                seq.append(r); prev,cur=cur,u
                if cur == comp[0]: break
            factors.append((sum(seq[::2]),sum(seq[1::2])))
    dp=[0]*(n+1); dp[base]=1
    for a,b in factors:
        nxt=[0]*(n+1)
        for i,v in enumerate(dp):
            for j in (a,b):
                if i+j <= n: nxt[i+j]=min(cap,nxt[i+j]+v)
        dp=nxt
    return dp


def all_colored(n):
    pairs=list(product(range(n),repeat=2))
    for values in product(range(3),repeat=n*n):
        yield {e:s-1 for e,s in zip(pairs,values) if s}


def main():
    counts=Counter()
    for n in range(3):
        for colors in all_colored(n):
            for k in range(-1,n+2):
                counts['actual_expanded_matchings_enumerated'] += check_actual(n,colors,k)
                counts['actual_expanded_instances'] += 1
            X=original_matchings(n,colors)
            for k in range(n+1):
                fiber=[M for M in X if sum(colors[e] for e in M) == k]
                for size in range(1,len(fiber)+1):
                    for F in combinations(fiber,size):
                        require(trie_extra(n,colors,k,F) == (len(fiber)>len(F)), 'Trie reduction failed')
                        counts['trie_explicit_families'] += 1
    rng=random.Random(20261019)
    samples=[(3,120),(4,60),(5,12)]
    for n,number in samples:
        for _ in range(number):
            colors={(i,j):rng.randrange(2) for i in range(n) for j in range(n) if rng.randrange(4)}
            for k in range(n+1):
                counts['actual_expanded_matchings_enumerated'] += check_actual(n,colors,k)
                counts['actual_expanded_instances'] += 1
    for colors in all_colored(3):
        costs=partial_cover_costs(3,colors)
        original=original_matchings(3,colors)
        orig_counts=Counter(sum(colors[e] for e in M) for M in original)
        for k in range(4):
            T=12+k
            total=sum(4*p+r == T for p,r in costs)+sum(4*p+r == 0 for p,r in costs)
            require(total == 1+orig_counts[k], 'Compressed exhaustive reduction failed')
            counts['exhaustive_three_by_three_targets'] += 1
        degrees=Counter(a for a,b in colors)+Counter(3+b for a,b in colors)
        if all(d <= 2 for d in degrees.values()):
            for cap in range(1,8):
                dp=cycle_count_dp(3,colors,cap)
                require(dp == [min(cap,orig_counts[k]) for k in range(4)], 'Cycle DP failed')
                counts['degree_two_capped_distributions'] += 1
    out={'status':'passed','seed':20261019,**dict(sorted(counts.items()))}
    Path(__file__).with_name('results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,sort_keys=True))

if __name__ == '__main__':
    main()
