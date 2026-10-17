"""Unweighted maximum-cardinality matching in a finite simple undirected graph.

Independent implementation of Edmonds' augmenting-path/blossom-contraction
method (Jack Edmonds, "Paths, Trees, and Flowers", Canadian Journal of
Mathematics 17 (1965), 449-467). This is a standard algorithm, not a novel
research result. No external implementation was used or downloaded.

API: maximum_matching(n, edges) returns a tuple mate, with mate[v] == -1 for
unmatched vertices. Vertices are integers 0,...,n-1. Parallel copies of an edge
are harmless and deduplicated. Self loops and malformed inputs are rejected.
The algorithm is O(n^3) time, O(n+m) storage for simple graphs. Python integer
and indexing operations are treated as unit cost; graph/input size and actual
Python object overhead are separate considerations. Unweighted only.
"""
from collections import deque
from numbers import Integral


def _integer(value):
    return isinstance(value, Integral) and not isinstance(value, bool)


def _graph(n, edges):
    if not _integer(n) or n < 0:
        raise ValueError('n must be a nonnegative integer (not bool)')
    n = int(n)
    adjacency = [set() for _ in range(n)]
    try:
        iterator = iter(edges)
    except TypeError as exc:
        raise ValueError('edges must be an iterable of vertex pairs') from exc
    for edge in iterator:
        try:
            u, v = edge
        except (TypeError, ValueError) as exc:
            raise ValueError('every edge must contain exactly two vertices') from exc
        if not _integer(u) or not _integer(v):
            raise ValueError('edge endpoints must be integers (not bool)')
        u, v = int(u), int(v)
        if not (0 <= u < n and 0 <= v < n):
            raise ValueError('edge endpoint out of range')
        if u == v:
            raise ValueError('self loops are not supported')
        adjacency[u].add(v)
        adjacency[v].add(u)
    return [sorted(neighbors) for neighbors in adjacency]


def maximum_matching(n, edges):
    """Return a maximum-cardinality matching as a symmetric partner tuple."""
    adjacency = _graph(n, edges)
    n = len(adjacency)
    mate = [-1] * n

    def augment_from(root):
        # parent records alternating-forest links, including links adjusted
        # during contraction to encode expansion of each detected blossom.
        parent = [-1] * n
        base = list(range(n))
        outer = [False] * n
        outer[root] = True
        queue = deque([root])

        def common_base(a, b):
            ancestors = [False] * n
            while True:
                a = base[a]
                ancestors[a] = True
                if mate[a] == -1:
                    break
                a = parent[mate[a]]
            while True:
                b = base[b]
                if ancestors[b]:
                    return b
                b = parent[mate[b]]

        def mark_arm(vertex, blossom_base, child, in_blossom):
            while base[vertex] != blossom_base:
                in_blossom[base[vertex]] = True
                in_blossom[base[mate[vertex]]] = True
                parent[vertex] = child
                child = mate[vertex]
                vertex = parent[mate[vertex]]

        while queue:
            v = queue.popleft()
            for u in adjacency[v]:
                if base[v] == base[u] or mate[v] == u:
                    continue
                if u == root or (mate[u] != -1 and parent[mate[u]] != -1):
                    # An edge between outer vertices closes an odd alternating
                    # cycle. Its two arms meet at their least common base.
                    b = common_base(v, u)
                    in_blossom = [False] * n
                    mark_arm(v, b, u, in_blossom)
                    mark_arm(u, b, v, in_blossom)
                    for w in range(n):
                        if in_blossom[base[w]]:
                            base[w] = b
                            if not outer[w]:
                                outer[w] = True
                                queue.append(w)
                elif parent[u] == -1:
                    parent[u] = v
                    if mate[u] == -1:
                        # Follow the encoded expansion and reverse alternating
                        # edges. Each augmentation increases cardinality by one.
                        endpoint = u
                        while endpoint != -1:
                            predecessor = parent[endpoint]
                            next_endpoint = mate[predecessor] if predecessor != -1 else -1
                            mate[endpoint] = predecessor
                            if predecessor != -1:
                                mate[predecessor] = endpoint
                            endpoint = next_endpoint
                        return True
                    w = mate[u]
                    outer[w] = True
                    queue.append(w)
        return False

    for root in range(n):
        if mate[root] == -1:
            augment_from(root)
    return tuple(mate)


def maximum_matching_edges(n, edges):
    """Return maximum matching as canonical (smaller, larger) vertex pairs."""
    mate = maximum_matching(n, edges)
    return tuple((v, u) for v, u in enumerate(mate) if v < u)


def verify_matching(n, edges, matching, require_perfect=False):
    """Return whether a partner vector is a valid (optionally perfect) matching.

    This checks feasibility, NOT maximality or maximum cardinality. A malformed
    graph raises ValueError; a malformed candidate matching returns False.
    """
    adjacency = [set(a) for a in _graph(n, edges)]
    try:
        candidate = tuple(matching)
    except TypeError:
        return False
    if len(candidate) != n:
        return False
    if any(not _integer(u) or not -1 <= u < n for u in candidate):
        return False
    for v, u in enumerate(candidate):
        if u == -1:
            if require_perfect:
                return False
        elif u == v or candidate[u] != v or u not in adjacency[v]:
            return False
    return True
