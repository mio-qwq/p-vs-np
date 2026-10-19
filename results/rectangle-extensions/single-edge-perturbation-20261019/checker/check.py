#!/usr/bin/env python3
"""Exact independent certificates; Python standard library only.

No assert statements: every check remains active under python -O.
All polynomials are coefficient lists in ascending Lambda degree.
"""
from fractions import Fraction as Q
from itertools import permutations, combinations
from math import comb, factorial, prod
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent

def require(test, message):
    if not test:
        raise RuntimeError(message)

def trim(p):
    p=list(p)
    while p and p[-1]==0: p.pop()
    return p

def add(p,q,scale=1):
    z=[0]*max(len(p),len(q))
    for i,x in enumerate(p): z[i]+=x
    for i,x in enumerate(q): z[i]+=scale*x
    return trim(z)

def mul(p,q):
    if not p or not q: return []
    z=[0]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q): z[i+j]+=x*y
    return trim(z)

def power(a,e): return [comb(e,k)*a**(e-k) for k in range(e+1)]
def sign(p): return (-1)**sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))
def vand(v): return prod(v[j]-v[i] for i in range(len(v)) for j in range(i+1,len(v)))
def H(n): return prod(factorial(i) for i in range(n))

def determinant(a,e,red):
    n=len(a)
    require(len(e)==n,'nonsquare input')
    entries=[[power(x,y) for y in e] for x in a]
    result={}
    feasible=set()
    for perm in permutations(range(n)):
        t=sum((i,perm[i]) in red for i in range(n))
        feasible.add(t)
        p=[1]
        for i,j in enumerate(perm): p=mul(p,entries[i][j])
        result[t]=add(result.get(t,[]),p,sign(perm))
    return {k:v for k,v in result.items() if v},feasible

def matrix_det(a):
    a=[list(map(Q,row)) for row in a]; n=len(a); d=Q(1)
    for c in range(n):
        p=next((i for i in range(c,n) if a[i][c]),None)
        if p is None: return Q(0)
        if p!=c: a[p],a[c]=a[c],a[p];d=-d
        v=a[c][c];d*=v
        for j in range(c,n): a[c][j]/=v
        for i in range(c+1,n):
            v=a[i][c]
            for j in range(c,n): a[i][j]-=v*a[c][j]
    return d

def rank(a):
    a=[list(map(Q,row)) for row in a]
    if not a or not a[0]: return 0
    n=len(a);rank_=0
    for c in range(len(a[0])):
        p=next((i for i in range(rank_,n) if a[i][c]),None)
        if p is None: continue
        a[p],a[rank_]=a[rank_],a[p]
        v=a[rank_][c]
        a[rank_]=[x/v for x in a[rank_]]
        for i in range(n):
            if i==rank_:continue
            v=a[i][c]
            a[i]=[x-v*y for x,y in zip(a[i],a[rank_])]
        rank_+=1
        if rank_==n:break
    return rank_

def moments(e,J,q):
    X=[e[j] for j in sorted(J)];Y=[e[j] for j in range(len(e)) if j not in J]
    rho=[Q(prod(x-y for y in Y),prod(x-v for v in X if v!=x)) for x in X]
    mu=[sum(w*x**l for x,w in zip(X,rho)) for l in range(len(X)+q)]
    piv=[]
    for c in range(len(X)):
        cols=piv+[c]
        if rank([[mu[i+j] for j in cols] for i in range(q)])>len(piv):piv.append(c)
    require(len(piv)==q,'moment rank')
    shape=list(reversed([b-j for j,b in enumerate(piv)]))
    k=sum(shape)
    gamma=matrix_det([[mu[i+j] for j in piv] for i in range(q)])
    return {'pivots':piv,'shape':shape,'loss':k,'gamma':gamma,'moments':mu}

def elementary(a,k): return sum(prod(t) for t in combinations(a,k))
def homogeneous(a,k):
    h=[Q(1)]+[Q(0)]*k
    for x in a:
        for j in range(1,k+1):h[j]+=x*h[j-1]
    return h[k]
def rising(x,k):return prod(x+i for i in range(k))
def falling(x,k):return prod(x-i for i in range(k))

