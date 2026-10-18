#!/usr/bin/env python3
"""Independent exact audit: quotient-ring interpolation and direct determinant.
No imports from the supplied checker or exploration artifacts.
"""
from pathlib import Path
import itertools, json, hashlib
import sympy as S

z,x,y,v=S.symbols('z x y v')
d,R,B,T,E1,E2,E3,E4=S.symbols('d R B T E1 E2 E3 E4')
checks=[]
def check(name, actual, expected=0):
    delta=S.factor(actual-expected)
    if delta != 0:
        raise ValueError(f'{name}: {delta}')
    checks.append(name)
    print('PASS',name,flush=True)

def falling(e,k):
    return S.prod(e-i for i in range(k))/S.factorial(k)

# In Q[E1,...,E4][x]/(x^4-E1*x^3+E2*x^2-E3*x+E4),
# evaluation at the four offsets multiplies a remainder matrix by a
# Vandermonde matrix. In Q[R,B,T][y]/(y^3-R*y^2+B*y-T),
# evaluation at r,s,t similarly produces their Vandermonde. The determinant
# below is therefore the pair coefficient divided by both Vandermondes.
qx=x**4-E1*x**3+E2*x*x-E3*x+E4
qy=y**3-R*y*y+B*y-T
px=[S.Poly(S.rem(x**k,qx,x),x) for k in range(11)]
py=[S.Poly(S.rem(falling(y,k),qy,y),y) for k in range(11)]
M=[]
for row in range(4):
    entries=[]
    # Entry series after factoring z^row. k<row cannot contribute.
    entries.append([S.expand(px[k].nth(row)*falling(d,k)) if k else S.Integer(0) for k in range(row,row+5)])
    for col in range(3):
        entries.append([S.expand(px[k].nth(row)*py[k].nth(col)) for k in range(row,row+5)])
    M.append(entries)

def convolve(a,b,limit):
    out=[S.Integer(0)]*(limit+1)
    for i,aa in enumerate(a):
        if aa == 0: continue
        for j,bb in enumerate(b[:limit-i+1]):
            if bb != 0: out[i+j]+=aa*bb
    return out

def det_coefficient(n,subs):
    out=0
    for perm in itertools.permutations(range(4)):
        inversions=sum(perm[i]>perm[j] for i in range(4) for j in range(i+1,4))
        prod=[S.Integer(1)]
        for row,col in enumerate(perm):
            series=[S.expand(e.subs(subs)) for e in M[row][col][:n+1]]
            prod=convolve(prod,series,n)
        out+=(-1)**inversions*prod[n]
    return S.factor(out)

# Substitute only previously established necessary relations, before each
# determinant coefficient is extracted. This is exact symbolic algebra,
# with d,R,T,E variables free; no numerical samples are used.
check('quotient C6',det_coefficient(0,{}),-d*(d*d-d*R+B)/12)
subB={B:d*R-d*d}
check('quotient C7 under C6',det_coefficient(1,subB),E1*T*d/48)
check('quotient C8 under C6,E1',det_coefficient(2,{**subB,E1:0}),E2*T*d*(2*R-3*d+15)/720)
sub9={B:d*(3*d-15)/2-d*d,R:(3*d-15)/2,E1:0}
check('quotient C9 under C6,E1,C8',det_coefficient(3,sub9),-E3*T*d*(d*d+95)/1920)
pair=-d*T*((5*T+4*d*d-460)*E2**2-(68*T+74*d*d-3050)*E4)/20160
check('quotient C10 under C6 through C9',det_coefficient(4,{**sub9,E3:0}),pair)

# Independent leading full determinant formula, via the leading degrees
# 0,1,2,3,4 and factorial Vandermonde, keeping outside exponents explicit.
r,s,t=S.symbols('r s t')
es=[0,d,r,s,t]
full_vand=S.prod(es[j]-es[i] for i in range(5) for j in range(i+1,5))
Vout=(s-r)*(t-r)*(t-s)
full=S.cancel(E4*full_vand/(S.prod(S.factorial(i) for i in range(5))*Vout))
check('full C10 before constraints',full,E4*d*r*s*t*(r-d)*(s-d)*(t-d)/288)
# Reduction of (r-d)(s-d)(t-d) through the cubic qy gives T-dB+d^2R-d^3.
full_reduced=E4*d*T*(T-d*B+d*d*R-d**3)/288
check('full C10 after C6',full_reduced.subs(subB),E4*d*T*T/288)
comp=d*T*((5*T+4*d*d-460)*E2**2+(2*T-74*d*d+3050)*E4)/20160
check('complement C10',E4*d*T*T/288-pair,comp)

# Compute the original polynomial determinant directly, using x^3 row
# pair sum/difference symmetry only in SymPy's polynomial determinant.
exponents=[0,3,5,8,9]
rows=[[x**e if e in {0,3,9} else 0 for e in exponents]]
rows += [[(x+b)**e for e in exponents] for b in [-1,1,-v,v]]
print('Computing original 5-by-5 determinant directly...',flush=True)
original=S.Poly(S.expand(S.Matrix(rows).det(method='domain-ge')),x)
check('original determinant degree at most 15',sum(c*x**mon[0] for mon,c in original.terms() if mon[0]>15))
c15=-864*v*(v*v-1)**2*(v**4-9*v*v+1)
c13=36*v*(v*v-1)**2*(v*v+1)*(23*v**4-282*v*v+23)
check('original x15 coefficient',original.nth(15),c15)
check('original x14 coefficient',original.nth(14))
check('original x13 coefficient',original.nth(13),c13)
check('original odd in x',original.as_expr()+original.as_expr().subs(x,-x))
check('exact candidate remainder',S.rem(c13,v**4-9*v*v+1,v),S.rem(-2700*v**3*(v*v-1)**2*(v*v+1),v**4-9*v*v+1,v))

u=S.symbols('u',real=True)
pair_inside=(5*T+4*d*d-460)*(u*u+v*v)**2-(68*T+74*d*d-3050)*u*u*v*v
comp_inside=(5*T+4*d*d-460)*(u*u+v*v)**2+(2*T-74*d*d+3050)*u*u*v*v
check('d7 complement',comp_inside.subs({d:7,T:-60}),-564*(u**4+v**4)-1824*u*u*v*v)
check('d3 pair',pair_inside.subs({d:3,T:40}),-224*(u**4+v**4)-784*u*u*v*v)
check('rho gap identity',(u*u+v*v)**2-4*u*u*v*v,(u*u-v*v)**2)
# At d=7, the necessary square sum is 65, so all entries lie in [-8,8].
d7=[q for q in itertools.combinations(range(-8,9),3) if sum(q)==3 and sum(a*a for a in q)==65]
if d7 != [(-5,2,6),(-4,0,7)]: raise ValueError(d7)
checks.append('d7 exhaustive integer arithmetic')
print('PASS d7 exhaustive integer arithmetic',d7,flush=True)
base=Path(__file__).parent
receipt={'status':'PASS','method':'quotient-ring interpolation and direct polynomial determinant','sympy':S.__version__,'checks':checks,'d7_triples':d7,'proof_sha256':hashlib.sha256((base/'PROOF.md').read_bytes()).hexdigest()}
(base/'audit_independent_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2),flush=True)
