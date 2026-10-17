"""Explicit CNF test families; no external dependencies."""

def pigeonhole(pigeons, holes, start=1):
    def v(p,h): return start+p*holes+h
    clauses = [tuple(v(p,h) for h in range(holes)) for p in range(pigeons)]
    clauses += [(-v(p,h), -v(q,h)) for h in range(holes)
                for p in range(pigeons) for q in range(p+1,pigeons)]
    return clauses, start+pigeons*holes-1


def selector_stars(k):
    """UNSAT; intended >=2**k canonical nonterminal states for exact ARB.

    x_i=1..k; t_i=k+1..2k; then PHP(4,3); then distinct star
    centers and leaves. Clause count 22+k+k(k+1)/2.
    """
    if k < 0:
        raise ValueError('k must be nonnegative')
    clauses = [(i, k+i) for i in range(1,k+1)]
    core, n = pigeonhole(4,3,2*k+1)
    clauses.extend(core)
    for i in range(1,k+1):
        n += 1
        center = n
        for _ in range(i):
            n += 1
            clauses.append((i,center,n))
    return clauses,n


def cubic_tseitin(edges, odd=True):
    from itertools import product
    vertices=sorted({v for e in edges for v in e})
    clauses=[]
    for vertex in vertices:
        inc=[i+1 for i,e in enumerate(edges) if vertex in e]
        charge=int(odd and vertex==vertices[0])
        for assignment in product((0,1),repeat=len(inc)):
            if sum(assignment)%2 != charge:
                clauses.append(tuple(-v if bit else v for v,bit in zip(inc,assignment)))
    return clauses,len(edges)


def hide_cubic_clauses(cnf,n):
    """C=(a or b or c) -> (a or b or y) and (not y or c)."""
    result=[]
    for c in cnf:
        if len(c)!=3:
            raise ValueError('Requires clauses of exactly length 3')
        n+=1
        result.extend(((c[0],c[1],n),(-n,c[2])))
    return result,n
