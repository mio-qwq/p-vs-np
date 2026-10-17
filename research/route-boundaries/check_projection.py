"""Exact small-instance checks of assignment evaluation versus SAT projection."""
from itertools import product, combinations
import json

def ev_clause(c,x):
    return any(x[abs(l)-1] == (l>0) for l in c)
def sat(f,n):
    return any(all(ev_clause(c,x) for c in f) for x in product((False,True), repeat=n))
def projected_clause_shortcut(f,n):
    return all(any(ev_clause(c,x) for x in product((False,True),repeat=n)) for c in f)
def rails_eval(f,x):
    # Ordinary dual-rail CNF circuit: polynomial-size evaluation only.
    rails={(i+1,b): x[i]==b for i in range(len(x)) for b in (False,True)}
    return all(any(rails[abs(l),l>0] for l in c) for c in f)
counts=[]
for n in range(1,4):
    clauses=[]
    for signs in product((-1,0,1),repeat=n):
        clauses.append(tuple((i+1)*s for i,s in enumerate(signs) if s))
    checked=wrong=evals=0
    for r in range(4):
        for f in combinations(clauses,r):
            truth=sat(f,n)
            wrong+=projected_clause_shortcut(f,n)!=truth
            for x in product((False,True),repeat=n):
                assert rails_eval(f,x)==all(ev_clause(c,x) for c in f)
                evals+=1
            checked+=1
    counts.append(dict(n=n,formulas=checked,assignment_evaluations=evals,projection_shortcut_failures=wrong))
# Full point-local intersection does not combine values at different assignments.
u={0,1}; a={1}; b={0}
assert bool(a) and bool(b) and not bool(a&b)
assert sat(((1,),(-1,)),1) is False
assert projected_clause_shortcut(((1,),(-1,)),1) is True
out={'results':counts,'minimal_counterexample':[[1],[-1]],
     'counterexample_sat':False,'projected_clause_shortcut':True,
     'scope':'No shortcut was asserted by the source; this rejects a tempting proposed existential-projection shortcut.'}
print(json.dumps(out,indent=2))
