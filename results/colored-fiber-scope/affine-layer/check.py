#!/usr/bin/env python3
"""Exact, standard-library-only check of a bounded affine/binary-layer separation.

No assertions are used, so python -O runs every check. No network or solver.
"""
import argparse
from collections import Counter
from fractions import Fraction
from itertools import permutations
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent

def require(condition, message):
    if not condition:
        raise ValueError(message)

def rank(rows):
    A = [[Fraction(x) for x in row] for row in rows]
    k = 0
    for j in range(len(A[0]) if A else 0):
        pivot = next((i for i in range(k, len(A)) if A[i][j]), None)
        if pivot is None:
            continue
        A[k], A[pivot] = A[pivot], A[k]
        z = A[k][j]
        A[k] = [x / z for x in A[k]]
        for i in range(len(A)):
            if i != k and A[i][j]:
                z = A[i][j]
                A[i] = [a - z*b for a,b in zip(A[i], A[k])]
        k += 1
    return k

def coeff_vector(p):
    return [int(p[i] == j) for i in range(3) for j in range(3)]

def dot(a,b):
    return sum(x*y for x,y in zip(a,b))

def score(w,p):
    return sum(w[4*i+p[i]] for i in range(4))

def fiber(w,t,P):
    return {p for p in P if score(w,p)==t}

def polynomial(p):
    inv = sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))
    c = [(-1)**inv]
    for i,j in enumerate(p):
        for _ in range(j):
            d=[0]*(len(c)+1)
            for k,v in enumerate(c):
                d[k] += i*v
                d[k+1] += v
            c=d
    return c

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--certificate', type=Path, default=ROOT/'certificate.json')
    args=ap.parse_args()
    data=json.loads(args.certificate.read_text())
    W=data['costs'];t=data['target'];S={tuple(p) for p in data['permutations']}
    P=list(permutations(range(4)))
    require(len(W)==16 and len(S)==7,'Malformed certificate')
    require(fiber(W,t,P)==S,'Integer matrix fails to realize the stated exact layer')
    require({(i,p[i]) for p in S for i in range(4)}==set((i,j) for i in range(4) for j in range(4)), 'Union is not full support')

    # Verify the complete normal form symbolically by its three coefficient vectors.
    # Q=[[b,b-a,b,0],[a+b-c,2b-c,b,0],[a,b,c,0],[0,0,0,0]].
    N=[(0,1,0),(-1,1,0),(0,1,0),(1,1,-1),(0,2,-1),(0,1,0),(1,0,0),(0,1,0),(0,0,1)]
    s0=min(S)
    base=coeff_vector(s0)
    equations=[[x-y for x,y in zip(coeff_vector(p),base)] for p in S if p!=s0]
    require(rank(equations)==6,'Constancy constraints must have rank six')
    for col in range(3):
        v=[q[col] for q in N]
        require(all(dot(eq,v)==0 for eq in equations),'Normal form fails constancy')
    require(rank([[q[col] for q in N] for col in range(3)])==3,'Normal form must have three independent parameters')
    norm_score=lambda p:tuple(sum(N[3*i+p[i]][c] for i in range(3) if p[i]<3) for c in range(3))
    require({norm_score(p) for p in S}=={(0,2,0)},'Common score must be 2b')
    # Each equality between the four normalized row-2 entries forces an outsider.
    witnesses={
        (1,2,3,0):(-1,0,0),  # a=0
        (0,1,2,3):(0,1,0),   # b=0
        (1,0,3,2):(0,0,-1),  # c=0
        (2,3,0,1):(1,-1,0),  # a=b
        (2,0,3,1):(1,0,-1),  # a=c
        (0,1,3,2):(0,1,-1),  # b=c
    }
    for p,v in witnesses.items():
        require(p not in S,'Leak witness lies in S')
        require(tuple(x-y for x,y in zip(norm_score(p),(0,2,0)))==v,'Incorrect leak identity')

    # Fully independent binary check: explicit entry lists and integer sums.
    counts=Counter();constant=0;min_leaks=24;layers=set()
    for mask in range(1<<16):
        w=[(mask>>j)&1 for j in range(16)]
        levels={score(w,p) for p in S}
        if len(levels)!=1:
            continue
        constant+=1
        level=next(iter(levels))
        F=fiber(w,level,P)
        require(F!=S,'COUNTEREXAMPLE: a binary matrix realizes the family')
        require(any(score(w,p)==level for p in witnesses),'Six-witness certificate fails')
        d=[w[8+j]-w[12+j] for j in range(4)]
        require(len(set(d))<4,'Binary row-difference pigeonhole failed')
        counts[len(F)]+=1;min_leaks=min(min_leaks,len(F-S))
        layers.add(tuple(sorted(F)))
    expected={8:4,10:12,11:6,12:12,13:10,14:60,16:40,24:30}
    require(dict(counts)==expected,'Binary histogram differs')
    require(constant==174 and len(layers)==14,'Binary totals differ')

    # Positive controls detect an indiscriminate impossible-fiber checker.
    require(fiber([0]*16,0,P)==set(P),'Full-family binary positive control failed')
    require(fiber(W,t,P)==S,'Integer positive control failed')
    c=[sum(polynomial(p)[i] for p in S) for i in range(7)]
    require(c==[42,86,130,129,64,14,1],'Polynomial coefficient vector differs')
    require(c[-1]==1,'Nonvanishing leading coefficient failed')
    result={'status':'PASS','optimization':sys.flags.optimize,
        'n':4,'family_size':len(S),'union_edges':16,'integer_weights':W,'target':t,
        'normal_form_rank':6,'normal_form_parameters':3,'six_leak_identities_verified':True,
        'binary_matrices_checked':65536,'binary_matrices_constant_on_family':constant,
        'distinct_binary_layers_containing_family':len(layers),'minimum_additional_matchings':min_leaks,
        'layer_size_histogram':dict(sorted(counts.items())),
        'polynomial_coefficients_low_to_high':c,'positive_controls':'PASS'}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
