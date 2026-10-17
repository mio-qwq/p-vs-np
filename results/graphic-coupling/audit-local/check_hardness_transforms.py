from itertools import combinations,product
from random import Random

def affine_solutions(n,edges,b):
    rows=[sum(1<<i for i,e in enumerate(edges) if v in e) for v in range(n)]
    piv={}
    for row,rhs in zip(rows,b):
        while row:
            p=row.bit_length()-1
            if p in piv:row^=piv[p][0];rhs^=piv[p][1]
            else:piv[p]=(row,rhs);break
        if not row and rhs:return []
    def finish(x,inhom):
        for p,(row,rhs) in sorted(piv.items()):
            if ((row&x).bit_count()%2)^(rhs if inhom else 0):x^=1<<p
        return x
    x0=finish(0,True);basis=[finish(1<<f,False) for f in range(len(edges)) if f not in piv]
    S=[x0]
    for v in basis:S += [x^v for x in S]
    return S

def solutions(n,E,P,b):return {x for x in affine_solutions(n,E,b) if not any((x>>e&1) and (x>>f&1) for e,f in P)}
def distance2(n,E,P,b):
    M=len(E);newE=[];mid=[];marked=[];halves=[];newb=list(b)
    for e,(v,w) in enumerate(E):
        u=len(newb);newb.append(0);mid.append(u)
        a=len(newE);newE.extend(((v,u),(u,w)));halves.append((a,a+1));marked.append(a)
    newP=[];guards=[]
    for e,f in P:
        newP.append((marked[e],marked[f]));ue,uf=mid[e],mid[f]
        c=len(newE);newE.append((ue,uf));leaf=len(newb);newb.append(1)
        d=len(newE);newE.append((ue,leaf));newb[ue]^=1
        newP.append((c,d));guards.append((c,d))
    return len(newb),newE,newP,newb,halves,guards

def line_dist(E,e,f):
    if e==f:return 0
    seen={e};todo=[e];d=0
    while todo:
        nxt=[];d+=1
        for x in todo:
            for y in range(len(E)):
                if y not in seen and set(E[x])&set(E[y]):
                    if y==f:return d
                    seen.add(y);nxt.append(y)
        todo=nxt
    return None
rng=Random(22417)
for trial in range(1200):
    n=rng.randrange(1,7);E=[e for e in combinations(range(n),2) if rng.random()<.4]
    if len(E)>9:E=E[:9]
    order=list(range(len(E)));rng.shuffle(order);P=[tuple(order[i:i+2]) for i in range(0,len(order)-1,2) if rng.random()<.7]
    b=[rng.randrange(2) for _ in range(n)];S=solutions(n,E,P,b)
    nn,EE,PP,bb,H,G=distance2(n,E,P,b);T=solutions(nn,EE,PP,bb)
    assert len(set(tuple(sorted(e)) for e in EE))==len(EE)
    assert len({e for pair in PP for e in pair})==2*len(PP)
    assert all(line_dist(EE,e,f)<=2 for e,f in PP)
    expected=set()
    for x in S:
        y=sum(((x>>e)&1)*((1<<a)|(1<<c)) for e,(a,c) in enumerate(H))
        y|=sum(1<<d for c,d in G);expected.add(y)
    assert expected==T
print('1200 distance2 transformations: exact solution bijection, simplicity, disjoint pairs, pair distances PASS')

def coloring_transform(n,E):
    # center 0, outer vertices1..n; new intermediates follow.
    EE=[];b=[n%2]+[1]*n;marked={}
    for v in range(n):
        for j in range(3):
            u=len(b);b.append(0);marked[v,j]=len(EE);EE.extend(((0,u),(u,v+1)))
    P=[]
    for v in range(n):P.extend((marked[v,j],marked[v,k]) for j,k in combinations(range(3),2))
    for v,w in E:P.extend((marked[v,j],marked[w,j]) for j in range(3))
    return len(b),EE,P,b,marked
for n in range(0,5):
 possible=list(combinations(range(n),2))
 for mask in range(1<<len(possible)):
    E=[e for i,e in enumerate(possible) if mask>>i&1]
    expected={c for c in product(range(3),repeat=n) if all(c[v]!=c[w] for v,w in E)}
    nn,EE,P,b,marked=coloring_transform(n,E);T=solutions(nn,EE,P,b)
    observed=set()
    for x in T:
        c=tuple(next(j for j in range(3) if x>>marked[v,j]&1) for v in range(n))
        assert all(sum(x>>marked[v,j]&1 for j in range(3))==1 for v in range(n))
        observed.add(c)
    assert observed==expected and len(T)==len(expected)
    assert all(0 in EE[e] and 0 in EE[f] for e,f in P)
print('all simple graphs n<=4: exact3coloring/local-overlap solution bijection PASS')
