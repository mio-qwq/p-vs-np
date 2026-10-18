import itertools,json,collections
from pathlib import Path
P=list(itertools.permutations(range(4)))
def sg(p):return (-1)**sum(p[a]>p[b] for a in range(4) for b in range(a+1,4))
S={p:sg(p) for p in P}
def canon(rows):
 return min(tuple(sorted(sum(((r>>p[j])&1)<<j for j in range(4)) for r in rows)) for p in P)
def components(rows):
 match=[p for p in P if all(rows[i]&(1<<p[i]) for i in range(4))]
 if not match:return None,None,None
 allowed=[0]*4
 for p in match:
  for i,j in enumerate(p):allowed[i]|=1<<j
 adj={i:set() for i in range(8)}
 for i,r in enumerate(allowed):
  for j in range(4):
   if r>>j&1:adj[i].add(4+j);adj[4+j].add(i)
 unseen=set(adj);comps=[]
 while unseen:
  stack=[min(unseen)];component=set(stack);unseen-=component
  while stack:
   for j in adj[stack.pop()]-component:
    component.add(j);unseen.remove(j);stack.append(j)
  rr=[i for i in component if i<4];cc=[i-4 for i in component if i>=4]
  if len(rr)!=len(cc): raise RuntimeError('Unbalanced allowed-edge component')
  comps.append((rr,cc))
 return allowed,match,comps
orb_counts=collections.Counter();pm=0;irreducible=0;block_sizes=collections.Counter()
for rows in itertools.product(range(16),repeat=4):
 allowed,match,comp=components(rows)
 if match is None:continue
 pm+=1;block_sizes[tuple(sorted(len(r) for r,c in comp))]+=1
 if len(comp)==1:
  irreducible+=1
  if rows!=tuple(allowed): raise RuntimeError('An unused edge exists in an elementary graph')
  if sum(S[p] for p in match)==0:orb_counts[canon(rows)]+=1
out={'total_masks':16**4,'perfect_matching_masks':pm,'irreducible_masks':irreducible,'block_sizes':{str(k):v for k,v in block_sizes.items()},'singular_irreducible_orbit_count':len(orb_counts),'orbits':[{'rows':list(k),'size':v} for k,v in sorted(orb_counts.items())]}

if out['perfect_matching_masks']!=37823 or out['irreducible_masks']!=6785 or out['singular_irreducible_orbit_count']!=23:
 raise RuntimeError('Unexpected exhaustive mask counts')
sorted_counts=collections.Counter()
for rows in itertools.combinations_with_replacement(range(1,16),4):
 allowed,match,comp=components(rows)
 if match is None: key='no_matching'
 elif sum(S[p] for p in match): key='nonsingular_mask'
 elif len(comp)>1: key='singular_disconnected'
 else: key='singular_connected'
 sorted_counts[key]+=1
expected={'no_matching':1062,'nonsingular_mask':940,'singular_disconnected':851,'singular_connected':207}
if dict(sorted_counts)!=expected: raise RuntimeError(('Sorted mask counts',dict(sorted_counts)))
out['sorted_multiset_counts']=dict(sorted_counts)
expected_rows=[(3,5,10,12),(3,5,10,15),(3,5,11,13),(3,5,14,14),(3,5,15,15),(3,7,11,12),(3,7,11,15),(3,7,12,15),(3,7,13,13),(3,7,15,15),(3,12,15,15),(3,13,13,14),(3,13,13,15),(3,13,14,15),(3,13,15,15),(3,15,15,15),(7,7,11,11),(7,7,11,13),(7,7,11,15),(7,7,15,15),(7,11,15,15),(7,15,15,15),(15,15,15,15)]
if sorted(orb_counts)!=expected_rows: raise RuntimeError('Orbit representatives differ')
print(json.dumps(out,indent=2))
Path(__file__).with_name('orbit_results.json').write_text(json.dumps(out,indent=2)+'\n')
