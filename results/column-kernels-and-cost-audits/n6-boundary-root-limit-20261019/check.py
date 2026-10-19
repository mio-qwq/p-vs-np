from pathlib import Path
import json
import sympy as s
q,Q=s.symbols('q Q')
h=[]
for r in range(16):
    if r==0:v=s.Integer(1)
    else:
        co=[2,-(q+s.Rational(11,9)),q+s.Rational(2,9),-2*q/9]
        v=sum(co[j-1]*h[r-j] for j in range(1,5) if r>=j)
    h.append(s.expand(v))
Z=s.factor(2*q/9*sum(h[:14])-2*h[14]+h[15])
G=23914845*q**7-96722262*q**6-311660622*q**5+1403896536*q**4-1763300097*q**3+989902134*q**2-259912971*q+21435980
if s.expand(Z+G/4782969)!=0:raise RuntimeError('Boundary polynomial mismatch')
ratios=[]
for t in [s.Rational(1,20),s.Rational(1,4)]:
    X=[t,s.Rational(1,3),s.Rational(2,3),1-t,s.Integer(1)]
    r=[0,1,2,3,17];B=s.Matrix([[x**e for e in r] for x in X])
    D=B.det();C=B.minor_submatrix(4,2).det()
    Y=X[:-1];Delta=s.prod(Y[j]-Y[i] for i in range(4) for j in range(i+1,4))
    value=s.factor(Z.subs(q,t*(1-t)))
    if s.cancel(D-C-Delta*value)!=0:raise RuntimeError('Raw-minor check failed')
    ratios.append({'t':str(t),'q':str(t*(1-t)),'Z':str(value),'deleted_to_full_ratio':str(C/D),'masked_sign':int(s.sign(D-C))})
if [r['masked_sign'] for r in ratios]!=[-1,1]:raise RuntimeError('Sign reversal failed')

# Exact binomial expansion in the symmetric normal form.
hA=[1,1,1+Q,1+Q];A=[]
for ell in range(4):
    v=(5*s.binomial(18,14-ell)-s.binomial(19,15-ell))*hA[ell]
    if ell:v+=s.binomial(18,15-ell)*hA[ell-1]
    A.append(s.expand(v))
c17=s.expand(A[1]-3*A[0]);c15=s.expand(A[3]-3*A[2]+3*A[1]-A[0])
if c17!=0 or c15!=-69768*Q-4080:raise RuntimeError('Degree-15 coefficient failed')
# Independent exact raw determinant coefficient for one rational symmetric input.
L=s.symbols('L');a=[-1,-s.Rational(3,4),-s.Rational(1,3),s.Rational(1,3),s.Rational(3,4),1];e=[0,1,2,3,4,18]
# Compute the two relevant cofactors directly; the full alternant has degree13.
cof=s.Matrix([[(L+a[i])**e[j] for j in range(6) if j!=3] for i in range(6) if i!=0])
# Leading truncated coefficients via expansion at infinity avoids a large full determinant.
z=s.symbols('z')
M=s.Matrix([[(1+a[i]*z)**e[j] for j in range(6) if j!=3] for i in range(6) if i!=0])
# The first unnormalized cofactor coefficient needed corresponds to z^13 in total degree28.
# Direct permutation coefficient convolution is independent of the Schur formula.
from itertools import permutations
from math import comb
N=13
coeff=s.Integer(0)
for perm in permutations(range(5)):
    inv=sum(perm[i]>perm[j] for i in range(5) for j in range(i+1,5))
    terms=[s.Integer(1)]
    factors=[(a[0],e[3])]+[(a[i],e[[j for j in range(6) if j!=3][perm[i-1]]]) for i in range(1,6)]
    for offset,exponent in factors:
        nxt=[s.Integer(0)]*min(N+1,len(terms)+exponent)
        for u,cv in enumerate(terms):
            for v in range(min(exponent,N-u)+1):nxt[u+v]+=cv*comb(exponent,v)*offset**v
        terms=nxt
    if len(terms)>N:coeff+=(-1)**(inv+3)*terms[N]
C0=-s.prod(a[j]-a[i] for i in range(1,6) for j in range(i+1,6))
expected=C0*(-69768*(a[1]**2+a[2]**2)-4080)
if s.expand(coeff-expected)!=0:raise RuntimeError('Independent cofactor coefficient failed')
out={'status':'passed','G':str(G),'boundary_ratios':ratios,'B_top_coefficients':[str(v) for v in A],'H_degree17':str(c17),'H_degree15':str(c15),'independent_raw_cofactor_degree15':str(coeff),'full_masked_degree':15,'full_zero_polynomial_counterexample':False}
Path(__file__).with_name('results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
