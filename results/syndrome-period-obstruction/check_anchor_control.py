from itertools import combinations
from pathlib import Path
import json
# Any five anchors suffice; verify all assignments and every deleted clause's role.
F=[tuple(s*x for x in t) for t in combinations(range(1,6),3) for s in (1,-1)]
def evaluate(F,a):return all(any(bool(a>>(abs(l)-1)&1)==(l>0) for l in c) for c in F)
assert not any(evaluate(F,a) for a in range(32))
# Generic small-core detector is O(n^5*32*L), no NAE-specific recognition required.
def small_core(F,n,k=5):
    for V in combinations(range(1,n+1),min(k,n)):
        ren={v:i+1 for i,v in enumerate(V)}
        sub=[tuple((1 if l>0 else -1)*ren[abs(l)] for l in c) for c in F if all(abs(l) in ren for l in c)]
        if not any(evaluate(sub,a) for a in range(1<<len(V))): return V
    return None
assert small_core(F,5)==(1,2,3,4,5)
out={'anchor_variables':5,'anchor_clauses':len(F),'truth_table_assignments_checked':32,'unsat':True,'generic_small_core_detected':True}
Path(__file__).with_name('anchor_control_results.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
