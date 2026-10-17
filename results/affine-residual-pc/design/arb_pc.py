"""Exact affine-residual branching with safe purity and decomposition. Python 3 standard library.

No claim of polynomial total runtime. Integers encode O(n)-bit GF(2) vectors.
The implementation is deterministic; every ordering/tie rule is explicit.
"""
from dataclasses import dataclass, asdict
from itertools import product

@dataclass
class Stats:
    pure_assignments: int = 0
    component_splits: int = 0
    calls: int = 0
    unique_states: int = 0
    cache_hits: int = 0
    branches: int = 0
    parity_blocks: int = 0
    max_depth: int = 0
    max_free_dimension: int = 0
    max_literals: int = 0
    normalize_calls: int = 0
    input_variables: int = 0
    expanded_variables: int = 0


def ordinary_normalize(cnf):
    out = set()
    for clause in cnf:
        c = frozenset(clause)
        if 0 in c:
            raise ValueError('Literal 0 is not permitted')
        if any(-x in c for x in c):
            continue
        out.add(tuple(sorted(c)))
    return tuple(sorted(out, key=lambda c: (len(c), c)))


def to_3cnf(cnf, n):
    out = []
    for c in ordinary_normalize(cnf):
        if len(c) <= 3:
            out.append(c)
            continue
        n += 1
        y = n
        out.append((c[0], c[1], y))
        for lit in c[2:-2]:
            n += 1
            z = n
            out.append((-y, lit, z))
            y = z
        out.append((-y, c[-2], c[-1]))
    return ordinary_normalize(out), n


def extract_parity(cnf):
    """Extract explicit entire forbidden-parity blocks, support size <= 3."""
    groups = {}
    for c in cnf:
        support = tuple(sorted(abs(x) for x in c))
        groups.setdefault(support, set()).add(c)
    equations = []
    remaining = []
    blocks = 0
    for support in sorted(groups):
        cs = groups[support]
        if not support:
            remaining.extend(cs)
            continue
        for rhs in (0, 1):
            block = set()
            for bits in product((0, 1), repeat=len(support)):
                if sum(bits) % 2 != rhs:
                    block.add(tuple(sorted(-v if b else v
                                           for v, b in zip(support, bits))))
            if block <= cs:
                cs.difference_update(block)
                equations.append((sum(1 << (v-1) for v in support), rhs))
                blocks += 1
        remaining.extend(cs)
    affine = tuple(tuple((1 << (abs(lit)-1), int(lit < 0)) for lit in c)
                   for c in remaining)
    return affine, tuple(equations), blocks


def rref(equations):
    """Return pivot -> (row mask, right side), or None for contradiction."""
    rows = {}
    for mask, rhs in equations:
        rhs &= 1
        for p in sorted(rows):
            if mask & (1 << p):
                a, b = rows[p]
                mask ^= a
                rhs ^= b
        if mask == 0:
            if rhs:
                return None
            continue
        p = (mask & -mask).bit_length() - 1
        for q, (a, b) in list(rows.items()):
            if a & (1 << p):
                rows[q] = (a ^ mask, b ^ rhs)
        rows[p] = (mask, rhs)
    return rows


def normalize_base(clauses, n, equations=()):
    """Return False, True, or key (free dimension, sorted affine clauses).

    Unit equations are saturated. After substitution, only coordinates that
    appear in remaining clauses are retained, in inherited order. Dropping
    unused free coordinates preserves satisfiability (not model counts).
    """
    while True:
        rows = rref(equations)
        if rows is None:
            return False
        out = set()
        units = []
        for clause in clauses:
            forms = set()
            satisfied = False
            for mask, const in clause:
                for p in sorted(rows):
                    if mask & (1 << p):
                        a, b = rows[p]
                        mask ^= a
                        const ^= b
                if mask == 0:
                    if const:
                        satisfied = True
                        break
                    continue
                if (mask, const ^ 1) in forms:
                    satisfied = True
                    break
                forms.add((mask, const))
            if satisfied:
                continue
            if not forms:
                return False
            c = tuple(sorted(forms))
            if len(c) == 1:
                mask, const = c[0]
                units.append((mask, const ^ 1))
            out.add(c)
        if not out:
            return True
        # All clauses now depend only on nonpivot coordinates. Units can be
        # eliminated in this same coordinate system; prior rows are unnecessary.
        if units:
            clauses = tuple(out)
            equations = tuple(units)
            continue
        ordered = sorted(out, key=lambda c: (len(c), c))
        kept = []
        kept_sets = []
        for c in ordered:
            s = frozenset(c)
            if not any(t <= s for t in kept_sets):
                kept.append(c)
                kept_sets.append(s)
        used = 0
        for c in kept:
            for mask, _ in c:
                used |= mask
        columns = [i for i in range(n) if used & (1 << i)]
        def dense(mask):
            result = 0
            for new, old in enumerate(columns):
                if mask & (1 << old):
                    result |= 1 << new
            return result
        key_clauses = tuple(sorted(
            (tuple(sorted((dense(mask), const) for mask, const in c)) for c in kept),
            key=lambda c: (len(c), c)))
        return len(columns), key_clauses