def leading_data(a,e,I,J,q):
    n=len(a);r=len(I);M=n-r
    A=[a[i] for i in sorted(I)];C=[a[i] for i in range(n) if i not in I]
    X=[e[j] for j in sorted(J)];Y=[e[j] for j in range(n) if j not in J]
    mo=moments(e,J,q);shape=mo['shape'];k=mo['loss']
    if not k:B=Q(1)
    elif q==1:
        B=sum(Q((-1)**u)*elementary(A,u)*homogeneous(C,k-u)/
              (falling(r,u)*rising(M,k-u)) for u in range(k+1))
    elif all(x==1 for x in shape):
        B=sum(Q((-1)**u)*homogeneous(A,u)*elementary(C,q-u)/
              (rising(r,u)*falling(M,q-u)) for u in range(q+1))
    else:raise RuntimeError('unsupported Schur shape in finite checker')
    Av=Q((-1)**sum(I)*vand(A)*vand(C),H(r)*H(M))
    K=(-1)**sum(J)*vand(X)*vand(Y)
    eps=(-1)**(q*(n-q))
    const=Av*K*eps*mo['gamma']*B
    raw=sum(e)-comb(r,2)-comb(M,2)
    return {**mo,'row_factor':B,'constant':const,'raw_degree':raw,'degree':raw-k}

