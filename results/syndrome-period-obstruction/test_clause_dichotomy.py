from itertools import product
from pathlib import Path
import json
from syndrome_dp import basis,clause_copies
from stabilizer_dp import local_sets
count=0
for columns in product(range(8),repeat=3):
    rank=len(basis(columns))
    image=set()
    for a in range(8):
        z=0
        for j,c in enumerate(columns):
            if a>>j&1:z^=c
        image.add(z)
    for forbidden in range(8):
        S=set()
        for a in range(8):
            if a==forbidden:continue
            z=0
            for j,c in enumerate(columns):
                if a>>j&1:z^=c
            S.add(z)
        periods={h for h in range(8) if {s^h for s in S}==S}
        if rank==3:assert len(S)==7 and periods=={0}
        else:assert S==image and periods==image
        count+=1
# Strict clauses, every variable repeated; period0 and expected spans.
clauses=[(1,2,3),(-1,2,4),(1,-3,4),(-2,3,-4)]
blocks=clause_copies(clauses)
for b,S in zip(blocks,local_sets(blocks)):
    assert len(S)==7 and len(basis(b['columns']))==3
    assert {h for h in S if {s^h for s in S}==S} in ({0},set()) # 0 may not lie in S
    s0=min(S)
    T={s^s0 for s in S}
    assert {h for h in T if {s^h for s in T}==T}=={0}
    assert len(basis(T))==3
out={'all_3_by_3_binary_maps_and_deleted_points':count,'strict_clause_copy_checks':len(blocks)}
Path(__file__).with_name('clause_dichotomy_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(out)
