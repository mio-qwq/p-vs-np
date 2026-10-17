from pathlib import Path
"""Verified common-star graph certificates for disjoint quota groups."""
import itertools,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'pair'))
from certificate_solver import rank,equal_kernels,linear_solution
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'quota'))
from quota import solve_quota

def extension(A,groups):
    seen=set();extra=[];reps=[]
    if any(not a for a in A):raise ValueError('preprocess zero columns first')
    for ids,cap in groups:
        if len(set(ids))!=len(ids) or not 0<=cap<=len(ids):raise ValueError('invalid group')
        if seen&set(ids):raise ValueError('solver requires globally disjoint groups')
        seen.update(ids)
        bycol={}
        for i in ids:bycol.setdefault(A[i],i)
        unique=list(bycol)
        if rank(unique)!=len(unique):return None
        representatives=list(bycol.values());reps.append(representatives)
        extra.extend(A[i]^A[j] for i,j in itertools.combinations(representatives,2))
    return A+extra,reps

def solve_star_certificate(A,groups,target,n,extedges):
    data=extension(A,groups)
    if data is None:raise ValueError('group direction dependence prevents a common star')
    ext,reps=data
    if len(extedges)!=len(ext):raise ValueError('wrong certificate edge count')
    if any(u==v or min(u,v)<0 or max(u,v)>=n for u,v in extedges):raise ValueError('invalid graph endpoint')
    B=[(1<<u)|(1<<v) for u,v in extedges]
    if not equal_kernels(ext,B):raise ValueError('invalid graphic certificate kernel')
    original=extedges[:len(A)];hosted=[]
    for ids,cap in groups:
        if not ids:continue
        common=set(original[ids[0]])
        for i in ids:common&=set(original[i])
        if not common:raise AssertionError('independent pairwise incident group failed common-star lemma')
        hosted.append((min(common),ids,cap))
    z=linear_solution(A,target)
    if z is None:return None
    targetB=0
    for i,b in enumerate(B[:len(A)]):
        if z>>i&1:targetB^=b
    mask=solve_quota(n,original,hosted,targetB)
    if mask is not None:
        syndrome=0
        for i,a in enumerate(A):
            if mask>>i&1:syndrome^=a
        assert syndrome==target
        assert all(sum((mask>>i)&1 for i in ids)<=cap for ids,cap in groups)
    return mask
