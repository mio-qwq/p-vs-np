"""Exact group-labeled matching, parameterized by bits + forbidden-edge cover.

Undirected simple graph on an even number of vertices. Default graph is complete.
Research prototype; no novelty claim.
"""
from solver import colorings
from cover_solver import pack


def solve(labels, k, target, allowed=None, cover=()):
    if type(k) is not int or k < 0:
        raise ValueError('nonnegative integer bit count required')
    size = len(labels)
    if size % 2 or any(len(row) != size for row in labels):
        raise ValueError('even square label matrix required')
    if type(target) is not int or not 0 <= target < 1 << k:
        raise ValueError('target out of range')
    if any(type(x) is not int or not 0 <= x < 1 << k for row in labels for x in row):
        raise ValueError('label out of range')
    if any(labels[i][j] != labels[j][i] for i in range(size) for j in range(size)):
        raise ValueError('undirected labels must be symmetric')
    if allowed is None:
        allowed = [[i != j for j in range(size)] for i in range(size)]
    if len(allowed) != size or any(len(row) != size for row in allowed):
        raise ValueError('allowed matrix shape mismatch')
    if any(type(x) is not bool for row in allowed for x in row):
        raise ValueError('allowed entries must be bool')
    if any(allowed[i][i] for i in range(size)) or any(
            allowed[i][j] != allowed[j][i] for i in range(size) for j in range(size)):
        raise ValueError('simple undirected allowed matrix required')
    cover = set(cover)
    if any(type(v) is not int or not 0 <= v < size for v in cover):
        raise ValueError('invalid cover vertex')
    if any(not allowed[i][j] and i not in cover and j not in cover
           for i in range(size) for j in range(i+1,size)):
        raise ValueError('cover misses forbidden edge')
    n = size // 2
    base = [labels[2*i][2*i+1] for i in range(n)]
    initial = 0
    for value in base:
        initial ^= value
    mandatory = {i for i in range(n) if not allowed[2*i][2*i+1]}
    desired = target ^ initial
    if desired == 0 and not mandatory:
        return tuple((2*i,2*i+1) for i in range(n))
    if n <= 1:
        return None
    t = min(n, 4*(k+len(cover))+1)
    for colors in colorings(n,t):
        owners = {colors[v]:v for v in mandatory}
        if len(owners) != len(mandatory):
            continue
        vertices = [v for v in range(n) if colors[v] not in owners or owners[colors[v]] == v]
        cycles = {}
        for start in vertices:
            for entry in (0,1):
                front = {(1<<colors[start], start, entry, 0): ((start,entry),)}
                for length in range(1,len(set(colors))+1):
                    nxt = {}
                    for (mask,last,port,value),path in front.items():
                        out = 2*last+(1-port)
                        first = 2*start+entry
                        if length >= 2 and allowed[out][first]:
                            cycles.setdefault((mask,value ^ labels[out][first] ^ base[last]),path)
                        for vertex in vertices:
                            bit = 1<<colors[vertex]
                            if mask & bit:
                                continue
                            for other in (0,1):
                                endpoint = 2*vertex+other
                                if allowed[out][endpoint]:
                                    nxt.setdefault((mask|bit,vertex,other,value ^ labels[out][endpoint] ^ base[last]),
                                                   path+((vertex,other),))
                    front = nxt
                    if not front:
                        break
        required = sum(1<<colors[v] for v in mandatory)
        witness = pack(cycles,desired,t,required)
        if witness is None:
            continue
        used = set()
        edges = []
        for cycle in witness:
            for j,(pair,port) in enumerate(cycle):
                nxt,entry = cycle[(j+1)%len(cycle)]
                edges.append((2*pair+(1-port),2*nxt+entry))
                used.add(pair)
        edges += [(2*i,2*i+1) for i in range(n) if i not in used]
        assert sorted(v for edge in edges for v in edge) == list(range(size))
        actual = 0
        for u,v in edges:
            assert allowed[u][v]
            actual ^= labels[u][v]
        assert actual == target
        return tuple(edges)
    return None
