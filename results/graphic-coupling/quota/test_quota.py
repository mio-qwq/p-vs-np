import random,itertools,json
from pathlib import Path
from quota import *
r=random.Random(5513);count=0;nontrivial=0
for n in range(2,9):
 for _ in range(100):
  options=list(itertools.combinations(range(n),2));r.shuffle(options);edges=options[:r.randrange(min(10,len(options))+1)]
  groups=[]
  for v in range(n):
   ids=[i for i,e in enumerate(edges) if v in e];r.shuffle(ids)
   while ids:
    width=r.randrange(1,len(ids)+1);group=ids[:width];ids=ids[width:];cap=r.randrange(width+1)
    groups.append((v,group,cap));nontrivial+=width>2
  target=r.randrange(1<<n)
  expected=next((x for x in range(1<<len(edges)) if valid_quota(edges,groups,target,x)),None)
  actual=solve_quota(n,edges,groups,target)
  assert (expected is None)==(actual is None),(n,edges,groups,target,expected,actual)
  count+=1
out={'quota_matching_vs_exhaustive_checks':count,'tested_groups_larger_than_two':nontrivial,'backend':'independent standard Edmonds implementation, ../blossom/blossom.py'}
Path(__file__).with_name('results.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
