#!/usr/bin/env python3
"""Exact local controls for the written height-bound proof; not a finite search proof."""
import itertools
import json
import sympy as s

B,C,D,u,v=s.symbols('B C D u v')

def require(ok,msg):
    if not ok:
        raise RuntimeError(msg)

def parity(p):
    return (-1)**sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))

def bn(e,k):
    return s.prod(e-j for j in range(k))/s.factorial(k)

def convolve(a,b,N):
    return [sum(a[i]*b[k-i] for i in range(k+1)) for k in range(N+1)]

def determinant_coefficients(mask, offsets, exponents, N):
    out=[s.Integer(0)]*(N+1)
    for p in itertools.permutations(range(len(mask))):
        if not all(mask[i][p[i]] for i in range(len(mask))):
            continue
        f=[s.Integer(1)]+[s.Integer(0)]*N
        for i in range(len(mask)):
            f=convolve(f,[bn(exponents[p[i]],j)*offsets[i]**j for j in range(N+1)],N)
        out=[x+parity(p)*y for x,y in zip(out,f)]
    return [s.factor(x) for x in out]

mask4=[[1,1,0,0],[1,0,1,0],[1,1,1,1],[1,1,1,1]]
c=determinant_coefficients(mask4,[0,1,u,v],[0,B,C,D],4)
require(c[0]==0,'overlap4 C0')
require(s.expand(c[1]+(u-v)*(B+C-D))==0,'overlap4 C1')
c2=s.factor(c[2].subs(D,B+C))
require(s.expand(c2-B*C*(u-v)*(u+v-1))==0,'overlap4 C2 after C1')
c3=s.factor(c[3].subs(D,B+C).subs(v,1-u))
require(s.expand(c3+u*B*C*(u-1)*(2*u-1)*(B+C+2)/2)==0,'overlap4 C3 after C2')
c4=s.factor(c[4].subs(D,B+C).subs(v,1-u).subs(C,-B-2))
require(s.expand(c4-u*B*(u-1)*(2*u-1)*(B+1)*(B+2)/6)==0,'overlap4 C4 after C3')

# Every exponent-order gap yields at least one required nonempty Laplace class.
mask5=[[1,1,0,0,0],[1,0,1,0,0]]+[[1]*5 for _ in range(3)]
perms=[p for p in itertools.permutations(range(5)) if all(mask5[i][p[i]] for i in range(5))]
require(len(perms)==18,'exactly eighteen supported terms')
classes=[]
for size in range(1,5):
    for left_tuple in itertools.combinations(range(5),size):
        left=set(left_tuple); right=set(range(5))-left
        selected=left if len(left & {0,1,2})>=2 else right
        m=len(selected)
        rows={0,1,*range(2,m)}
        require(2<=m<=4,'chosen side size')
        members=[p for p in perms if {i for i in range(5) if p[i] in selected}==rows]
        require(bool(members),'chosen class nonempty')
        special=len(selected & {0,1,2})
        case='forced_partial_assignments' if special==2 else ('binary_determinant_minus_one' if m==3 else 'overlap_four')
        classes.append({'left_columns':sorted(left),'chosen_columns':sorted(selected),'chosen_rows':sorted(rows),'terms':len(members),'case':case})
require(len(classes)==30,'all nontrivial labelled cuts covered')
require(s.Matrix([[1,1,0],[1,0,1],[1,1,1]]).det()==-1,'three-row binary leading coefficient')
require(3*s.binomial(17,2)==408,'circuit bound arithmetic')
require(4*408==1632,'span bound arithmetic')

# Deliberately altered coefficient must fail the same exact-identity logic.
require(s.expand(c4-u*B*(u-1)*(2*u-1)*(B+1)*(B+2)/5)!=0,'negative coefficient control')
report={
    'status':'PASS',
    'scope':'Independent symbolic overlap-four coefficients and finite mask combinatorics only. The global bound rests on REVIEW.md proof, not this test.',
    'overlap_four_coefficients':{'C1':str(c[1]),'C2_after_C1':str(c2),'C3_after_C2':str(c3),'C4_after_C3':str(c4)},
    'supported_terms':len(perms),'cut_controls':classes,
    'gap_bound':408,'normalized_span_bound':1632,
    'negative_control':'altered C4 coefficient rejected'
}
print(json.dumps(report,indent=2,sort_keys=True))
