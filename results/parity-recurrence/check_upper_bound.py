"""Rebuild acyclic dual-rail parity circuits and evaluate all assignments."""
import json
from pathlib import Path
def build(n):
 gates=[]
 def gate(op,a,b):
  idx=2*n+len(gates);gates.append((op,a,b));return idx
 p,q=1,0 # tokens 2*i+b mean xi=b
 for i in range(1,n):
  x,nx=2*i+1,2*i
  pp=gate('AND',gate('OR',p,x),gate('OR',q,nx))
  if i<n-1: qq=gate('AND',gate('OR',p,nx),gate('OR',q,x))
  else:qq=None
  p,q=pp,qq
 return gates,p
def evaluate(n,gates,out,x):
 v=[((x>>(j//2))&1)==j%2 for j in range(2*n)]
 for op,a,b in gates:v.append(v[a] and v[b] if op=='AND' else v[a] or v[b])
 return v[out]
report=[]
for n in range(2,13):
 g,o=build(n); count=sum(op=='AND' for op,_,_ in g)
 assert count==2*n-3
 assert all(evaluate(n,g,o,x)==bool(x.bit_count()%2) for x in range(1<<n))
 report.append({'n':n,'and_gates':count,'assignments':1<<n})
g,o=build(5);damaged=list(g);op,a,b=damaged[-1];damaged[-1]=('OR',a,b)
assert any(evaluate(5,damaged,o,x)!=bool(x.bit_count()%2) for x in range(32))
r={'checks':report,'rho5_upper':7,'mutated_final_AND_to_OR_rejected':True,'scope':'finite evaluation confirms constructed instances; general upper proof in PROOF.md'}
Path(__file__).with_name('upper_bound_result.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
