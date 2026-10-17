from functools import lru_cache
from itertools import combinations

def gadget(n,edges,pairs,target):
    """Polynomial reduction for pairs sharing a vertex. Return matching graph."""
    inc=[[] for _ in range(n)];ports={};newedges=[];count=0
    for i,(u,v) in enumerate(edges):
        assert u!=v
        for endpoint in (u,v):
            ports[(i,endpoint)]=count;inc[endpoint].append(count);count+=1
        newedges.append((ports[i,u],ports[i,v]))
    external=list(newedges);hosted=[[] for _ in range(n)];seen=set()
    for i,j in pairs:
        assert i!=j and i not in seen and j not in seen;seen|={i,j}
        common=set(edges[i])&set(edges[j]);assert common
        v=min(common);hosted[v].append((ports[i,v],ports[j,v]))
    for v in range(n):
        clique=list(inc[v]);p=len(hosted[v]);d=len(clique)
        if ((d+p)&1)!=((target>>v)&1):clique.append(count);count+=1
        for a,b in hosted[v]:newedges.extend([(count,a),(count,b)]);count+=1
        newedges.extend(combinations(clique,2))
    return count,newedges,external

def brute_pm(n,edges):
    """Exponential independent validation oracle, NOT polynomial solver."""
    if n%2:return None
    adj=[0]*n
    for u,v in edges:adj[u]|=1<<v;adj[v]|=1<<u
    @lru_cache(None)
    def rec(mask):
        if not mask:return ()
        u=min((i for i in range(n) if mask>>i&1),key=lambda i:(adj[i]&mask).bit_count())
        choices=adj[u]&mask
        while choices:
            bit=choices&-choices;choices-=bit;v=bit.bit_length()-1
            ans=rec(mask^(1<<u)^bit)
            if ans is not None:return ((u,v),)+ans
        return None
    return rec((1<<n)-1)

def valid(edges,pairs,target,mask):
    parity=0
    for i,(u,v) in enumerate(edges):
        if mask>>i&1:parity^=(1<<u)|(1<<v)
    return parity==target and all(not(mask>>i&1 and mask>>j&1) for i,j in pairs)

def brute_join(edges,pairs,target):
    return next((m for m in range(1<<len(edges)) if valid(edges,pairs,target,m)),None)

def reduce_sat(n,clauses,pad_all=False):
    """SAT to arbitrary disjoint forbidden-edge-pair T-join."""
    edges=[];pairs=[];nextv=n+len(clauses)+1;false_edges={};branch_options=[]
    def branch(start,end,labels):
        nonlocal nextv
        length=max(2,len(labels));vs=[start]+list(range(nextv,nextv+length-1))+[end];nextv+=length-1
        ids=[]
        for a,b in zip(vs,vs[1:]):ids.append(len(edges));edges.append((a,b))
        return ids
    for var in range(n):
        opts=[]
        for value in range(2):
            labels=[(ci,li) for ci,c in enumerate(clauses) for li,l in enumerate(c) if abs(l)==var+1 and (l>0)!=bool(value)]
            ids=branch(var,var+1,labels)
            false_edges.update(zip(labels,ids));opts.append(ids)
        branch_options.append(opts)
    for ci,c in enumerate(clauses):
        opts=[]
        for li,l in enumerate(c):
            ids=branch(n+ci,n+ci+1,[(ci,li)]);pairs.append((false_edges[ci,li],ids[0]));opts.append(ids)
        branch_options.append(opts)
    if pad_all:
        used={e for pair in pairs for e in pair}
        for i in range(len(edges)):
            if i not in used:
                pairs.append((i,len(edges)));edges.append((0,nextv));nextv+=1
    target=1|(1<<(n+len(clauses)))
    return nextv,edges,pairs,target,branch_options
