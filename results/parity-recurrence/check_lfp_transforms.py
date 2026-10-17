"""Finite regression checks; does not prove the all-circuit recurrence."""
import random,json
from pathlib import Path
rng=random.Random(741903)
def solve(gates,lits,out):
 s=[False]*len(gates)
 def val(f):return any(lits[i] if i<len(lits) else s[i-len(lits)] for i in f)
 for _ in range(len(gates)+1):
  t=[val(a) and val(b) for a,b in gates]
  if t==s:return any(lits[i] if i<len(lits) else s[i-len(lits)] for i in out)
  assert all(not a or b for a,b in zip(s,t));s=t
 raise AssertionError('monotone iteration did not stabilize')
count=0
for n in range(1,5):
 for k in range(1,7):
  L=2*n
  for trial in range(150):
   gates=[tuple({i for i in range(L+k) if rng.randrange(5)==0} for _ in range(2)) for j in range(k)]
   out={i for i in range(L+k) if rng.randrange(3)==0}
   clean=[(a-{L+j},b-{L+j}) for j,(a,b) in enumerate(gates)]
   j=rng.randrange(k);lit=rng.randrange(L)
   fact=[(set(a),set(b)) for a,b in clean]
   fact[j][0].add(lit);fact[j][1].add(lit)
   transformed=[]
   for i,(a,b) in enumerate(fact):
    aa=a-{lit} if i==j else set(a)
    bb=b-{lit} if i==j else set(b)
    if L+j in aa:aa.add(lit)
    if L+j in bb:bb.add(lit)
    transformed.append((aa,bb))
   out2=out|{lit} if L+j in out else out
   for x in range(1<<n):
    ls=[((x>>(i//2))&1)==i%2 for i in range(L)]
    assert solve(gates,ls,out)==solve(clean,ls,out)
    assert solve(fact,ls,out)==solve(transformed,ls,out2)
    count+=1
# Least fixed point is essential: y=y AND 1 remains zero, despite fixed point one.
assert solve([({2},{1})],[False,True],{2}) is False
report={'seed':741903,'input_circuit_cases':count,'self_loop_deletion':'pass','duplicate_literal_factoring':'pass','least_fixed_point_negative_control':'pass','scope':'finite regression only; general proof remains separate'}
Path(__file__).with_name('lfp_transform_result.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
