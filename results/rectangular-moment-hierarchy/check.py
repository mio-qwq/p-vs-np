"""Exact finite checks of the proved moment hierarchy; no sampling or remote writes."""
from itertools import combinations, permutations
from math import comb, factorial, prod
from fractions import Fraction as Q
from pathlib import Path
import json

OUT=Path(__file__).resolve().parent

def det(a):
    a=[list(map(Q,row)) for row in a]; n=len(a); ans=Q(1)
    for j in range(n):
        p=next((i for i in range(j,n) if a[i][j]),None)
        if p is None:return Q(0)
        if p!=j:a[p],a[j]=a[j],a[p];ans=-ans
        v=a[j][j];ans*=v
        for i in range(j+1,n):
            ratio=a[i][j]/v
            if ratio:
                for k in range(j+1,n):a[i][k]-=ratio*a[j][k]
    return ans

def delta(a):return prod(a[j]-a[i] for i in range(len(a)) for j in range(i+1,len(a)))
def H(m):return prod(factorial(i) for i in range(m))
def elementary(a,k):return sum(prod(c) for c in combinations(a,k))
def complete(a,k):
    h=[Q(1)]+[Q(0)]*k
    for x in a:
        for j in range(1,k+1):h[j]+=x*h[j-1]
    return h[k]
def falling(m,k):return prod(range(m-k+1,m+1))
def rising(m,k):return prod(range(m,m+k))
def qpoly(A,C,l):
    return sum(Q((-1)**j*elementary(A,j),falling(len(A),j))*Q(complete(C,l-j),rising(len(C),l-j)) for j in range(l+1))

