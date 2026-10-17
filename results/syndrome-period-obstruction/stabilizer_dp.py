"""Exact translation-stabilizer quotient followed by syndrome-set DP."""
from syndrome_dp import basis,member,local_ok

def reduce_vector(v,piv):
    for p in sorted(piv,reverse=True):
        if v>>p&1:v^=piv[p]
    return v

def local_sets(blocks):
    sets=[]
    for bl in blocks:
        S=set()
        for a in range(1<<len(bl['columns'])):
            if local_ok(bl['clauses'],a):
                v=0
                for j,c in enumerate(bl['columns']):
                    if a>>j&1:v^=c
                S.add(v)
        sets.append(S)
    return sets

def solve_sets(sets,target):
    if any(not S for S in sets):return False,{'empty_block':True}
    normalized=[]; periods=[]
    for S in sets:
        s0=min(S); target^=s0
        T={s^s0 for s in S}; normalized.append(T)
        # Since 0 belongs to T, every period belongs to T.
        periods.extend(h for h in T if all(t^h in T for t in T))
    H=basis(periods)
    normalized=[{reduce_vector(t,H) for t in T} for T in normalized]
    target=reduce_vector(target,H)
    suffix=[{} for _ in range(len(sets)+1)]
    for i in reversed(range(len(sets))):suffix[i]=basis(list(suffix[i+1].values())+list(normalized[i]))
    states={0} if member(target,suffix[0]) else set(); counts=[len(states)]; widths=[0]; prefix=[]
    for i,T in enumerate(normalized):
        states={s^t for s in states for t in T if member(target^s^t,suffix[i+1])}
        prefix+=list(T)
        U=basis(prefix);V=suffix[i+1]
        w=len(U)+len(V)-len(basis(list(U.values())+list(V.values())))
        assert len(states)<=1<<w
        counts.append(len(states)); widths.append(w)
    return target in states,{'period_rank':len(H),'counts':counts,'widths':widths,'quotient_set_sizes':list(map(len,normalized))}

def solve(blocks,target):return solve_sets(local_sets(blocks),target)
