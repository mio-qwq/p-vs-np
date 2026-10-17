import itertools,json,random
from pathlib import Path
OUT=Path(__file__).parent

def possible_coordinates(k):
    # R(z)=OR of selected state bits, or constant TRUE. Other fixed-pointwise
    # source values are absorbed in that constant.
    rs=[]
    for mask in range(1<<k):
        rs.append(tuple(bool(mask&z) for z in range(1<<k)))
    rs.append((True,)*(1<<k))
    return sorted({tuple(a and b for a,b in zip(l,r)) for l in rs for r in rs})

def check(F,k):
    def f(z):return sum(int(F[j][z])<<j for j in range(k))
    z=0;hist=[z]
    for t in range(k):
        zz=f(z);assert z&~zz==0
        z=zz;hist.append(z)
    assert f(z)==z
    # Directly check leastness among all fixed points.
    for w in range(1<<k):
        if f(w)==w:assert z&~w==0
    t=next(i for i in range(k+1) if f(hist[i])==hist[i])
    return t

rows=[]
for k in range(4):
    coords=possible_coordinates(k);count=0;maxround=0
    for F in itertools.product(coords,repeat=k):
        t=check(F,k);maxround=max(maxround,t);count+=1
    rows.append({'k':k,'distinct_coordinate_functions':len(coords),'maps_exhaustively_tested':count,'maximum_rounds_to_fixedpoint':maxround})
rng=random.Random(20261017);random_rows=[]
for k in [4,5,6,7,8]:
    coords=possible_coordinates(k);maxround=0
    for _ in range(2000):
        F=[rng.choice(coords) for j in range(k)]
        maxround=max(maxround,check(F,k))
    random_rows.append({'k':k,'maps_tested':2000,'maximum_observed_rounds':maxround})
# The bound k is exact for synchronous state iteration: z1'=1,zj'=z(j-1).
tight=[]
for k in range(1,13):
    F=[tuple(True for z in range(1<<k))]+[tuple(bool(z&(1<<(j-1))) for z in range(1<<k)) for j in range(1,k)]
    assert check(F,k)==k;tight.append(k)
report={'status':'all checks passed','exhaustive':rows,'random':random_rows,'tight_chain_k':tight,'scope':'pair-coordinate simultaneous update, not generic lattice iteration or internal gate-level schedule','seed':20261017}
(OUT/'pair_state_unrolling_results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
