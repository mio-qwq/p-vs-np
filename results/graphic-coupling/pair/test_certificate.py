import random,itertools,json
from pathlib import Path
from certificate_solver import *
r=random.Random(9001);checks=0;witnesses=0
for n in range(3,8):
 for _ in range(100):
  options=list(itertools.combinations(range(n),2));r.shuffle(options);edges=options[:r.randrange(1,min(9,len(options))+1)]
  remaining=list(range(len(edges)));r.shuffle(remaining);pairs=[]
  while remaining:
   i=remaining.pop();cand=[j for j in remaining if set(edges[i])&set(edges[j])]
   if cand and r.randrange(2):j=r.choice(cand);remaining.remove(j);pairs.append((i,j))
  extra=[]
  for i,j in pairs:extra.append(tuple(set(edges[i])^set(edges[j])))
  extedges=edges+extra
  # Scramble the incidence row representation by invertible elementary row ops.
  A=[(1<<u)|(1<<v) for u,v in edges]
  target=r.randrange(1<<n)
  for _ in range(3*n):
   u,v=r.sample(range(n),2)
   A=[a^(((a>>u)&1)<<v) for a in A]
   target^=((target>>u)&1)<<v
  expected=[]
  for mask in range(1<<len(A)):
   syn=0
   for i,a in enumerate(A):
    if mask>>i&1:syn^=a
   if syn==target and all(not(mask>>i&1 and mask>>j&1) for i,j in pairs):expected.append(mask)
  actual=solve_with_certificate(A,pairs,target,n,extedges)
  assert (actual is None)==(not expected)
  if actual is not None:assert actual in expected;witnesses+=1
  checks+=1
out={'scrambled_binary_matrix_certificate_solver_checks':checks,'returned_witnesses':witnesses,'graphic_discovery':'not implemented; supplied certificates are checked in polynomial time'}
Path(__file__).with_name('certificate_results.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
