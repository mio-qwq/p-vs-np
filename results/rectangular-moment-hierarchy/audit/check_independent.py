#!/usr/bin/env python3
"""Independent full-polynomial integer determinant reconstruction; stdlib only.
Does not import or reuse the producer's Cauchy--Binet/minor routines.
"""
from fractions import Fraction as Q
from itertools import combinations
from math import factorial, comb
from pathlib import Path
import json, hashlib


def det_bareiss(A):
    A=[list(row) for row in A]; n=len(A)
    if not n:return 1
    sign=1; old=1
    for k in range(n-1):
        pivot=next((i for i in range(k,n) if A[i][k]),None)
        if pivot is None:return 0
        if pivot!=k:A[k],A[pivot]=A[pivot],A[k];sign=-sign
        p=A[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                val=A[i][j]*p-A[i][k]*A[k][j]
                v,rem=divmod(val,old)
                if rem:raise RuntimeError('nonexact Bareiss division')
                A[i][j]=v
            A[i][k]=0
        old=p
    return sign*A[-1][-1]


def reconstruct(vals):
    # Conversion of Newton forward coefficients to ordinary monomials.
    out=[Q(0)]*len(vals); basis=[Q(1)]; row=list(vals)
    for k in range(len(vals)):
        for j,b in enumerate(basis):out[j]+=row[0]*b
        row=[row[j+1]-row[j] for j in range(len(row)-1)]
        nxt=[Q(0)]*(len(basis)+1)
        for j,b in enumerate(basis):nxt[j]-=b*k/(k+1);nxt[j+1]+=b/(k+1)
        basis=nxt
    if any(v.denominator!=1 for v in out):raise RuntimeError('noninteger polynomial')
    return [v.numerator for v in out]


def es(xs,k):return sum((product(v) for v in combinations(xs,k)),0)
def product(xs):
    ans=1
    for x in xs:ans*=x
    return ans

def hs(xs,k):
    a=[1]+[0]*k
    for x in xs:
        for j in range(1,k+1):a[j]+=x*a[j-1]
    return a[k]

def vd(xs):return product(xs[j]-xs[i] for i in range(len(xs)) for j in range(i+1,len(xs)))
def H(n):return product(factorial(j) for j in range(n))
def qval(a,I,l):
    r=len(I); X=[a[i] for i in I];Y=[a[i] for i in range(len(a)) if i not in I]
    return sum((Q((-1)**j*es(X,j)*hs(Y,l-j),product(r-h for h in range(j))*product(r+2+h for h in range(l-j))) for j in range(l+1)),Q(0))

def run(case):
    name,a,e,I,J=case; r=len(I);n=len(a); E=sum(e); X=[e[j] for j in J];Y=[e[j] for j in range(n) if j not in J]
    if n!=2*r+2 or len(J)!=r+1:raise RuntimeError('wrong dimensions')
    k=next(j for j in range(1,r+2) if es(X,j)!=es(Y,j))
    D=E-comb(r,2)-comb(n-r,2);degree=D-k+1
    A=Q((-1)**sum(I)*vd([a[i] for i in I])*vd([a[i] for i in range(n) if i not in I]),H(r)*H(n-r))
    K=(-1)**sum(J)*vd(X)*vd(Y)
    pred=A*K*(-1)**(k-1)*(es(Y,k)-es(X,k))*qval(a,I,k-1)
    # At most E in lambda and r in w, so this finite reconstruction is exact.
    lambda_columns=[]
    for w in range(r+1):
        vals=[]
        for x in range(E+1):
            vals.append(det_bareiss([[(x+a[i])**e[j]*(1+w if i in I and j in J else 1) for j in range(n)] for i in range(n)]))
        lambda_columns.append(reconstruct(vals))
    coeffs=[reconstruct([lambda_columns[w][d] for w in range(r+1)]) for d in range(E+1)]
    actual_degree=max(d for d,c in enumerate(coeffs) if any(c))
    if any(any(c) for c in coeffs[degree+1:]):raise RuntimeError(name+' nonzero coefficient above candidate')
    expected=[0]*r+[pred]
    if coeffs[degree]!=expected:raise RuntimeError(name+' candidate mismatch '+repr((coeffs[degree],expected)))
    # Direct extra evaluations verify code consistency independently of interpolation grid.
    for xx,ww in [(-19,7),(E+2,-3),(E+3,11)]:
        val=det_bareiss([[(xx+a[i])**e[j]*(1+ww if i in I and j in J else 1) for j in range(n)] for i in range(n)])
        interp=sum(sum(c*ww**j for j,c in enumerate(row))*xx**d for d,row in enumerate(coeffs))
        if val!=interp:raise RuntimeError(name+' evaluation inconsistency')
    # Audit the sharpened rank-cancellation bound against every full w layer.
    refined=[]
    for size in range(r+1):
        j=r-size
        first_loss=max(j*(j+2),k-1+j*(j+1))
        allowed=D-first_loss
        if any(coeffs[d][size] for d in range(max(0,allowed+1),E+1)):
            raise RuntimeError(name+' sharper layer-bound mismatch at size '+str(size))
        actual=max((d for d in range(E+1) if coeffs[d][size]),default=None)
        refined.append({'size':size,'degree_bound':allowed,'actual_degree':actual})
    # Direct lower-layer leading scalar, with no remainder reduction.
    lower=[]
    for s in range(r):
        ds=E-comb(s,2)-comb(n-s,2)
        if ds>=degree:
            total=sum((-1)**sum(B)*vd([e[b] for b in B])*vd([e[b] for b in range(n) if b not in B]) for B in combinations(J,s))
            lower.append({'size':s,'raw_degree':ds,'S':total})
            if ds==degree and total:raise RuntimeError(name+' interfering lower-layer leading scalar')
    result={'name':name,'a':a,'e':e,'I':I,'J':J,'k':k,'D':D,'predicted_degree':degree,'actual_degree':actual_degree,'predicted_scalar':str(pred),'q':str(qval(a,I,k-1)),'leading_w_coefficients':coeffs[actual_degree],'lower_layer_scalars':lower,'sharpened_layer_checks':refined,'nonzero_lambda_coefficients':{str(d):c for d,c in enumerate(coeffs) if any(c)}}
    print(name, 'k='+str(k),'D='+str(D),'degree='+str(actual_degree),'scalar='+str(pred),flush=True)
    return result

cases=[
 ('r1_k1_unsorted',[4,-2,1,7],[3,0,4,2],[2],[0,3]),
 ('r1_k2_unsorted',[4,-2,1,7],[3,0,4,1],[2],[0,3]),
 ('r1_k2_separated',[0,1,2,3],[0,1,2,3],[0],[0,3]),
 ('r1_k2_equal_means',[0,-2,-1,3],[0,1,2,3],[0],[0,3]),
 ('r2_k1_nonprincipal',[7,-3,2,9,0,4],[5,0,6,2,1,4],[1,4],[0,2,5]),
 ('r2_k2_gapped',[0,1,2,3,4,5],[0,1,2,3,4,6],[0,1],[0,2,5]),
 ('r2_k3_ideal',[0,1,2,3,4,5],[0,1,2,4,5,6],[0,1],[0,3,4]),
 ('r2_k3_integer_qzero',[-5,5,-13,-9,9,13],[0,1,2,4,5,6],[0,1],[0,3,4]),
 ('r2_k3_integer_qzero_shifted',[0,4,8,18,22,26],[0,1,2,4,5,6],[2,3],[0,3,4]),
 ('r2_k3_nonprincipal',[5,-4,2,8,0,-1],[5,2,0,6,1,4],[1,4],[0,2,5]),
 ('r3_k3_standard',[0,1,2,3,4,5,6,7],list(range(8)),[0,1,2],[0,3,5,6]),
 ('r3_k4_ideal',[0,1,2,3,4,5,6,7],[0,1,4,7,9,12,15,16],[0,1,2],[0,3,4,7]),
 ('r4_k5_ideal',list(range(10)),[0,1,2,4,8,10,14,16,17,18],[0,1,2,3],[1,2,5,6,9]),
 ('r4_k5_nonprincipal',[4,-2,8,11,0,15,7,-8,3,6],[10,0,18,4,2,16,1,17,14,8],[0,1,4,7],[0,2,4,6,8]),
 ('r3_k4_unsorted',[3,-5,8,1,0,7,-2,4],[9,1,16,4,0,12,7,15],[1,4,6],[0,2,4,6]),
]
if __name__=='__main__':
    results=[run(c) for c in cases]
    path=Path(__file__).with_name('independent-results.json')
    path.write_text(json.dumps(results,indent=2)+'\n')
    print('SHA256',hashlib.sha256(path.read_bytes()).hexdigest())
