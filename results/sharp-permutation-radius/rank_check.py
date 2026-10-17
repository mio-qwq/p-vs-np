from itertools import permutations,combinations
from math import prod

def rank(rows):
 piv={}
 for x in rows:
  while x:
   i=x.bit_length()-1
   if i in piv:x^=piv[i]
   else:piv[i]=x;break
 return len(piv)
for n in range(2,8):
 ps=list(permutations(range(n)))
 for d in range(1,3):
  keys=[()]
  for s in range(1,d+1):
   for dom in combinations(range(n),s):
    for ran in permutations(range(n),s):keys.append(tuple(zip(dom,ran)))
  ix={k:i for i,k in enumerate(keys)}
  rows=[]
  for p in ps:
   z=1
   for s in range(1,d+1):
    for dom in combinations(range(n),s):z|=1<<ix[tuple((a,p[a]) for a in dom)]
   rows.append((sum(a!=b for a,b in enumerate(p)),z))
  R=min(n,2*d+1);full=rank(z for _,z in rows);good=rank(z for s,z in rows if s<=R);bad=rank(z for s,z in rows if s<R)
  assert full==good and bad<full
  print('GF2 rank',n,d,'radius',R,'full',full,'ball',good,'previous',bad,flush=True)
for n in (2,4,6,8):
 nonzero=0
 for p in permutations(range(n)):
  v=prod(p[a]==a+1 for a in range(0,n,2))
  if v:assert all(a!=b for a,b in enumerate(p));nonzero+=1
 assert nonzero
 print('even monomial',n,'nonzero',nonzero,flush=True)
print('PASS')
