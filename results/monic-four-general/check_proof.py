#!/usr/bin/env python3
"""Exact symbolic checks accompanying PROOF.md; not exponent/offset sampling.

Python 3 + installed SymPy. No network or downloaded code. Checks remain active
under python -O. Optional --write records the complete support orbit mapping.
"""
import argparse
import json
from functools import lru_cache
from itertools import combinations_with_replacement, permutations
from pathlib import Path
import sympy as S

p,q,r,b,c,t,u,h,n = S.symbols('p q r b c t u h n')
ES=(0,p,q,r)
PERMS=tuple(permutations(range(4)))
def require(ok,msg):
    if not ok: raise ValueError(msg)
def sign(pp):
    return (-1)**sum(pp[i]>pp[j] for i in range(4) for j in range(i+1,4))
@lru_cache(None)
def matchings(rows):
    return tuple(pp for pp in PERMS if all(rows[i]>>pp[i]&1 for i in range(4)))
def connected(ps):
    adj=[set() for _ in range(8)]
    for pp in ps:
        for i,j in enumerate(pp): adj[i].add(j+4);adj[j+4].add(i)
    seen={0};stack=[0]
    while stack:
        for v in adj[stack.pop()]-seen: seen.add(v);stack.append(v)
    return len(seen)==8

def map_rows(rows,pp):
    raw=tuple(sum(((row>>pp[j])&1)<<j for j in range(4)) for row in rows)
    rp=tuple(sorted(range(4),key=lambda i:(raw[i],i)))
    return tuple(raw[i] for i in rp),rp

def coverage():
    counts=dict(no_matching=0,nonzero_top=0,disconnected=0,connected_singular=0)
    cert=[];orbits={}
    for rows in combinations_with_replacement(range(1,16),4):
        ps=matchings(rows)
        if not ps:counts['no_matching']+=1;continue
        if sum(map(sign,ps)):counts['nonzero_top']+=1;continue
        if not connected(ps):counts['disconnected']+=1;continue
        counts['connected_singular']+=1
        rep,cp,rp=min((map_rows(rows,pp)[0],pp,map_rows(rows,pp)[1]) for pp in PERMS)
        require(map_rows(rows,cp)==(rep,rp),'bad orbit map')
        for i in range(4):
            for j in range(4):
                require((rep[i]>>j&1)==(rows[rp[i]]>>cp[j]&1),'bad entry map')
        cert.append(dict(rows=rows,representative=rep,column_permutation=cp,row_permutation=rp))
        orbits[rep]=orbits.get(rep,0)+1
    require(counts==dict(no_matching=1062,nonzero_top=940,disconnected=851,connected_singular=207),'support count changed')
    expected={(3,5,10,12):3,(3,5,10,15):12,(3,5,11,13):12,(3,5,14,14):12,
      (3,5,15,15):12,(3,7,11,12):6,(3,7,11,15):6,(3,7,12,15):12,
      (3,7,13,13):24,(3,7,15,15):12,(3,12,15,15):3,(3,13,13,14):12,
      (3,13,13,15):12,(3,13,14,15):6,(3,13,15,15):12,(3,15,15,15):6,
      (7,7,11,11):6,(7,7,11,13):12,(7,7,11,15):12,(7,7,15,15):4,
      (7,11,15,15):6,(7,15,15,15):4,(15,15,15,15):1}
    require(orbits==expected,'orbit representatives changed')
    print('PASS support coverage: 3060 row multisets, 207 residual classes, 23 orbits',flush=True)
    return counts,cert,set(orbits)

def choose(e,k):return S.prod(e-j for j in range(k))/S.factorial(k)
@lru_cache(None)
def coefficient(rows,k):
    out=0
    for pp in matchings(rows):
        for i in range(k+1):
            for j in range(k-i+1):
                l=k-i-j
                out+=sign(pp)*choose(ES[pp[1]],i)*choose(ES[pp[2]],j)*choose(ES[pp[3]],l)*b**j*c**l
    return S.factor(out)

def substituted(rows,k,ss):
    # Substitute before expansion for large, reduced expressions.
    out=0
    for pp in matchings(rows):
        for i in range(k+1):
            for j in range(k-i+1):
                l=k-i-j
                term=sign(pp)*choose(ES[pp[1]],i)*choose(ES[pp[2]],j)*choose(ES[pp[3]],l)*b**j*c**l
                out+=S.sympify(term).subs(ss,simultaneous=True)
    return S.factor(out)

