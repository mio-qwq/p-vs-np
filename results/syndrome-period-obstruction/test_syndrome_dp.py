import random,json
from pathlib import Path
from syndrome_dp import *
r=random.Random(20261017); tests=0
for _ in range(1800):
    blocks=[]; rows=r.randrange(0,8)
    for i in range(r.randrange(0,5)):
        n=r.randrange(0,4)
        cls=[[r.choice([-1,1])*r.randrange(1,n+1) for _ in range(r.randrange(0,4))] for _ in range(r.randrange(0,5))] if n else ([[]] if r.randrange(2) else [])
        blocks.append({'columns':[r.randrange(1<<rows) for _ in range(n)],'clauses':cls})
    target=r.randrange(1<<rows)
    witness,stats=solve(blocks,target)
    assert (witness is not None)==(brute(blocks,target) is not None)
    if witness is not None:
        assert all(local_ok(b['clauses'],a) for b,a in zip(blocks,witness))
        v=0
        for b,a in zip(blocks,witness):
            for j,c in enumerate(b['columns']):
                if a>>j&1:v^=c
        assert v==target
    tests+=1
# Equality-star columns have cut rank one per split original variable.
for _ in range(500):
    n=r.randrange(1,8)
    cls=[[r.choice([-1,1])*r.randrange(1,n+1) for _ in range(r.randrange(1,5))] for _ in range(r.randrange(1,9))]
    blocks=clause_copies(cls)
    witness,stats=solve(blocks,0)
    truth=any(all(any(bool(a>>(abs(l)-1)&1)==(l>0) for l in c) for c in cls) for a in range(1<<n))
    assert (witness is not None)==truth
    for cut,w in enumerate(stats['widths']):
        left={abs(l) for c in cls[:cut] for l in c};right={abs(l) for c in cls[cut:] for l in c}
        assert w==len(left&right),(cls,cut,w,left&right)
# Saturating exponential family: equality pairs, all first copies then seconds.
growth=[]
for k in range(1,15):
    blocks=[{'columns':[1<<i], 'clauses':[]} for _ in range(2) for i in range(k)]
    witness,stats=solve(blocks,0)
    assert stats['counts'][k]==2**k
    growth.append({'k':k,'blocks':2*k,'middle_states':stats['counts'][k],'width':max(stats['widths'])})
# Unsound quotient: exact states 0 and 1 at first cut must remain distinct.
# A suffix unit x=0 extends only syndrome 0, although both share suffix-span coset.
quotient_example=[{'columns':[1],'clauses':[]},{'columns':[1],'clauses':[[-1]]}]
assert solve(quotient_example,0)[1]['counts']==[1,2,1]
out={'random_local_xor_tests':tests,'random_clause_copy_tests':500,'growth':growth,'quotient_counterexample_counts':[1,2,1]}
Path(__file__).with_name('results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
