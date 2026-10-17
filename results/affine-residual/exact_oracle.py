from itertools import product,combinations

def sat_witness(clauses,n=None):
    clauses=tuple(tuple(c) for c in clauses)
    inferred=max((abs(l) for c in clauses for l in c),default=0)
    if n is None:n=inferred
    if n<inferred or any(l==0 for c in clauses for l in c):raise ValueError('invalid variable count/index')
    for values in product((False,True),repeat=n):
        if all(any(values[abs(l)-1]==(l>0) for l in c) for c in clauses):return values
    return None

def canonical_clauses(n):
    return tuple(tuple((i+1)*s for i,s in enumerate(signs) if s) for signs in product((0,1,-1),repeat=n))

def canonical_formulas(n,max_clauses=None):
    clauses=canonical_clauses(n)
    upper=len(clauses) if max_clauses is None else min(max_clauses,len(clauses))
    for size in range(upper+1):yield from combinations(clauses,size)

if __name__=='__main__':
    assert sat_witness(())==()
    assert sat_witness(((),)) is None
    assert sat_witness(((1,-1),)) is not None
    assert sat_witness(((1,),(-1,))) is None
    print('Direct-definition oracle edge cases passed')
