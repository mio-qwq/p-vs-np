"""Independent full permutation expansion over Q(sqrt(2))."""
from fractions import Fraction as Q
from itertools import permutations
from math import comb
from pathlib import Path
import json

Z=(Q(0),Q(0)); O=(Q(1),Q(0))
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def mul(a,b):return (a[0]*b[0]+2*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def scale(a,c):return (a[0]*c,a[1]*c)
def power(a,k):
    ans=O
    for _ in range(k):ans=mul(ans,a)
    return ans

a=[(Q(0),Q(-1,2)),(Q(0),Q(1,2))]+[(Q(i),Q(0)) for i in [-2,-1,1,2]]
e=[0,1,2,4,5,6];J={0,3,4}
entries=[[[scale(power(a[i],ex-d),comb(ex,d)) for d in range(ex+1)] for ex in e] for i in range(6)]
F={}
for p in permutations(range(6)):
    sign=(-1)**sum(p[i]>p[j] for i in range(6) for j in range(i+1,6))
    t=sum(p[i] in J for i in range(2));poly=[O]
    for i in range(6):
        entry=entries[i][p[i]];out=[Z]*(len(poly)+len(entry)-1)
        for u,v in enumerate(poly):
            if v==Z:continue
            for w,b in enumerate(entry):
                if b!=Z:out[u+w]=add(out[u+w],mul(v,b))
        poly=out
    for d,c in enumerate(poly):F[d,t]=add(F.get((d,t),Z),scale(c,sign))
F={key:value for key,value in F.items() if value!=Z}
# Exact full polynomial supplied by a separate symbolic determinant computation.
# F = 9 sqrt(2) x [3560 x6(z-1)^2 + x4(-6380z2+9400z-3020)
#                 + x2(1150z2+1676z-2336) +1695z2-3712z+1478].
coeffs={7:[3560,-7120,3560],5:[-3020,9400,-6380],3:[-2336,1676,1150],1:[1478,-3712,1695]}
expected={(d,t):(Q(0),Q(9*c)) for d,row in coeffs.items() for t,c in enumerate(row)}
if F!=expected:raise RuntimeError(('Full bivariate polynomial mismatch',F,expected))
result={'method':'Signed sum of all 720 permutations over exact Q(sqrt(2))','D':11,'degree':max(d for d,t in F),'leading':'32040 sqrt(2) (z-1)^2','complete_coefficients':{str(d):[str(F[d,t][1])+' sqrt(2)' for t in range(3)] for d in sorted(coeffs,reverse=True)}}
Path(__file__).with_name('cancellation_result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
