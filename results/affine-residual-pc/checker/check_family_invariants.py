"""Structural census independent of the repaired solver implementation."""
from itertools import product
import json
from pathlib import Path
from connected_family import connected_cycles,graph_components,pure_literals

def restrict_and_units(cnf,assignment):
    cs={frozenset(c) for c in cnf}
    values=dict(assignment)
    while True:
        out=set()
        for c in cs:
            if any(abs(l) in values and values[abs(l)]==(l>0) for l in c):continue
            d=frozenset(l for l in c if abs(l) not in values)
            if not d:return None,values
            out.add(d)
        units={next(iter(c)) for c in out if len(c)==1}
        if not units:return out,values
        if any(-l in units for l in units):return None,values
        values.update({abs(l):l>0 for l in units});cs=out

def dense_key(cnf):
    names=sorted({abs(l) for c in cnf for l in c});index={v:i+1 for i,v in enumerate(names)}
    return tuple(sorted(tuple(sorted(index[abs(l)]*(1 if l>0 else -1) for l in c)) for c in cnf))

def run():
    results=[];prefixes=0
    for k in range(9):
        cnf,n=connected_cycles(k);allkeys=set();counts=[]
        for depth in range(k+1):
            keys=set()
            for bits in product((False,True),repeat=depth):
                cs,assigned=restrict_and_units(cnf,dict(zip(range(1,depth+1),bits)))
                assert cs is not None
                assert pure_literals(cs)==[]
                assert len(graph_components(cs))==1
                assert sum(len(c)==3 for c in cs)==4+k-depth
                marker_variables=set(range(3*k+13,5*k+13))
                present={abs(l) for c in cs for l in c}
                assert marker_variables<=present
                retained=0
                for i in range(k):
                    a=3*k+13+2*i;b=a+1
                    has_star=frozenset((a,b)) in cs
                    expected=i<depth and bits[i] is False
                    assert has_star==expected
                    retained+=has_star
                assert retained==sum(not bit for bit in bits)
                key=dense_key(cs)
                assert key not in keys
                keys.add(key);prefixes+=1
            assert len(keys)==2**depth
            assert not allkeys.intersection(keys)
            allkeys.update(keys);counts.append(len(keys))
        results.append({'k':k,'variables':n,'clauses':len(cnf),'prefix_keys_by_depth':counts,'total_distinct_prefix_keys':len(allkeys)})
    # Negative control: break a marker cycle, purity detection must flag it.
    bad,n=connected_cycles(1)
    h=4;a=16;b=17
    bad.remove((-b,h))
    assert b in pure_literals(bad)
    out={'prefixes_checked':prefixes,'results':results,'negative_control':'Removing marker edge b->h exposes pure positive b, detected.'}
    Path(__file__).resolve().with_name('family_invariants.json').write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))
if __name__=='__main__':run()
