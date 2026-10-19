#!/usr/bin/env python3
"""Exact q=3 collision certificate. Standard-library arithmetic only.

Actual coefficients come from finite translated-minor Cauchy--Binet sums,
independently of the omitted-node / Schur prediction.
"""
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
from math import comb, factorial, prod
from pathlib import Path
import json


def require(test, message):
    if not test:
        raise RuntimeError(message)


def det(matrix):
    a = [list(row) for row in matrix]
    n = len(a)
    if n == 0:
        return 1
    sign, previous = 1, 1
    for k in range(n - 1):
        pivot = next((i for i in range(k, n) if a[i][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            sign = -sign
        value = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                num = a[i][j] * value - a[i][k] * a[k][j]
                require(num % previous == 0, 'Bareiss division is inexact')
                a[i][j] = num // previous
            a[i][k] = 0
        previous = value
    return sign * a[-1][-1]


def partitions(total, length, maximum=None):
    if length == 0:
        if total == 0:
            yield ()
        return
    if maximum is None:
        maximum = total
    for first in range(min(total, maximum), -1, -1):
        for tail in partitions(total - first, length - 1, first):
            yield (first,) + tail


@lru_cache(None)
def coefficient(offsets, exponents, loss):
    b = len(offsets)
    return sum(det([[a**d for d in degrees] for a in offsets])
               * det([[comb(e,d) for e in exponents] for d in degrees])
               for lam in partitions(loss,b)
               for degrees in [tuple(i+lam[b-1-i] for i in range(b))])


def layer_coefficient(offsets, exponents, I, J, s, loss):
    n = len(offsets)
    total = 0
    for rows in combinations(I,s):
        rc = tuple(i for i in range(n) if i not in rows)
        for cols in combinations(J,s):
            cc = tuple(j for j in range(n) if j not in cols)
            a, ac = tuple(offsets[i] for i in rows), tuple(offsets[i] for i in rc)
            e, ec = tuple(exponents[j] for j in cols), tuple(exponents[j] for j in cc)
            total += (-1)**(sum(rows)+sum(cols))*sum(
                coefficient(a,e,u)*coefficient(ac,ec,loss-u) for u in range(loss+1))
    return total


def root_poly(roots):
    p = [1]
    for x in roots:
        out = [0]*(len(p)+1)
        for i,c in enumerate(p):
            out[i] -= x*c
            out[i+1] += c
        p = out
    return p


def vandermonde(xs):
    return prod(xs[j]-xs[i] for j in range(len(xs)) for i in range(j))


def complete(xs,k):
    if k < 0:
        return 0
    h = [1]+[0]*k
    for x in xs:
        for d in range(1,k+1):
            h[d] += x*h[d-1]
    return h[k]


def schur(xs,lam):
    lam = tuple(v for v in lam if v)
    return det([[complete(xs,lam[i]-i+j) for j in range(len(lam))]
                for i in range(len(lam))])


def transpose(lam):
    return tuple(sum(x > j for x in lam) for j in range(max(lam,default=0)))


def H(b):
    return prod(factorial(i) for i in range(b))


def T(xs,lam):
    b = len(xs)
    lam = tuple(lam)+(0,)*(b-len(lam))
    return Fraction(H(b)*schur(xs,lam),prod(factorial(lam[i]+b-i-1) for i in range(b)))


def rectangular_row_factor(a,ac,width,height):
    return sum((-1)**sum(eta)*T(a,transpose(eta))
               *T(ac,tuple(width-x for x in reversed(eta)))
               for degree in range(width*height+1)
               for eta in partitions(degree,height,width))


def main():
    X = (0,5,6,16,17,22)
    Y = (1,2,10,12,20,21)
    e = tuple(sorted(X+Y))
    a = tuple(range(12))
    I = (0,1,2)
    J = tuple(j for j,x in enumerate(e) if x in X)
    f,g = root_poly(X),root_poly(Y)
    diff = [v-u for u,v in zip(f,g)]
    require(diff[1:] == [0]*6 and diff[0] != 0,'Constant-remainder identity failed')
    R = diff[0]
    rho = {x:Fraction(R,prod(x-y for y in X if y!=x)) for x in X}
    def E(k,lam):
        return sum(vandermonde(Z)**2*prod(rho[x] for x in Z)*schur(Z,lam)
                   for Z in combinations(X,k))
    # Every first-level Schur value is independently a sum over root subsets.
    functional = []
    for k in (1,2,3,4,5,6):
        loss = k*(6-k)
        shape = (6-k,)*k
        gamma = (-1)**comb(k,2)*R**k
        for d in range(loss+1):
            for lam in partitions(d,k):
                actual = E(k,lam)
                expected = gamma if lam==shape else 0
                require(actual==expected, 'Exterior Schur certificate failed')
        functional.append({'omitted_nodes':k,'kappa':loss,'shape':shape,'gamma':str(gamma)})
    B = rectangular_row_factor(a[:3],a[3:],3,3)
    A = Fraction((-1)**sum(I)*vandermonde(a[:3])*vandermonde(a[3:]),H(3)*H(9))
    K = (-1)**sum(J)*vandermonde(X)*vandermonde(Y)
    gamma = -R**3
    sign = (-1)**(3*(12-3))
    candidate = sign*A*K*gamma*B
    require(B>0,'Separated-offset row factor is not positive')
    vals=[]
    for loss in range(10):
        value=layer_coefficient(a,e,I,J,3,loss)
        vals.append(value)
        require(value==(candidate if loss==9 else 0),'Translated-minor coefficient disagrees')
        print('maximal-layer loss',loss,'coefficient',value,flush=True)
    # The size-2 layer raw gap is 7; own losses 0,1,2 would sit above or at loss 9.
    smaller=[layer_coefficient(a,e,I,J,2,l) for l in range(9)]
    require(smaller[:8]==[0]*8 and smaller[8]!=0,'Competing smaller-layer cancellation failed')
    # All other layers are excluded already by their raw gaps 16 and 27.
    D=sum(e)-comb(3,2)-comb(9,2)
    # Exact omitted-column original-index signs, for every maximal/lower-layer subset.
    weight_checks=0
    for k in range(3,7):
        for Zind in combinations(J,k):
            selected=tuple(j for j in J if j not in Zind)
            rest=tuple(j for j in range(12) if j not in selected)
            Z=tuple(e[j] for j in Zind)
            actual=Fraction((-1)**sum(selected)*vandermonde(tuple(e[j] for j in selected))
                            *vandermonde(tuple(e[j] for j in rest)),K)
            expected=(-1)**(k*(12-k))*vandermonde(Z)**2*prod(rho[x] for x in Z)
            require(actual==expected,'Original-index weight sign failed')
            weight_checks+=1
    # Coefficient sign and invariance checks for the explicit row factor.
    shifted=rectangular_row_factor(tuple(x+7 for x in a[:3]),tuple(x+7 for x in a[3:]),3,3)
    reversed_factor=rectangular_row_factor(tuple(-x for x in a[:3]),tuple(-x for x in a[3:]),3,3)
    require(shifted==B and reversed_factor==-B,'Row-factor translation/reversal failed')
    result={'status':'passed','method':'exact translated-minor Cauchy--Binet sums, independently compared with exterior/Schur formula',
            'n':12,'r':3,'q':3,'offsets':a,'exponents':e,'I':I,'J':J,'X':X,'Y':Y,
            'f_low_to_high':f,'g_low_to_high':g,'R':R,'D':D,'kappa':9,'shape':[3,3,3],
            'A':str(A),'K':str(K),'gamma':str(gamma),'omitted_weight_sign':sign,'row_factor':str(B),
            'leading_degree':D-9,'leading_coefficient':str(candidate),
            'maximal_layer_coefficients':[str(v) for v in vals],
            'next_smaller_layer':{'size':2,'raw_gap':7,'own_losses':list(range(9)),
                                  'global_losses':list(range(7,16)),'coefficients':[str(v) for v in smaller],
                                  'first_exterior_loss':8,'first_possible_global_loss':15},
            'other_raw_gaps':{'size1':16,'size0':27},'exterior_certificates':functional,
            'original_index_weight_checks':weight_checks,
            'shifted_row_factor':str(shifted),'reverse_separation_row_factor':str(reversed_factor)}
    # The same sextic identity supplies exact q=1 and q=2 reductions.
    regressions=[]
    for q in (1,2):
        r=6-q
        rows=tuple(range(r))
        kappa=q*r
        rowfactor=rectangular_row_factor(a[:r],a[r:],r,q)
        prefactor=Fraction((-1)**sum(rows)*vandermonde(a[:r])*vandermonde(a[r:]),H(r)*H(12-r))
        egamma=(-1)**comb(q,2)*R**q
        expected=(-1)**(q*(12-q))*prefactor*K*egamma*rowfactor
        actual=[layer_coefficient(a,e,rows,J,r,l) for l in range(kappa+1)]
        require(actual==[0]*kappa+[expected],'q=1 or q=2 translated-minor regression failed')
        gap=12-2*r+1
        lower=[layer_coefficient(a,e,rows,J,r-1,l) for l in range(kappa-gap+1)]
        require(lower==[0]*len(lower),'q=1 or q=2 smaller-layer regression failed')
        degree=sum(e)-comb(r,2)-comb(12-r,2)
        regressions.append({'q':q,'r':r,'I':rows,'kappa':kappa,'shape':[r]*q,
                            'row_factor':str(rowfactor),'D':degree,'leading_degree':degree-kappa,
                            'maximal_layer_coefficients':[str(v) for v in actual],
                            'leading_coefficient':str(expected),'smaller_raw_gap':gap,
                            'smaller_own_losses':list(range(len(lower))),
                            'smaller_coefficients':[str(v) for v in lower]})
        print('q='+str(q),'reduction passed; B =',rowfactor,'; leading coefficient =',expected,flush=True)
    result['one_and_two_omission_regressions']=regressions
    # A nonconstant remainder gives a shorter-height q=3 first shape.
    en=(0,25,48,123,146,266,386,409,484,507,532)
    Jold=(1,2,5,8,9)
    Jn=tuple(j for j in range(11) if j not in Jold)
    Xn=tuple(en[j] for j in Jn)
    Yn=tuple(en[j] for j in Jold)
    fn,gn=root_poly(Xn),root_poly(Yn)
    Cn=20835207993600
    product=[0]*(len(gn)+1)
    for i,c in enumerate(gn):
        product[i]-=266*c
        product[i+1]+=c
    require([u-v for u,v in zip(product,fn)]==[Cn]+[0]*6,'Nonconstant-remainder identity failed')
    an=tuple(range(11)); In=(0,1,2)
    rhon={x:Fraction(prod(x-y for y in Yn),prod(x-y for y in Xn if y!=x)) for x in Xn}
    for d in range(7):
        for lam in partitions(d,3):
            value=sum(vandermonde(Z)**2*prod(rhon[x] for x in Z)*schur(Z,lam) for Z in combinations(Xn,3))
            require(value==(-Cn**2 if lam==(3,3,0) else 0),'Short-height exterior shape failed')
    Bn=rectangular_row_factor(an[:3],an[3:],3,2)
    Kn=(-1)**sum(Jn)*vandermonde(Xn)*vandermonde(Yn)
    An=Fraction((-1)**sum(In)*vandermonde(an[:3])*vandermonde(an[3:]),H(3)*H(8))
    expected=An*Kn*(-Cn**2)*Bn  # epsilon=(-1)^(3*(11-3))=+1.
    actual=[layer_coefficient(an,en,In,Jn,3,l) for l in range(7)]
    require(actual==[0]*6+[expected],'Short-height translated-minor check failed')
    lower=layer_coefficient(an,en,In,Jn,2,0)
    require(lower==0,'Short-height lower-layer collision did not cancel')
    result['short_height_q3_regression']={'n':11,'r':3,'q':3,'offsets':an,'exponents':en,'I':In,'J':Jn,
        'R_low_to_high':gn,'S':Cn,'degree_echelon_set':[0,1,5],'pivot_columns':[0,4,5],
        'shape':[3,3],'kappa':6,'row_factor':str(Bn),'gamma':str(-Cn**2),'omitted_weight_sign':1,
        'D':2895,'leading_degree':2889,'leading_coefficient':str(expected),
        'maximal_layer_coefficients':[str(v) for v in actual],
        'smaller_raw_gap':6,'smaller_own_loss_0_coefficient':str(lower)}
    print('q=3 short-height regression passed; B =',Bn,'; leading coefficient =',expected,flush=True)
    Path(__file__).with_name('q3_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print('All q=3 checks passed. B =',B,'; D =',D,'; leading coefficient =',candidate,flush=True)

if __name__=='__main__':
    main()
