import random,itertools,json
from pathlib import Path
from graphic import *
from distance_two import *
r=random.Random(1221);tests=0;witnesses=0;maxedges=0
for n in range(2,6):
 for _ in range(20):
  choices=list(itertools.combinations(range(n),2));r.shuffle(choices);edges=choices[:r.randrange(min(4,len(choices))+1)]
  ids=list(range(len(edges)));r.shuffle(ids);pairs=[tuple(ids[i:i+2]) for i in range(0,len(ids)-1,2)]
  target=r.randrange(1<<n)
  N,E,P,B,halves,ones,zeros=localize(n,edges,pairs,target)
  assert all(pair_distance_at_most_two(E,pair) for pair in P)
  assert len(set(e for p in P for e in p))==len(E)==2*len(P)
  assert len({tuple(sorted(e)) for e in E})==len(E)
  for mask in range(1<<len(edges)):
   if valid(edges,pairs,target,mask):
    assert valid(E,P,B,lift(mask,halves,ones));witnesses+=1
  original=brute_join(edges,pairs,target);actual=brute_join(E,P,B)
  assert (original is None)==(actual is None)
  if actual is not None:
   assert all(actual>>e&1 for e in ones) and all(not(actual>>e&1) for e in zeros)
   assert all(((actual>>a)&1)==((actual>>b)&1) for a,b in halves)
   recovered=sum(((actual>>a)&1)<<i for i,(a,b) in enumerate(halves))
   assert valid(edges,pairs,target,recovered)
  maxedges=max(maxedges,len(E));tests+=1
out={'exact_original_vs_distance2_tjoin_checks':tests,'lifted_witnesses':witnesses,'max_transformed_edges':maxedges,'complete_pairing_simple_graph_and_distance2_verified':True}
Path(__file__).with_name('distance_two_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
