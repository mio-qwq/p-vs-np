"""Complete bipartite fixed-k parity matching by sharp support testing.
No missing edges and no general-graph claim. Runtime n^{O(k)}, not FPT.
"""
from itertools import combinations,permutations

def solve(labels,k,target):
 if type(k) is not int or k<0:raise ValueError('nonnegative integer k required')
 if type(target) is not int or not 0<=target<(1<<k):raise ValueError('target out of range')
 n=len(labels)
 if any(len(row)!=n for row in labels):raise ValueError('square complete matrix required')
 if any(type(a) is not int or not 0<=a<(1<<k) for row in labels for a in row):raise ValueError('invalid edge label')
 base=0
 for i in range(n):base^=labels[i][i]
 if base==target:return list(range(n))
 for s in range(2,min(n,2*k+1)+1):
  for support in combinations(range(n),s):
   for images in permutations(support):
    if any(a==b for a,b in zip(support,images)):continue
    value=base
    for a,b in zip(support,images):value^=labels[a][a]^labels[a][b]
    if value==target:
     p=list(range(n))
     for a,b in zip(support,images):p[a]=b
     return p
 return None
