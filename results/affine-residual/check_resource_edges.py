import sys,random,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import arb
from test_families import pigeonhole
out={};big=(1<<200)+31
sparse=[([(big,)],True),([(big,),(-big,)],False),([(big,-big)],True),([],True)]
for cs,expected in sparse:
    answer,stats=arb.solve(cs,n=big+1)
    assert answer==expected
    assert stats.expanded_variables<=1
out['sparse_label_cases']=len(sparse);out['largest_label_bit_length']=big.bit_length()
rng=random.Random(5123)
for _ in range(300):
    n=rng.randrange(1,7)
    cs=[tuple(rng.choice((-1,1))*rng.randrange(1,n+1) for _ in range(rng.randrange(1,5))) for _ in range(rng.randrange(15))]
    assert arb.solve(cs,n,cache=True)[0]==arb.solve(cs,n,cache=False)[0]
out['cache_toggle_equivalence_cases']=300
old=sys.getrecursionlimit();sys.setrecursionlimit(50)
try:
    answer,stats=arb.solve([(2*i+1,2*i+2) for i in range(80)],160)
    assert answer is True and stats.max_depth==80
finally:sys.setrecursionlimit(old)
out['explicit_stack_depth_test']={'recursion_limit':50,'observed_search_depth':stats.max_depth,'answer':answer}
cs,n=pigeonhole(3)
try:arb.solve(cs,n,max_states=0)
except RuntimeError as exc:out['budget_limit']=str(exc)
else:raise AssertionError('budget must be exception, not SAT decision')
out['candidate_sha256']=hashlib.sha256(Path(arb.__file__).read_bytes()).hexdigest()
Path(__file__).resolve().with_name('resource_edge_results.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
