"""Exact checks for identities and the false stronger lemma; not a general proof."""
from pathlib import Path
import json
import sympy as S
L=S.symbols('L')

def det_mask(a,e,p,c):
    n=len(a)
    return S.expand(S.det(S.Matrix([[0 if j==c and i in (0,p) else (L+a[i])**e[j] for j in range(n)] for i in range(n)])))

def schur(nodes,exps):
    n=len(nodes)
    d=S.prod(nodes[j]-nodes[i] for i in range(n) for j in range(i+1,n))
    return S.cancel(S.det(S.Matrix([[x**e for e in exps] for x in nodes]))/d)

# Full exact signed dependence, rather than a numerical evaluation.
a=[-3,-1,1,3];e=[0,1,2,4];c=1
T=[]
for s in range(4):
    M=S.Matrix([[(L+a[i])**e[j] for j in range(4) if j!=c] for i in range(4) if i!=s])
    T.append(S.expand((-1)**(s+c)*(L+a[s])**e[c]*M.det()))
expected=[-128*L**4+896*L**2+768*L,384*L**4-1152*L**2+768*L,-384*L**4+1152*L**2+768*L,128*L**4-896*L**2+768*L]
if T!=expected or S.expand(T[0]-T[1]-T[2]+T[3])!=0:
    raise RuntimeError('Signed dependence certificate failed')
C=S.Matrix([[S.Poly(t,L).nth(j) for t in T] for j in range(5)])
if C.rank()!=3 or C.nullspace()!=[S.Matrix([1,-1,-1,1])]:
    raise RuntimeError('Exact kernel check failed')

# Direct checks of the signed ratio in Section 3, with arbitrary positive nodes
# and three different normalized exponent tails. R need not equal one here.
ratio_checks=[]
for X,r,q in [([1,2,5],[0,1,3],2),([2,4,14,15],[0,1,2,4],2),([1,3,4,8,12],[0,2,5,6,9],1)]:
    m=len(X); Y=X[:q]+X[q+1:]
    B=S.Matrix([[x**b for b in r] for x in X])
    signed=(-1)**q*B.minor_submatrix(q,0).det()
    # Removing one staircase from the partition: s_mu(Y) has exponents r_j-1.
    sX=schur(X,r)
    sY=schur(Y,[b-1 for b in r[1:]])
    R=S.prod(S.Rational(y,y-X[q]) for y in Y)
    lhs=S.Rational(signed,B.det());rhs=S.cancel(R*sY/sX)
    if lhs!=rhs or not 0<sY<sX:
        raise RuntimeError('Schur ratio/sign check failed')
    ratio_checks.append({'nodes':X,'exponents':r,'row':q,'ratio':str(lhs),'R':str(R),'schur_without':str(sY),'schur_all':str(sX)})

# Three theorem routes on the same known simultaneous-resonance offsets.
# These corroborate implementation signs; the universal proof is PROOF.md.
a=[0,2,4,14,15];p=3
routes=[]
for label,e,c in [('second_smallest',[0,1,2,3,5],1),('even_rank',[0,7,10,17,22],2),('diagonal_hole',[0,1,2,3,15],3)]:
    # Boundary value avoids constructing the large full polynomial.
    B=S.Matrix([[0 if i in (0,p) and j==c else S.Integer(a[i])**e[j] for j in range(5)] for i in range(5)])
    value=B.det()
    if value==0 or sum(e)!=5*e[c]+6:
        raise RuntimeError('Boundary theorem route failed')
    if label=='diagonal_hole' and not value<0:
        raise RuntimeError('Diagonal sign failed')
    if label!='diagonal_hole' and not value>0:
        raise RuntimeError('Positive boundary sign failed')
    routes.append({'route':label,'exponents':e,'column':c,'boundary_value':str(value)})

out={'signed_dependency':{'offsets':[-3,-1,1,3],'exponents':[0,1,2,4],'column':1,'polynomials':[str(t) for t in T],'kernel':[1,-1,-1,1],'rank':3,'two_hole_middle':str(T[1]+T[2]),'zero_fiber_counterexample':False},'schur_ratio_checks':ratio_checks,'boundary_sign_checks':routes,'status':'passed','general_proof':'PROOF.md'}
Path(__file__).with_name('checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
