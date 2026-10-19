#!/usr/bin/env python3
"""Exact, independent checks; finite verification is not the proof."""
import json, math
from pathlib import Path
import sympy as s
L=s.symbols('L')
def require(condition, detail='exact check failed'):
    if not condition:
        raise RuntimeError(detail)
out=Path(__file__).parent

def homog(xs,d):
    a=[s.Integer(1)]+[s.Integer(0)]*d
    for x in xs:
        for j in range(1,d+1):
            a[j]=s.expand(a[j]+x*a[j-1])
    return a[d]

cases=[]
for nodes in [(-2,0,3),(-3,-1,2,5),(-4,-1,0,2,7)]:
    n=len(nodes)
    for d in range(1,5):
        h=3
        background=list(range(h,h+n-2))+[h+n-2+d]
        xs=[L+a for a in nodes]
        H=homog(xs,d); B=homog(xs,d-1)
        require(s.expand(s.diff(H,L)-(n+d-1)*B)==0)
        for k in sorted(set([0,1,2,h+n-2,h+n-1,h+n+d,h+n+d+1])-set(background)):
            ell=k-h; exps=background+[k]; c=n-1
            lap=[]; reduced=[]
            G=s.prod(x**h for x in xs)
            delta=s.prod(nodes[j]-nodes[i] for i in range(n) for j in range(i+1,n))
            factor=(-1)**(n-1+c)*G*delta
            for i in range(n):
                others=[j for j in range(n) if j!=i]
                minor=s.Matrix([[xs[j]**b for b in background] for j in others]).det(method='domain-ge')
                T=s.expand((-1)**(i+c)*xs[i]**k*minor)
                D=s.prod(nodes[i]-nodes[j] for j in others)
                R=xs[i]**ell*(H-xs[i]*B)/D
                require(s.cancel(T-factor*R)==0)
                lap.append(T); reduced.append(R)
            degree=max(s.degree(x,L) for x in lap)
            C=s.Matrix([[s.Poly(x,L).nth(j) for x in lap] for j in range(degree+1)])
            rank=C.rank()
            if d%2 or k<h or math.gcd(d//2,n-1)==1:
                require(rank==n, (nodes,d,k,rank))
            # Direct ODE identity for an arbitrary fixed nonzero weight vector.
            weights=[(-1)**i*(i+2) for i in range(n)]
            Q=lambda j: sum(weights[i]/s.Integer(s.prod(nodes[i]-nodes[t] for t in range(n) if t!=i))*xs[i]**j for i in range(n))
            relation=H*Q(ell)-B*Q(ell+1)
            if ell!=-1:
                Y=Q(ell+1)
                require(s.cancel((n+d-1)*H*s.diff(Y,L)-(ell+1)*s.diff(H,L)*Y-(n+d-1)*(ell+1)*relation)==0)
            cases.append({'nodes':nodes,'h':h,'d':d,'k':k,'rank':rank,'n':n,'negative_offset':ell<0,'log_exception':ell==-1})
z=s.symbols('n', positive=True)
r4=s.factor((5*(z+2)*(z+3)/(3*z*(z+1))-1)/2)
r6=s.factor((125*(z+2)*(z+3)*(z+4)*(z+5)/(z*z*(z+1)**2)-90*r4-15)/120)
expected4=(z*z+11*z+15)/(3*z*(z+1))
expected6=(2*z**4+34*z**3+202*z*z+470*z+375)/(3*z*z*(z+1)**2)
expecteddiff=(z**4+22*z**3+176*z*z+455*z+375)/(3*z*z*(z+1)**2)
require(s.cancel(r4-expected4)==0)
require(s.cancel(r6-expected6)==0)
require(s.cancel(r6-r4-expecteddiff)==0)
result={'moment_algebra_exact': True, 'case_count':len(cases),'all_factorizations_and_odes_exact':True,'all_required_independence_checks_passed':True,'cases':cases}
(out/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='cases'}))
