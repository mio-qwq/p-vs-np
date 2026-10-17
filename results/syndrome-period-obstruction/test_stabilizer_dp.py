import random,json,itertools
from pathlib import Path
import stabilizer_dp as s
from syndrome_dp import brute
r=random.Random(17102026)
count=0
for rows in range(5):
 for _ in range(700):
    sets=[{v for v in range(1<<rows) if r.randrange(2)} for _ in range(r.randrange(5))]
    target=r.randrange(1<<rows)
    expected=False
    for choices in itertools.product(*sets):
        z=0
        for v in choices:z^=v
        if z==target:expected=True;break
    actual,stats=s.solve_sets(sets,target)
    assert actual==expected,(sets,target,stats)
    count+=1
# Exponential raw trellis family is entirely absorbed by independent periods.
growth=[]
for k in (1,2,4,8,16,64,256):
    sets=[{0,1<<i} for _ in range(2) for i in range(k)]
    ans,stats=s.solve_sets(sets,0)
    assert ans and max(stats['counts'])==1 and stats['period_rank']==k
    growth.append({'k':k,'period_rank':k,'max_quotient_states':1})
# Zero stabilizer does not mean small interface; sets {0,e_i,f_i} in duplicated blocks.
# At middle, all 3^k states are reachable and extendible; each block has no nonzero period.
barrier=[]
for k in range(1,9):
    one=[{0,1<<(2*i),1<<(2*i+1)} for i in range(k)]
    ans,stats=s.solve_sets(one+one,0)
    assert ans and stats['period_rank']==0 and stats['counts'][k]==3**k and max(stats['widths'])==2*k
    barrier.append({'k':k,'middle_states':3**k,'width':2*k,'period_rank':0})
# These sets arise from genuine two-variable local CNF (not a hidden set oracle).
blocks=[{'columns':[1,2],'clauses':[[-1,-2]]}]*2
assert s.local_sets(blocks)==[{0,1,2}]*2
assert s.solve(blocks,0)[0]==(brute(blocks,0) is not None)
out={'random_syndrome_set_tests':count,'affine_slack_growth':growth,'nonaffine_barrier':barrier}
Path(__file__).with_name('stabilizer_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