def degree_lists(m,u):
    # Sorted k_i=i+d_i with 0<=d_0<=...<=d_(m-1), sum d_i=u.
    def rec(ds,total,lo):
        left=m-len(ds)
        if not left:
            if total==0:yield tuple(i+d for i,d in enumerate(ds))
            return
        for d in range(lo,total//left+1):yield from rec(ds+[d],total-d,d)
    yield from rec([],u,0)

def minor_coeffs(b,f,L):
    m=len(b);out=[]
    for u in range(L+1):
        value=Q(0)
        for ks in degree_lists(m,u):
            value+=det([[x**k for k in ks] for x in b])*det([[comb(e,k) if k<=e else 0 for e in f] for k in ks])
        out.append(value)
    return out

def max_layer(a,e,I,J,L):
    n=len(a);I=tuple(I);J=tuple(J);r=len(I);Ic=tuple(i for i in range(n) if i not in I)
    out=[Q(0)]*(L+1)
    for B in combinations(J,r):
        Bc=tuple(j for j in range(n) if j not in B)
        u=minor_coeffs([a[i] for i in I],[e[j] for j in B],L)
        v=minor_coeffs([a[i] for i in Ic],[e[j] for j in Bc],L)
        for l in range(L+1):out[l]+=(-1)**(sum(I)+sum(B))*sum(u[t]*v[l-t] for t in range(l+1))
    return out

def layer_leading(a,e,I,J,s):
    n=len(a)
    rows=sum((-1)**sum(A)*delta([a[i] for i in A])*delta([a[i] for i in range(n) if i not in A]) for A in combinations(I,s))
    cols=sum((-1)**sum(B)*delta([e[j] for j in B])*delta([e[j] for j in range(n) if j not in B]) for B in combinations(J,s))
    return Q(rows*cols,H(s)*H(n-s))

def layer_first(a,e,I,J,s):
    n=len(a);rows=[];cols=[]
    for R in combinations(I,s):
        Rc=[i for i in range(n) if i not in R]
        w=(-1)**sum(R)*delta([a[i] for i in R])*delta([a[i] for i in Rc])
        rows.append((w,Q(sum(a[i] for i in R),s),Q(sum(a[i] for i in Rc),n-s)))
    for B in combinations(J,s):
        Bc=[j for j in range(n) if j not in B]
        w=(-1)**sum(B)*delta([e[j] for j in B])*delta([e[j] for j in Bc])
        cols.append((w,sum(e[j] for j in B)))
    S0=sum(w for w,b in cols);S1=sum(w*b for w,b in cols)
    return Q(sum(w*(ma*(S1-comb(s,2)*S0)+mc*((sum(e)-comb(n-s,2))*S0-S1)) for w,ma,mc in rows),H(s)*H(n-s))

def layer_correction(a,e,I,J,s,t):
    # Independent factorized Cauchy–Binet sum at arbitrary correction t.
    n=len(a);value=Q(0)
    for u in range(t+1):
        for alpha in degree_lists(s,u):
            for beta in degree_lists(n-s,t-u):
                rows=Q(0);cols=Q(0)
                for R in combinations(I,s):
                    Rc=[i for i in range(n) if i not in R]
                    rows+=(-1)**sum(R)*det([[a[i]**h for h in alpha] for i in R])*det([[a[i]**h for h in beta] for i in Rc])
                for B in combinations(J,s):
                    Bc=[j for j in range(n) if j not in B]
                    cols+=(-1)**sum(B)*det([[comb(e[j],h) if h<=e[j] else 0 for j in B] for h in alpha])*det([[comb(e[j],h) if h<=e[j] else 0 for j in Bc] for h in beta])
                value+=rows*cols
    return value

def check_case(name,a,e,I,J):
    n=len(a);r=len(I);X=[e[j] for j in J];Y=[e[j] for j in range(n) if j not in J]
    k=next(k for k in range(1,r+2) if elementary(X,k)!=elementary(Y,k))
    Ic=[i for i in range(n) if i not in I];A=[a[i] for i in I];C=[a[i] for i in Ic]
    aa=Q((-1)**sum(I)*delta(A)*delta(C),H(r)*H(r+2))
    K=(-1)**sum(J)*delta(X)*delta(Y);dk=elementary(Y,k)-elementary(X,k)
    q=qpoly(A,C,k-1);prediction=aa*K*(-1)**(k-1)*dk*q
    actual=max_layer(a,e,I,J,k-1)
    if actual!=[Q(0)]*(k-1)+[prediction]:raise RuntimeError((name,'max layer',actual,prediction))
    smaller=[]
    for j in range(1,r+1):
        bound=k-j-2
        if bound<0:continue
        values=[layer_leading(a,e,I,J,r-j)]
        if bound>=1:values.append(layer_first(a,e,I,J,r-j))
        for t in range(2,bound+1):values.append(layer_correction(a,e,I,J,r-j,t))
        if any(values):raise RuntimeError((name,'smaller layer',j,values))
        smaller.append({'size':r-j,'coefficients':list(map(str,values))})
    result={'name':name,'r':r,'first_differing_moment':k,'D':sum(e)-comb(r,2)-comb(r+2,2),'q':str(q),'coefficient':str(prediction),'degree':sum(e)-comb(r,2)-comb(r+2,2)-k+1 if prediction else None,'maximal_layer_coefficients':list(map(str,actual)),'checked_smaller_layers':smaller}
    print(json.dumps(result),flush=True);return result

results=[]
results.append(check_case('n8 first two moments equal',list(range(8)),list(range(8)),(0,1,2),(0,3,5,6)))
results.append(check_case('n8 first moment equal',list(range(8)),list(range(8)),(0,1,2),(0,1,6,7)))
results.append(check_case('n6 gapped first two moments equal',list(range(6)),[0,1,2,4,5,6],(0,1),(0,3,4)))
# Prouhet binary parity partition: first three moments equal, fourth differs.
J=tuple(i for i in range(16) if i.bit_count()%2==0)
results.append(check_case('n8 gapped first three moments equal',list(range(8)),[0,1,4,7,9,12,15,16],(0,1,2),(0,3,4,7)))
results.append(check_case('n16 first three moments equal',list(range(16)),list(range(16)),tuple(range(7)),J))
results.append(check_case('n10 first four moments equal',list(range(10)),[0,1,2,4,8,10,14,16,17,18],(0,1,2,3),(1,2,5,6,9)))
# Non-principal rows, unsorted non-integer offsets and shuffled exponents.
results.append(check_case('unsorted rational offsets',list(map(Q,['3/2','-2','7/3','1/5','10','-4','6','-9/2'])),[6,0,7,2,3,1,5,4],(1,3,6),(0,1,4,6)))
(OUT/'results.json').write_text(json.dumps(results,indent=2)+'\n')
