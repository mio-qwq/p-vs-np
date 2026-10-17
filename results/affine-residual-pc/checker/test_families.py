"""Independent original-CNF test generators; no dependency on candidate solver."""
from itertools import combinations, product

def parity_clause_block(variables, rhs):
    return [tuple(-v if b else v for v,b in zip(variables,bits))
            for bits in product((0,1),repeat=len(variables)) if sum(bits)%2!=rhs]

def hide_clauses(cnf):
    n=max((abs(l) for c in cnf for l in c), default=0)
    hidden=[]
    for clause in cnf:
        if len(clause)<3: hidden.append(clause);continue
        n+=1
        hidden.extend([tuple(clause[:-1])+(n,),(-n,clause[-1])])
    return hidden,n

def pigeonhole(holes):
    pigeons=holes+1
    var=lambda p,h:p*holes+h+1
    clauses=[tuple(var(p,h) for h in range(holes)) for p in range(pigeons)]
    clauses.extend((-var(p,h),-var(q,h)) for p,q in combinations(range(pigeons),2) for h in range(holes))
    return clauses,pigeons*holes

def tseitin_complete4(rhs=1):
    edges=list(combinations(range(4),2));clauses=[]
    for v in range(4):
        variables=tuple(i+1 for i,e in enumerate(edges) if v in e)
        clauses.extend(parity_clause_block(variables,rhs if v==0 else 0))
    return clauses,len(edges)

def xor_chain(n,conflict=False):
    # Inputs 1..n, running sums n+1 .. 2n-1; force all inputs to zero.
    clauses=[(-i,) for i in range(1,n+1)]
    prev=1
    for i in range(2,n+1):
        output=n+i-1
        clauses.extend(parity_clause_block((prev,i,output),0));prev=output
    clauses.append((prev if conflict else -prev,))
    return clauses,2*n-1
