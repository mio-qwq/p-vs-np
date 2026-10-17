from pathlib import Path
"""Parity subgraphs with disjoint local upper-quota edge groups."""
from itertools import combinations
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'blossom'))
from blossom import maximum_matching,verify_matching

def quota_gadget(n,edges,groups,target):
    ports={};inc=[[] for _ in range(n)];E=[];N=0
    for i,(u,v) in enumerate(edges):
        if u==v:raise ValueError('loops unsupported')
        for vtx in (u,v):ports[i,vtx]=N;inc[vtx].append(N);N+=1
        E.append((ports[i,u],ports[i,v]))
    external=list(E);hosted=[[] for _ in range(n)];used=[set() for _ in range(n)]
    for v,ids,cap in groups:
        ids=list(ids)
        assert len(set(ids))==len(ids) and 0<=cap<=len(ids)
        assert not(set(ids)&used[v]);used[v].update(ids)
        assert all(v in edges[i] for i in ids)
        hosted[v].append((ids,cap))
    for v in range(n):
        clique=list(inc[v]);a=sum(len(ids)-cap for ids,cap in hosted[v])
        if (len(clique)+a)%2 != ((target>>v)&1):clique.append(N);N+=1
        for ids,cap in hosted[v]:
            for _ in range(len(ids)-cap):
                E.extend((N,ports[i,v]) for i in ids);N+=1
        E.extend(combinations(clique,2))
    return N,E,external

def valid_quota(edges,groups,target,mask):
    parity=0
    for i,(u,v) in enumerate(edges):
        if mask>>i&1:parity^=(1<<u)|(1<<v)
    return parity==target and all(sum((mask>>i)&1 for i in ids)<=cap for v,ids,cap in groups)

def solve_quota(n,edges,groups,target):
    N,E,external=quota_gadget(n,edges,groups,target)
    M=maximum_matching(N,E)
    assert verify_matching(N,E,M)
    if any(v<0 for v in M):return None
    mask=sum(1<<i for i,(u,v) in enumerate(external) if M[u]==v)
    assert valid_quota(edges,groups,target,mask)
    return mask
