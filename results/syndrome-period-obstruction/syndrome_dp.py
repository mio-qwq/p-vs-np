"""Exact local-CNF / global-XOR syndrome DP. Integer bits encode equation rows."""
def basis(vectors):
    piv = {}
    for v in vectors:
        while v:
            p = v.bit_length()-1
            if p in piv: v ^= piv[p]
            else:
                piv[p] = v
                break
    return piv

def member(v, piv):
    while v:
        p=v.bit_length()-1
        if p not in piv: return False
        v ^= piv[p]
    return True

def local_ok(clauses, assignment):
    return all(any(bool(assignment >> (abs(l)-1)&1) == (l>0) for l in c) for c in clauses)

def solve(blocks, target):
    """blocks=[{'columns': [row-bitmasks], 'clauses': [local signed literals]}].
    Preconditions: nonnegative integer columns/target and well-formed local literals.
    Witness is a list of local assignment integers, or None. Explicit state counts.
    """
    if type(target) is not int or target<0: raise ValueError('target')
    for bl in blocks:
        if any(type(c) is not int or c<0 for c in bl['columns']): raise ValueError('columns')
        if any(type(l) is not int or not 1<=abs(l)<=len(bl['columns']) for cl in bl['clauses'] for l in cl): raise ValueError('literal')
    suffix=[None]*(len(blocks)+1)
    suffix[-1]={}
    for i in range(len(blocks)-1,-1,-1):
        suffix[i]=basis(list(suffix[i+1].values())+blocks[i]['columns'])
    if not member(target,suffix[0]): return None, {'counts':[0], 'widths':[]}
    states={0:()}; counts=[1]; widths=[0]; prefix=[]
    for i,bl in enumerate(blocks):
        choices={}
        for a in range(1<<len(bl['columns'])):
            if local_ok(bl['clauses'],a):
                contribution=0
                for j,c in enumerate(bl['columns']):
                    if a>>j&1: contribution ^= c
                choices.setdefault(contribution,a)
        following={}
        for s,path in states.items():
            for contribution,a in choices.items():
                z=s^contribution
                if member(target^z,suffix[i+1]): following.setdefault(z,path+(a,))
        prefix += bl['columns']
        u=basis(prefix); v=suffix[i+1]
        width=len(u)+len(v)-len(basis(list(u.values())+list(v.values())))
        states=following; counts.append(len(states)); widths.append(width)
        assert len(states)<=1<<width
    return states.get(target), {'counts':counts,'widths':widths}

def brute(blocks,target):
    from itertools import product
    for assignments in product(*(range(1<<len(bl['columns'])) for bl in blocks)):
        syndrome=0
        for bl,a in zip(blocks,assignments):
            if not local_ok(bl['clauses'],a): break
            for j,c in enumerate(bl['columns']):
                if a>>j&1: syndrome ^= c
        else:
            if syndrome==target: return assignments
    return None

def clause_copies(clauses):
    """Equisatisfiable CNF encoding: local clause copies + equality stars."""
    occurrences={}
    for i,c in enumerate(clauses):
        for j,l in enumerate(c): occurrences.setdefault(abs(l),[]).append((i,j))
    columns=[[0]*len(c) for c in clauses]; row=0
    for positions in occurrences.values():
        for p in positions[1:]:
            i,j=positions[0]; columns[i][j] ^= 1<<row
            i,j=p; columns[i][j] ^= 1<<row
            row+=1
    return [{'columns':cols, 'clauses':[[j+1 if l>0 else -(j+1) for j,l in enumerate(c)]]} for c,cols in zip(clauses,columns)]
