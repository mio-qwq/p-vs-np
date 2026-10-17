import random,json,itertools
from pathlib import Path
from graphic import *
r=random.Random(2026101713);checks=0;max_nodes=0
for n in range(2,8):
 for _ in range(100):
  all_edges=list(itertools.combinations(range(n),2));r.shuffle(all_edges);edges=all_edges[:r.randrange(min(9,len(all_edges))+1)]
  available=list(range(len(edges)));r.shuffle(available);pairs=[]
  while available:
   i=available.pop();matches=[j for j in available if set(edges[i])&set(edges[j])]
   if matches and r.randrange(2):
    j=r.choice(matches);available.remove(j);pairs.append((i,j))
  target=r.randrange(1<<n);N,E,external=gadget(n,edges,pairs,target);max_nodes=max(max_nodes,N)
  PM=brute_pm(N,E);expected=brute_join(edges,pairs,target)
  assert (PM is not None)==(expected is not None),(n,edges,pairs,target)
  if PM is not None:
   pm={frozenset(e) for e in PM};mask=sum(1<<i for i,e in enumerate(external) if frozenset(e) in pm)
   assert valid(edges,pairs,target,mask)
  checks+=1
# Local gadget exhaustion with arbitrary selected port subsets.
local_checks=0
for d in range(9):
 for p in range(d//2+1):
  for parity in range(2):
   # d ports, pair private vertices, optional dummy. Remove externally selected ports.
   delta=((d+p)&1)^parity;N=d+p+delta
   E=list(itertools.combinations(list(range(d))+([d+p] if delta else []),2))
   E += [(d+i,2*i+j) for i in range(p) for j in range(2)]
   for mask in range(1<<d):
    keep=[i for i in range(N) if i>=d or not(mask>>i&1)];idx={v:i for i,v in enumerate(keep)}
    sub=[(idx[a],idx[b]) for a,b in E if a in idx and b in idx]
    actual=brute_pm(len(keep),sub) is not None
    expected=mask.bit_count()%2==parity and all((mask>>(2*i))&3!=3 for i in range(p))
    assert actual==expected
    local_checks+=1
# SAT reduction: enumerate all simple branch paths, independent of truth assignment.
sat_checks=0
for n in (3,4,5):
 for _ in range(60):
  clauses=[tuple((v+1)*r.choice([-1,1]) for v in r.sample(range(n),3)) for _ in range(r.randrange(1,5))]
  expected=any(all(any(bool(x>>(abs(l)-1)&1)==(l>0) for l in c) for c in clauses) for x in range(1<<n))
  N,E,pairs,target,opts=reduce_sat(n,clauses,pad_all=True)
  assert len(set(e for pair in pairs for e in pair))==len(E)==2*len(pairs)
  assert len({tuple(sorted(e)) for e in E})==len(E)
  found=False
  for choices in itertools.product(*opts):
   mask=sum(1<<e for branch in choices for e in branch)
   if valid(E,pairs,target,mask):found=True;break
  assert found==expected
  sat_checks+=1
out={'random_incident_pair_global_checks':checks,'max_matching_gadget_vertices':max_nodes,'exhaustive_local_signature_checks':local_checks,'sat_to_arbitrary_pair_path_checks':sat_checks,'matching_oracle':'memoized exhaustive search used only for validation, not a polynomial implementation'}
Path(__file__).with_name('results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
# Strict3CNF UNSAT control plus all eight single-clause deletions.
all8=[tuple((i+1)*signs[i] for i in range(3)) for signs in itertools.product((-1,1),repeat=3)]
controls=[all8]+[all8[:i]+all8[i+1:] for i in range(8)]
for ci,clauses in enumerate(controls):
 N,E,pairs,target,opts=reduce_sat(3,clauses,pad_all=True)
 found=False
 for choices in itertools.product(*opts):
  mask=sum(1<<e for branch in choices for e in branch)
  if valid(E,pairs,target,mask):found=True;break
 assert found==(ci!=0)
out['strict_3cnf_unsat_and_single_deletion_controls']=9
# Direct exhaustive T-join oracle on two contradictory unit clauses.
N,E,pairs,target,opts=reduce_sat(1,[(1,),(-1,)],pad_all=True)
assert brute_join(E,pairs,target) is None
out['direct_unsat_tjoin_control_edges']=len(E)
Path(__file__).with_name('results.json').write_text(json.dumps(out,indent=2)+'\n');print('Additional UNSAT controls passed')