CHECKS=0
COVERED=set()
def eq(name,left,right):
    global CHECKS
    require(S.cancel(left-right)==0,'identity failed: '+name)
    CHECKS+=1

def check_coefficients():
    direct=[((3,7,12,15),1,c*p),((3,7,13,13),1,-r*(b-c)),
      ((3,7,15,15),1,-p*(b-c)),((3,12,15,15),2,-p*(b-c)*(q-r)),
      ((3,13,13,14),1,-2*(b-1)*(q-r)),((3,13,13,15),1,-(b-1)*(q-r)),
      ((3,13,15,15),1,-(b-c)*(q-r)),((7,7,11,11),2,-p*(b-c)*(q-r)),
      ((7,7,11,15),1,-p),((7,11,15,15),1,p*(b-c)),
      ((7,15,15,15),3,p*q*(b-1)*(b-c)*(c-1)*(p-q)/2)]
    for rows,k,target in direct:
        COVERED.add(rows)
        for j in range(k):eq(f'{rows} C{j}',coefficient(rows,j),0)
        eq(f'{rows} C{k}',coefficient(rows,k),target)
    COVERED.add((3,5,10,12));require(len(matchings((3,5,10,12)))==2,'two-matchings case')
    rows=(15,15,15,15);COVERED.add(rows)
    for j in range(6):eq(f'full C{j}',coefficient(rows,j),0)
    eq('full C6',coefficient(rows,6),b*c*(b-1)*(c-1)*(c-b)*p*q*r*(q-p)*(r-p)*(r-q)/12)
    COVERED.add((3,15,15,15))
    # Check the recalled exceptional one-partial-row formulas separately.
    rows=(6,15,15,15);V=(b-1)*(c-1)*(c-b);B=p*q*(p-q)*(p+q)
    eq('partial C3 exceptional',substituted(rows,3,{r:p+q}),0)
    eq('partial C4 exceptional',substituted(rows,4,{r:p+q}),V*B*(1+b+c)/6)
    eq('partial C5 under sum zero',substituted(rows,5,{r:p+q,c:-1-b}),(V*B*(b+c+b*c)/6).subs(c,-1-b))
    print('PASS direct support and recalled partial-row coefficients',flush=True)

    rows=(3,5,11,13);COVERED.add(rows)
    require([[sum(pp[i]==j for pp in matchings(rows)) for j in range(4)] for i in range(4)]==[[1,3,0,0],[1,0,3,0],[1,1,0,2],[1,0,1,2]],'sparse matching counts A')
    # Independent monomial cofactors with symbolic base powers verify the
    # binomial structure used in the valuation argument.
    X=S.symbols('X0:16');M=S.Matrix(4,4,lambda i,j:X[4*i+j] if rows[i]>>j&1 else 0)
    eq('sparse row2 r cofactor',M.cofactor(2,3),X[1]*(X[4]*X[14]-X[6]*X[12]))
    eq('sparse row3 r cofactor',M.cofactor(3,3),-X[6]*(X[0]*X[9]-X[1]*X[8]))

    rows=(3,5,10,15);COVERED.add(rows)
    require([[sum(pp[i]==j for pp in matchings(rows)) for j in range(4)] for i in range(4)]==[[2,2,0,0],[1,0,3,0],[0,1,0,3],[1,1,1,1]],'sparse matching counts B')
    M=S.Matrix(4,4,lambda i,j:X[4*i+j] if rows[i]>>j&1 else 0)
    eq('sparse row0 zero cofactor',M.cofactor(0,0),-X[6]*(X[9]*X[15]-X[11]*X[13]))
    eq('sparse row0 p cofactor',M.cofactor(0,1),X[11]*(X[4]*X[14]-X[6]*X[12]))
    A=p+q-r;BB=2*p*(p-r)-A;E=2*p*q+A
    eq('351015 C1',coefficient(rows,1),b*(r-p)+c*A-q)
    eq('351015 C1 at A0',coefficient(rows,1).subs(r,p+q),q*(b-1))
    ss={c:(b*(p-r)+q)/A}
    eq('351015 C2',substituted(rows,2,ss),-q*(b-1)*(p-r)*(b*BB+E)/(2*A*A))
    TT=6*p*p*q+5*p*p-6*p*q*r-5*p*q-5*p*r-3*p-3*q+3*r
    ss={b:-E/BB,c:(q-(p-r)*E/BB)/A}
    eq('351015 C3',substituted(rows,3,ss),-p*p*q*(p-r)*A*TT/(3*BB**3))
    eq('351015 p1 factor',TT.subs(p,1),-S.Rational(2,3)*((3*q+1)*(3*r+1)-4))
    eq('351015 pminus1 factor',TT.subs(p,-1),S.Rational(2,3)*((3*q+4)*(3*r+4)-4))
    print('PASS sparse valuation structures and coefficients',flush=True)

    rows=(3,5,14,14);COVERED.add(rows)
    eq('351414 C1',coefficient(rows,1),-(b-c)*(p+q-2*r))
    eq('351414 C2',substituted(rows,2,{r:(p+q)/2}),-(b-c)*(p-q)*((b+c)*(p-q)+2*q)/4)
    ss={r:(p+q)/2,b:(u-q)/(p-q),c:(-u-q)/(p-q)}
    eq('351414 C3',substituted(rows,3,ss),u*(u*u+p*q)/(2*(p-q)))
    C4=substituted(rows,4,ss)
    num,den=S.fraction(C4)
    eq('351414 C4 remainder',S.rem(num,u*u+p*q,u)/den,-p*q*u*(p+q)/(3*(p-q)**2))

    rows=(3,5,15,15);COVERED.add(rows)
    eq('351515 C1',coefficient(rows,1),-(b-c)*(p+q-r))
    eq('351515 C2',substituted(rows,2,{r:p+q}),p*q*(b-c)*(b+c-1))
    eq('351515 C3',substituted(rows,3,{r:p+q,c:1-b}),-b*p*q*(b-1)*(2*b-1)*(p+q+2)/2)
    eq('351515 C4',substituted(rows,4,{r:-2,q:-p-2,c:1-b}),b*p*(b-1)*(2*b-1)*(p+1)*(p+2)/6)

    rows=(3,7,11,12);COVERED.add(rows)
    eq('371112 C1',coefficient(rows,1),-p*(b+1))
    eq('371112 C2',substituted(rows,2,{b:-1}),-p*(c*(q-r)+p-q-r-1))
    eq('371112 C3',substituted(rows,3,{b:-1,c:(q+r+1-p)/(q-r)}),p*(p-2*q-1)*(p-2*r-1)/(2*(q-r)))

    rows=(3,7,11,15);COVERED.add(rows)
    eq('371115 C1',coefficient(rows,1),-p*(b-c+1))
    eq('371115 C2',substituted(rows,2,{c:b+1}),b*p*(p-q-r-1))
    eq('371115 C3',substituted(rows,3,{c:b+1,p:q+r+1}),b*(q+r+1)*(b*r*(q+1)+q*(r+1))/2)
    ss={p:q+r+1,b:-q*(r+1)/(r*(q+1)),c:(r-q)/(r*(q+1))}
    eq('371115 C4',substituted(rows,4,ss),q*q*(r+1)**2*(q+r+1)*(q*q+q+r*r+r)/(6*r*r*(q+1)**2))
    print('PASS four direct coefficient branches',flush=True)

    rows=(3,13,14,15);COVERED.add(rows)
    T=q+r-1
    eq('3131415 C1',coefficient(rows,1),-(q-r)*(b-2*c+1))
    eq('3131415 C2',substituted(rows,2,{c:(b+1)/2}),-(b-1)*(q-r)*(T*(b-1)+2*p)/4)
    eq('3131415 C3',substituted(rows,3,{b:1-2*p/T,c:1-p/T}),p*p*(q-r)*((T+p*(p-1))**2-p*p*(p*p-1))/(2*T**3))

    rows=(7,7,11,13);COVERED.add(rows)
    eq('771113 C1',coefficient(rows,1),-p-q)
    eq('771113 C2',substituted(rows,2,{q:-p}),p*(b*(p+r)+c*(p-r)-p))
    ss={q:-p,c:(p-b*(p+r))/(p-r)}
    L=4*p*p*r+p*p-r*r;N=2*p*p*r+p*r-r*r;F=2*L*(b*b-b)+N
    eq('771113 C3',substituted(rows,3,ss),-p*p*F/(2*(p-r)**2))
    C4=substituted(rows,4,ss);num,den=S.fraction(C4)
    G=(3*p*p-1)*(p*p-r*r)+6*p*p*(p*p-1)*r
    eq('771113 C4 remainder',S.rem(num,F,b)/den,p*p*r*(2*b-1)*G/(6*(p-r)*L))
    eq('771113 L zero obstruction',L.subs(r,p/(1-2*p)),-4*p**4/(2*p-1)**2)
    Tn=9*n**6-9*n**4+3*n*n+1
    eq('771113 discriminant',S.discriminant(G,r),4*p*p*Tn.subs(n,p))
    me=3*n**3-3*n/2;mo=3*n**3-(3*n+1)/2
    eq('even lower square gap',Tn-me**2,3*n*n/4+1)
    eq('even upper square gap',(me+1)**2-Tn,6*n**3-3*n*n/4-3*n)
    eq('odd lower square gap',Tn-mo**2,3*n**3+3*n*n/4-3*n/2+S.Rational(3,4))
    eq('odd upper square gap',(mo+1)**2-Tn,3*(n-1)*(4*n*n+3*n+1)/4)
    print('PASS both integer square obstructions',flush=True)

    rows=(7,7,15,15);COVERED.add(rows)
    eq('771515 C3',coefficient(rows,3),-p*q*(b-c)*(p-q)*(b+c-1)/2)
    eq('771515 C4',substituted(rows,4,{c:1-b}),-b*p*q*(b-1)*(2*b-1)*(p-q)*(p+q-3*r-3)/6)
    J=p*p-p*q+q*q;K=(p+q)*(2*p-q)*(p-2*q);A=K-45*J+135
    eq('771515 C6',substituted(rows,6,{c:1-b,r:(p+q-3)/3}),-b*p*q*(b-1)*(2*b-1)*(p-q)*(A*b*(b-1)-2*K)/3240)
    eq('771515 positive h branch',(K-5*J+15).subs(q,2*p+h),(9*h-15)*p*(p+h)+(2*h-5)*h*h+15)
    H=-K.subs(q,2*p-h);JJ=J.subs(q,2*p-h)
    eq('771515 negative h branch',H-15*JJ+45,9*(h-5)*(p-h-1)*(p+1)+2*h*(h-6)*(h+3))
    eq('771515 q2p A',A.subs(q,2*p),135*(1-p*p))
    print('PASS last-orbit infinity coefficients and integer inequalities',flush=True)

    # At offsets (-1,1,-t,t), powers at positive t are abstract U,V,W;
    # their actual values t^p,t^q,t^r are restored in the analytic proof.
    U,V,W=S.symbols('U V W');powers=(1,U,V,W)
    targets={
      (0,0,0,1):4*W*(-U*q+V*p-p+q),
      (0,0,1,0):-4*W*((r-p)*U+p*t*V-r)/t,
      (0,1,0,0):4*W*(q*t*U+(r-q)*V-r)/t,
      (0,1,1,1):4*W*((r-p)*U+(q-r)*V+(p-q)*t)/t}
    for parity,target in targets.items():
        M=[];N=[]
        for i,a in enumerate((-1,1,-t,t)):
            rr=[];dd=[]
            for j,e in enumerate(ES):
                val=S.sympify(1 if i<2 else powers[j])
                if i%2==0:val*=(-1)**parity[j]
                if i<2 and j==3:val=0
                rr.append(val);dd.append(e*val/a)
            M.append(rr);N.append(dd)
        deriv=0
        for i in range(4):
            MM=S.Matrix(M);MM[i,:]=S.Matrix([N[i]]);deriv+=MM.det()
        eq(f'center derivative parity {parity}',deriv,target)
    print('PASS all four centered derivative formulas',flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--write',type=Path)
    args=parser.parse_args()
    counts,cert,orbits=coverage()
    check_coefficients()
    require(COVERED==orbits,'proof branches do not cover exactly the orbit list')
    if args.write:
        args.write.write_text(json.dumps(dict(counts=counts,classes=cert),indent=2)+'\n')
    print(f'PASS: {CHECKS} exact identities; all 23 support orbits covered.',flush=True)
