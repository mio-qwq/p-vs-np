"""Exact independent audit of column-positive-functional deletion closure.
Standard-library only. Uses explicit failures rather than assert so -O is safe.
"""
from fractions import Fraction
from itertools import combinations, permutations, product
from math import comb
from search import laplace, mul

def require(value, message):
    if not value:
        raise RuntimeError(message)

def pad(p,n):
    return tuple(p)+tuple([0]*(n-len(p)))

def dot(x,y):
    return sum(a*b for a,b in zip(x,y))

def det_exact(M):
    """Independent exact Gaussian evaluation; not permutation expansion."""
    A=[[Fraction(x) for x in r] for r in M]
    n=len(A); d=Fraction(1)
    for c in range(n):
        pivot=next((r for r in range(c,n) if A[r][c]),None)
        if pivot is None:return Fraction(0)
        if pivot!=c:
            A[pivot],A[c]=A[c],A[pivot];d=-d
        pivotvalue=A[c][c];d*=pivotvalue
        for r in range(c+1,n):
            ratio=A[r][c]/pivotvalue
            for j in range(c+1,n):A[r][j]-=ratio*A[c][j]
            A[r][c]=0
    return d

def value(p,x):
    y=0
    for t in reversed(p):y=y*x+t
    return y

def verify_polynomials_by_elimination(a,e,c,removed,T):
    n=len(a);D=sum(e)
    # D+1 distinct points suffice for every claimed degree-at-most-D identity.
    for L in range(D+1):
        for s in range(n):
            M=[[(L+a[r])**e[j] if (r,j) not in removed and (j!=c or r==s) else 0
                for j in range(n)] for r in range(n)]
            require(det_exact(M)==value(T[s],L),f'independent determinant mismatch {(L,s)}')

# 1. The already published four-row positive functional is not deletion invariant.
a=(-3,-1,1,3);e=(0,1,2,4);c=1
original,original_counts=laplace(a,e,c)
require([t[1] for t in original]==[768]*4,'original four-row certificate')
removed={(0,3)}
T,counts=laplace(a,e,c,removed)
expected=[(0,768,896,0,-128,0,0,0),
          (648,-420,-612,120,224,44,-4,0),
          (648,1200,504,-96,-136,-80,8,0),
          (0,-204,76,-216,56,36,-4,0)]
require([tuple(t) for t in T]==expected,'four-row masked polynomials')
require(counts==[6,4,4,4],'four-row perfect matching counts')
require([Fraction(t[1],768) for t in T]==[Fraction(1),Fraction(-35,64),Fraction(25,16),Fraction(-17,64)],'four-row sign failure')
verify_polynomials_by_elimination(a,e,c,removed,T)
print('PASS: supplied four-row functional fails after one entry deletion; every distinguished-column edge extends to a perfect matching.')

# 2. Independently audit the stronger candidate supplied by the closure worker.
a=e=(0,1,2);c=1;removed={(1,0)}
T,counts=laplace(a,e,c,removed)
expected=[(0,1,2,1),(4,8,4,0),(-2,-5,-4,-1)]
require([tuple(t) for t in T]==expected,'three-row masked polynomials')
require(counts==[1,2,1],'three-row matching counts')
u=(Fraction(2,5),Fraction(1,5),Fraction(2,5))
require(all(dot(u,[t[k] for t in T])==0 for k in range(4)),'normalized nonnegative kernel')
require(all(x>0 for x in u) and sum(u)==1,'kernel normalization')
require(all(any(p) for p in T),'all masked Laplace polynomials nonzero')
verify_polynomials_by_elimination(a,e,c,removed,T)

original,_=laplace(a,e,c)
y=(4,-4,5,0)
require([dot(y,t) for t in original]==[2,4,2],'full canonical positive functional')
require([dot(y,t) for t in T]==[6,4,-8],'canonical same-functional failure')
require([sum(t[k] for t in T) for k in range(4)]==[2,4,2,0],'c0-only determinant')
require([sum(w*t[k] for w,t in zip((2,1,2),original)) for k in range(4)]==[0,-8,-4,0],'c1-only determinant')
for bits in product((0,1),repeat=3):
    if not any(bits):continue
    total=[sum(b*t[k] for b,t in zip(bits,T)) for k in range(4)]
    require(any(total),f'binary noncancellation {bits}')
print('PASS: canonical three-row deleted background has strictly positive rational kernel; all seven binary c1 masks remain nonzero.')

# 3. Test the symbolic arithmetic-progression family at independently varied integers.
for b,h in product(range(-3,4),range(-3,4)):
    if h==0:continue
    a=(b-h,b,b+h);e=(0,1,2)
    T,counts=laplace(a,e,1,{(1,0)})
    q=mul([b,1],[b,1])
    expected=[mul([b-h,1],q),[4*h*x for x in q],[-x for x in mul([b+h,1],q)]]
    require([tuple(t) for t in T]==[pad(t,4) for t in expected],'AP family formulas')
    require(all(sum(w*t[k] for w,t in zip((2,1,2),T))==0 for k in range(4)),'AP weighted kernel')
print('PASS: arithmetic-progression formulas checked on 42 integer parameter pairs; the proof is symbolic in PROOF.md.')
print('ALL EXACT CHECKS PASSED')