def normalize(clauses, n, equations=(), stats=None):
    """Affine normalization plus safe coordinate-level pure-literal elimination.

    A coordinate appearing inside any multi-coordinate affine form is not
    eligible. Every remaining occurrence must be the same singleton polarity.
    """
    while True:
        key = normalize_base(clauses, n, equations)
        if key is True or key is False:
            return key
        n, clauses = key
        signs = {}
        forbidden = 0
        for clause in clauses:
            for mask, const in clause:
                if mask.bit_count() != 1:
                    forbidden |= mask
                else:
                    signs.setdefault(mask, set()).add(const)
        equations = tuple((mask, next(iter(values)) ^ 1)
                          for mask, values in sorted(signs.items())
                          if len(values) == 1 and not (mask & forbidden))
        if not equations:
            return key
        if stats is not None:
            stats.pure_assignments += len(equations)


def split_components(key):
    """Disjoint coordinate-support components, independently densely named."""
    n, clauses = key
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a,b):
        a,b=find(a),find(b)
        if a != b:
            parent[max(a,b)] = min(a,b)
    supports=[]
    for clause in clauses:
        support=0
        for mask,_ in clause:
            support |= mask
        cols=[i for i in range(n) if support & (1 << i)]
        for i in cols[1:]:
            union(cols[0],i)
        supports.append(cols)
    groups={}
    for clause,cols in zip(clauses,supports):
        groups.setdefault(find(cols[0]),[]).append(clause)
    result=[]
    for cs in groups.values():
        used=0
        for c in cs:
            for mask,_ in c:
                used |= mask
        cols=[i for i in range(n) if used & (1 << i)]
        def dense(mask):
            return sum(1 << j for j,i in enumerate(cols) if mask & (1 << i))
        cs=tuple(sorted((tuple(sorted((dense(m),b) for m,b in c)) for c in cs),
                        key=lambda c:(len(c),c)))
        result.append((len(cols),cs))
    return tuple(sorted(result,key=lambda item:(item[0],len(item[1]),item[1])))


def solve(cnf, n=None, *, cache=True, max_states=None):
    """Return (Boolean answer, Stats). max_states is test instrumentation only.

    Exceeding max_states raises RuntimeError, never a SAT or UNSAT answer.
    Even cache=False retains a seen-key set for state-count instrumentation;
    it is not the polynomial-space version of the mathematical procedure.
    """
    cnf = tuple(tuple(c) for c in cnf)
    maximum = max((abs(x) for c in cnf for x in c), default=0)
    if n is None:
        n = maximum
    if n < maximum or n < 0:
        raise ValueError('n must cover every input variable')
    stats = Stats(input_variables=n)
    # Sparse or enormous variable labels must not create enormous bit vectors.
    # Relabel occurring variables by increasing original index before all work.
    names = sorted({abs(x) for c in cnf for x in c})
    if 0 in names:
        raise ValueError('Literal 0 is not permitted')
    dense_names = {old: new+1 for new, old in enumerate(names)}
    cnf = tuple(tuple(dense_names[abs(x)] if x > 0 else -dense_names[abs(x)]
                      for x in c) for c in cnf)
    n = len(names)
    cnf, n = to_3cnf(cnf, n)
    stats.expanded_variables = n
    clauses, equations, stats.parity_blocks = extract_parity(cnf)
    memo = {}
    seen = set()

    # Explicit DFS handles OR branches and AND components without recursion.
    stack = []
    work = (clauses, n, equations, 0)
    answer = None
    while True:
        if work is not None:
            clauses, dim, equations, depth = work
            work = None
            stats.calls += 1
            stats.normalize_calls += 1
            stats.max_depth = max(stats.max_depth, depth)
            key = normalize(clauses, dim, equations, stats)
            if key is True or key is False:
                answer = key
            elif cache and key in memo:
                stats.cache_hits += 1
                answer = memo[key]
            else:
                if key not in seen:
                    seen.add(key)
                    stats.unique_states += 1
                if max_states is not None and stats.unique_states > max_states:
                    raise RuntimeError('state budget exceeded')
                dim, cs = key
                stats.max_free_dimension = max(stats.max_free_dimension, dim)
                stats.max_literals = max(stats.max_literals, sum(map(len, cs)))
                components = split_components(key)
                if len(components) > 1:
                    stats.component_splits += 1
                    mode = 'and'
                    tasks = [(part_cs,part_dim,(),depth+1)
                             for part_dim,part_cs in components]
                else:
                    mask, const = cs[0][0]
                    assert mask != 0
                    stats.branches += 1
                    mode = 'or'
                    tasks = [(cs,dim,((mask,const),),depth+1),
                             (cs,dim,((mask,const ^ 1),),depth+1)]
                work = tasks.pop(0)
                stack.append({'key':key,'mode':mode,'tasks':tasks})
                continue
        if not stack:
            return answer, stats
        frame = stack[-1]
        short_circuit = ((frame['mode']=='or' and answer)
                         or (frame['mode']=='and' and not answer))
        if not short_circuit and frame['tasks']:
            work = frame['tasks'].pop(0)
            continue
        if cache:
            memo[frame['key']] = answer
        stack.pop()


def brute(cnf, n):
    return any(all(any(bool(a & (1 << (abs(lit)-1))) == (lit > 0)
                       for lit in c) for c in cnf) for a in range(1 << n))

if __name__ == '__main__':
    import json, sys
    data = json.load(sys.stdin)
    answer, stats = solve(data['clauses'], data.get('n'))
    print(json.dumps({'satisfiable': answer, 'stats': asdict(stats)}, sort_keys=True))
