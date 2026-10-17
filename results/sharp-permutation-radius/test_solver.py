from itertools import permutations
from random import Random
from solver import solve
R=Random(20261017);count=0
for n in range(8):
 for k in range(4):
  for rep in range(12):
   L=[[R.randrange(1<<k) for _ in range(n)] for _ in range(n)]
   feasible=set()
   for p in permutations(range(n)):
    z=0
    for i,j in enumerate(p):z^=L[i][j]
    feasible.add(z)
   for t in range(1<<k):
    p=solve(L,k,t);assert (p is not None)==(t in feasible)
    if p is not None:
     assert sorted(p)==list(range(n));z=0
     for i,j in enumerate(p):z^=L[i][j]
     assert z==t
    count+=1
for L,k,t in [([[None]],1,0),([[0,0]],1,0),([[True]],1,0),([[0]],-1,0),([[0]],1,2)]:
 try:solve(L,k,t)
 except ValueError:pass
 else:raise AssertionError('malformed input accepted')
print({'exact_target_comparisons':count,'n_max':7,'malformed_controls':5})
