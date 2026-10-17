from pathlib import Path
from itertools import permutations, combinations
from functools import lru_cache
import json

# Cayley distance is computed by BFS in the generating set, independently
# of the n - number of cycles formula used by the submitted proof.
def cayley(n):
    identity=tuple(range(n)); distance={identity:0}; queue=[identity]
    for p in queue:
        for i,j in combinations(range(n),2):
            q=list(p); q[i],q[j]=q[j],q[i]; q=tuple(q)
            if q not in distance: distance[q]=distance[p]+1; queue.append(q)
    return distance

def pf_value(p, subset):
    # Enumerate signed perfect matchings via exterior-algebra recursion.
    @lru_cache(None)
    def rec(s):
        if not s:return 1
        a=s[0]; result=0
        for k in range(1,len(s)):
            b=s[k]; entry=int(p[a]==b)-int(p[b]==a)
            if entry: result+=(-1)**(k+1)*entry*rec(s[1:k]+s[k+1:])
        return result
    return rec(tuple(subset))

def rank_insert(v,basis,field):
    if field==2:
        while v:
            pivot=v.bit_length()-1
            if pivot in basis:v^=basis[pivot]
            else:basis[pivot]=v;return
    else:
        v=v[:]
        for pivot in sorted(basis):
            if v[pivot]:
                t=v[pivot]; b=basis[pivot]
                for k in range(pivot,len(v)):v[k]=(v[k]-t*b[k])%field
        for pivot,x in enumerate(v):
            if x:
                inv=pow(x,-1,field);basis[pivot]=[(y*inv)%field for y in v];return

def direct_radius(n,d,field,dist):
    # On permutation matrices all monomials reduce either to zero or to
    # indicators of partial injective maps, of size at most d.
    monomials=[tuple(zip(rows,cols)) for k in range(min(n,d)+1)
               for rows in combinations(range(n),k)
               for cols in permutations(range(n),k)]
    vectors=[]
    for p in sorted(dist,key=dist.get):
        v=[int(all(p[i]==j for i,j in m)) for m in monomials]
        if field==2:v=sum(x<<i for i,x in enumerate(v))
        vectors.append((dist[p],v))
    basis={}; ranks=[]
    for r in range(max(dist.values())+1):
        for distance,v in vectors:
            if distance==r:rank_insert(v,basis,field)
        ranks.append(len(basis))
    radius=next(r for r,x in enumerate(ranks) if x==ranks[-1])
    expected=0 if d==0 or n<=1 else min(n-1,2*d)
    assert radius==expected,(n,d,field,ranks,expected)
    return {'n':n,'d':d,'field':field,'ranks_by_radius':ranks,'radius':radius,'monomials':len(monomials)}

out={'witness_checks':[],'direct_universal_radius_checks':[]}
for n in range(0,9):
    dist=cayley(n);count=0;general_checks=0
    if n>=2:
        for p,ell in dist.items():
            if n==2:q=int(p[0]==1)
            elif n%2:q=pf_value(p,range(n-1))
            else:q=(int(p[0]==1)-int(p[1]==0))*pf_value(p,range(2,n))
            assert q in (-1,0,1)
            if q:
                count+=1;assert ell==n-1,(n,p,ell,q)
            # Every degree regime for which the 2d lower construction applies.
            for d in range(1,(n-1)//2+1):
                val=pf_value(p,range(2*d)); general_checks+=1
                if val:assert ell>=2*d,(n,d,p,val,ell)
        assert count>0
    out['witness_checks'].append({'n':n,'permutations':len(dist),'nonzero_extremal':count,'general_minor_checks':general_checks})
    if n<=5:
        for d in range(n+1):
            out['direct_universal_radius_checks'].append(direct_radius(n,d,2,dist))
            if n<=4 or d<=2:
                out['direct_universal_radius_checks'].append(direct_radius(n,d,3,dist))
    print('n',n,'done',flush=True)
with open(Path(__file__).with_name('results.json'),'w') as f:json.dump(out,f,indent=2)
print('ALL PASS')