def coeffs_at(f,d):return {t:p[d] for t,p in f.items() if len(p)>d and p[d]}
def shifted_power_w(k,c=1,zshift=0):return {t+zshift:c*(-1)**(k-t)*comb(k,t) for t in range(k+1)}
def jsonable(v):
    if isinstance(v,Q):return str(v)
    if isinstance(v,dict):return {str(k):jsonable(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [jsonable(x) for x in v]
    return v

def run_case(name,a,e,I,J,p,c,q):
    n=len(a);r=len(I)
    require(len(set(a))==n and len(set(e))==n and min(e)>=0,'input distinctness')
    require(p not in I and c not in J,'added edge must be blue')
    require(max(a[i] for i in I)<min(a[i] for i in range(n) if i not in I) or
            max(a[i] for i in range(n) if i not in I)<min(a[i] for i in I),'separation')
    red={(i,j) for i in I for j in J}
    rect,feas_rect=determinant(a,e,red)
    new,feas=determinant(a,e,red|{(p,c)})
    require(feas==set(range(r+2)),'actual target feasibility')
    rows=[i for i in range(n) if i!=p];cols=[j for j in range(n) if j!=c]
    Im={rows.index(i) for i in I};Jm={cols.index(j) for j in J}
    am=[a[i] for i in rows];em=[e[j] for j in cols]
    minor,minor_feas=determinant(am,em,{(i,j) for i in Im for j in Jm})
    rhs={t:list(poly) for t,poly in rect.items()}
    for t,poly in minor.items():
        term=mul(power(a[p],e[c]),poly)
        rhs[t]=add(rhs.get(t,[]),term,-(-1)**(p+c))
        rhs[t+1]=add(rhs.get(t+1,[]),term,(-1)**(p+c))
    rhs={t:v for t,v in rhs.items() if v}
    require(new==rhs,'full rank-one cofactor identity')
    dat=leading_data(a,e,I,J,q);dm=leading_data(am,em,Im,Jm,q)
    require(coeffs_at(rect,dat['degree'])==shifted_power_w(r,dat['constant']),'original leading coefficient')
    require(max(len(v)-1 for v in rect.values())==dat['degree'],'original degree')
    if n>=2*r+q+1:
        require(dm['loss']<=dat['loss']+q,'loss inequality')
        require(coeffs_at(minor,dm['degree'])==shifted_power_w(r,dm['constant']),'minor leading coefficient')
        L=e[c]+dm['degree']
        require(L-dat['degree']>=n-r-q-1,'degree gap')
        predicted=shifted_power_w(r+1,(-1)**(p+c)*dm['constant'])
        require(coeffs_at(new,L)==predicted,'slack new leading coefficient')
        require(all(len(new[t])-1==L for t in range(r+2)),'slack fiber degrees')
    else:
        require(n==2*r+q,'tight boundary required')
        require(dm['pivots']==list(range(1,q+1)) and dm['loss']==q,'boundary pivots')
        require(coeffs_at(minor,dm['degree'])==shifted_power_w(r-1,dm['constant'],1),'boundary minor tie')
        require(0 not in minor_feas and new[0]==rect[0],'boundary zero fiber preservation')
        L=e[c]+dm['degree']
        if r>=2:
            require(L==dat['degree']+r-1,'boundary degree gap')
            require(coeffs_at(new,L)==shifted_power_w(r,(-1)**(p+c)*dm['constant'],1),'boundary leading polynomial')
            require(all(len(new[t])-1==L for t in range(1,r+2)),'boundary positive target degrees')
        else:
            i=next(iter(I));ratio=prod(Q(a[s]-a[i],a[s]-a[p]) for s in range(n) if s not in {i,p})
            require((-1)**(p+c)*dm['constant']/dat['constant']==ratio,'boundary ratio formula')
    return {'name':name,'a':a,'e':e,'I':sorted(I),'J':sorted(J),'edge':[p,c],
            'original':dat,'minor':dm,'fiber_degrees':{t:len(poly)-1 for t,poly in new.items()},
            'fiber_leading':{t:poly[-1] for t,poly in new.items()},'fibers':new}

results=[]
a=list(range(6));e=[0,1,2,4,5,6];I={0,1};J={0,3,4}
r=run_case('positive-loss slack',a,e,I,J,5,5,1)
require(r['original']['loss']==2 and r['original']['degree']==9 and r['original']['constant']==21600,'positive-loss expected original')
require(r['minor']['loss']==0 and r['fiber_degrees']=={t:14 for t in range(4)},'positive-loss expected edge')
require(r['fiber_leading']=={0:-20,1:60,2:-60,3:20},'positive-loss expected leading')
results.append(r)
# Reorder rows and columns independently to exercise original-index/cofactor signs.
rp=[4,0,5,2,1,3];cp=[5,2,0,4,1,3]
rperm=run_case('positive-loss reordered', [a[i] for i in rp],[e[j] for j in cp],
    {rp.index(i) for i in I},{cp.index(j) for j in J},rp.index(5),cp.index(5),1)
require(rperm['fibers']=={t:[sign(rp)*sign(cp)*v for v in poly] for t,poly in r['fibers'].items()},'full permutation signs')
results.append(rperm)
rneg=run_case('positive-loss reversed separation',[-x for x in a],e,I,J,5,5,1)
require(rneg['fibers']=={t:[(-1)**(sum(e)+k)*v for k,v in enumerate(poly)] for t,poly in r['fibers'].items()},'full reversed-offset homogeneity')
results.append(rneg)
r=run_case('tight boundary r2 q1',list(range(5)),list(range(5)),{0,1},{0,1,2},4,4,1)
require(r['fiber_degrees']=={0:6,1:7,2:7,3:7},'tight r2q1 exact degrees')
require(r['fiber_leading']=={0:2,1:-4,2:8,3:-4},'tight r2q1 exact leading')
results.append(r)
results.append(run_case('tight boundary r2 q2',list(range(6)),list(range(6)),{0,1},{0,1,2,3},5,5,2))
r=run_case('one-row leading obstruction',list(range(4)),list(range(4)),{0},{0,1,2},3,3,2)
require(r['fibers']=={0:[0,0,0,-2],1:[-42,-54,-18],2:[54,54,18,2]},'full one-row exact obstruction')
results.append(r)
# An equality-free tight one-row case and q=1 minimal boundary.
results.append(run_case('one-row unequal ratio', [0,1,2,4],list(range(4)),{0},{0,1,2},3,3,2))
results.append(run_case('minimal one-row q1 boundary',list(range(3)),list(range(3)),{0},{0,1},2,2,1))
output={'status':'PASS','arithmetic':'exact integer/Fraction, signed permutation expansion','cases':results}
(HERE/'results.json').write_text(json.dumps(jsonable(output),indent=2)+'\n')
print('PASS: '+str(len(results))+' exact cases; full cofactor identities, feasibility, signs, degree losses, boundary ties, and obstruction checked.')
