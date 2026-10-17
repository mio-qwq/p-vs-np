from pathlib import Path
import itertools as it, random, math, json, sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from general_solver import solve as root_solve
R=random.Random(17102026)
counts=dict(instances=0,targets=0,color_runs=0,indicator_checks=0,port_cycles=0)
def edge(u,v): return tuple(sorted((u,v)))
def matchings(vs):
 if not vs: yield (); return
 a=vs[0]
 for b in vs[1:]:
  yield from ((edge(a,b),)+m for m in matchings(tuple(v for v in vs[1:] if v!=b)))
def xor(vals):
 x=0
 for v in vals:x^=v
 return x
def family(n,t):
 if t<=1: yield (0,)*n;return
 L=(n-1).bit_length();r=min(L,t-1)
 for bits in it.combinations(range(L),r):
  codes=[sum(((i>>b)&1)<<j for j,b in enumerate(bits)) for i in range(n)]
  for S in it.combinations(range(1<<r),t):
   col={c:i for i,c in enumerate(S)}
   yield tuple(col.get(c,0) for c in codes)
def one(n,k,labels,allowed,target,h,mandatory):
 counts['color_runs']+=1
 B={h[i] for i in mandatory}
 if len(B)!=len(mandatory): return None
 avail=[i for i in range(n) if h[i] not in B or i in mandatory]
 baseline=[edge(2*i,2*i+1) for i in range(n)]
 D=target^xor(labels[e] for e in baseline)
 cycles={}
 # Fixed start pair and start entry port retained by separate DP runs.
 for s in avail:
  for a in (0,1):
   states={(1<<h[s],s,a,0):()}
   for size in range(1,n+1):
    for (mask,last,b,z),path in list(states.items()):
     if mask.bit_count()!=size:continue
     out=2*last+1-b
     if size>=2:
      e=edge(out,2*s+a)
      if e in allowed:
       nz=z^labels[e]^labels[baseline[last]]
       cycles.setdefault((mask,nz),path+(e,))
     for j in avail:
      if mask>>h[j]&1:continue
      for c in (0,1):
       e=edge(out,2*j+c)
       if e in allowed:
        key=(mask|1<<h[j],j,c,z^labels[e]^labels[baseline[last]])
        states.setdefault(key,path+(e,))
 packed={(0,0):()}
 for size in range(n+1):
  for (mask,z),es in list(packed.items()):
   if mask.bit_count()!=size:continue
   if z==D and all(mask>>c&1 for c in B):
    touched={v//2 for e in es for v in e}
    result=es+tuple(baseline[i] for i in range(n) if i not in touched)
    assert len(result)==n and sorted(v for e in result for v in e)==list(range(2*n))
    assert all(e in allowed for e in result) and xor(labels[e] for e in result)==target
    return result
   for (cm,cz),ce in cycles.items():
    if not mask&cm:packed.setdefault((mask|cm,z^cz),es+ce)
 return None
def solve(n,k,labels,allowed,target,cover):
 assert all(u in cover or v in cover for (u,v) in labels if (u,v) not in allowed)
 mandatory={i for i in range(n) if (2*i,2*i+1) not in allowed}
 t=min(n,4*(k+len(cover))+1)
 for h in family(n,t):
  ans=one(n,k,labels,allowed,target,h,mandatory)
  if ans is not None:return ans
 return None
def check(n,k,labels,allowed,cover,indicators=False):
 counts['instances']+=1
 ms=list(matchings(tuple(range(2*n))))
 valid={z:[] for z in range(1<<k)}
 for m in ms:
  if all(e in allowed for e in m):valid[xor(labels[e] for e in m)].append(m)
 for target in valid:
  counts['targets']+=1
  ans=solve(n,k,labels,allowed,target,cover)
  assert (ans is not None)==bool(valid[target]),(n,k,labels,allowed,target)
  lm=[[0]*(2*n) for _ in range(2*n)];am=[[False]*(2*n) for _ in range(2*n)]
  for (u,v),z in labels.items():lm[u][v]=lm[v][u]=z;am[u][v]=am[v][u]=(u,v) in allowed
  ra=root_solve(lm,k,target,am,cover)
  assert (ra is not None)==bool(valid[target])
  if ra is not None:
   ra=tuple(edge(*e) for e in ra)
   assert sorted(v for e in ra for v in e)==list(range(2*n))
   assert all(e in allowed for e in ra) and xor(labels[e] for e in ra)==target
  if valid[target]:
   t=min(n,4*(k+len(cover))+1)
   assert any(sum((2*i,2*i+1) not in m for i in range(n))<=t for m in valid[target])
 if indicators:
  for p in it.permutations(range(2*n)):
   E={e:sum((p[2*i],p[2*i+1]) in (e,e[::-1]) for i in range(n))%2 for e in labels}
   assert sum(E.values())==n
   for target in valid:
    f=1
    for j in range(k):f*=1^((xor(labels[e] for e in labels if E[e])^target)>>j&1)
    for v in cover:f*=sum(E[e] for e in allowed if v in e)%2
    expected=all(e in allowed for e in E if E[e]) and xor(labels[e] for e in E if E[e])==target
    assert bool(f)==expected;counts['indicator_checks']+=1
# Exhaust all ternary edge assignments on four vertices: forbidden, allowed 0, allowed 1.
es=list(it.combinations(range(4),2))
for vals in it.product(range(3),repeat=6):
 labels={e:int(v==2) for e,v in zip(es,vals)};allowed={e for e,v in zip(es,vals) if v}
 forbidden=set(es)-allowed
 cover=next(set(C) for q in range(5) for C in it.combinations(range(4),q) if all(set(e)&set(C) for e in forbidden))
 check(2,1,labels,allowed,cover,indicators=True)
for rep in range(250):
 n=R.randrange(1,6);k=R.randrange(4);es=list(it.combinations(range(2*n),2))
 cover=set(R.sample(range(2*n),R.randrange(min(4,2*n)+1)))
 allowed={e for e in es if not set(e)&cover or R.random()<.65}
 labels={e:R.randrange(1<<k) for e in es}
 check(n,k,labels,allowed,cover,indicators=n<=3 and rep<30)
# Exercise n>t and genuinely colliding perfect-family colorings.
for rep in range(4):
 n=6;k=1;es=list(it.combinations(range(2*n),2))
 labels={e:0 if rep==0 else R.randrange(2) for e in es}
 check(n,k,labels,set(es),set())
# Mandatory pair reservation: colliding substitute pairs cannot cover pair zero.
n=3;labels={e:0 for e in it.combinations(range(6),2)}
allowed={e for e in labels if min(e)>=2}
assert one(n,0,labels,allowed,0,(0,0,1),{0}) is None
# Full port-orientation enumeration checks that all alternating single cycles occur.
for n in range(2,6):
 for order in it.permutations(range(1,n)):
  seq=(0,)+order
  for ports in it.product((0,1),repeat=n):
   m=tuple(edge(2*seq[i]+1-ports[i],2*seq[(i+1)%n]+ports[(i+1)%n]) for i in range(n))
   assert sorted(v for e in m for v in e)==list(range(2*n))
   assert all(u//2!=v//2 for u,v in m)
   counts['port_cycles']+=1
print(json.dumps(counts,indent=2));print('PASS')
