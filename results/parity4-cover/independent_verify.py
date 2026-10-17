import json,hashlib,time
from pathlib import Path
src=Path(__file__).resolve().parent;out=src
files=['check_frozen_four.py','frozen_witnesses.json','verify_upper5.py']
hashes={f:hashlib.sha256((src/f).read_bytes()).hexdigest() for f in files}
data=json.loads((src/'frozen_witnesses.json').read_text());Fs=list(map(int,data['filter_masks']))
assert len(Fs)==120==len(set(Fs))
V=[i for i in range(16) if i.bit_count()%2==0];T=[i for i in range(16) if i.bit_count()%2]
W=[24]*8+[15]*32+[10]*24+[0]*56
for F in Fs:
 assert F>=0 and F.bit_length()<=256 and not(F&1) and F>>255&1
 # Check upward closure along Hasse edges, sufficient by transitivity.
 for A in range(256):
  if F>>A&1:
   for b in range(8): assert F>>(A|(1<<b))&1
 assert any(all(F>>sum(1<<j for j,y in enumerate(V) if not((x^y)>>i&1))&1 for i in range(4)) for x in T)
def weight(C):return sum(w for i,w in enumerate(W) if C>>i&1)
columns=set();paircount=0;eligible=0;maxload=0
for A in range(256):
 for B in range(A,256):
  C=sum(1<<i for i,F in enumerate(Fs) if F>>A&1 and F>>B&1 and not(F>>(A&B)&1))
  w=weight(C);maxload=max(maxload,w);assert w<=240;paircount+=1
  if w>=192:eligible+=1;columns.add(C)
Cs=sorted(columns);n=len(Cs);ALL=(1<<120)-1
adj=[0]*n
for i in range(n):
 for j in range(i):
  if weight(Cs[i]|Cs[j])>=432:
   assert weight(Cs[i]&Cs[j])<=48
   adj[i]|=1<<j;adj[j]|=1<<i
byw=[sum(1<<j for j,C in enumerate(Cs) if C>>i&1) for i in range(120)]
calls=0
# Independent exact set-cover search: branch on rarest uncovered witness,
# not increasing-column depth-first enumeration used by design artifact.
def search(covered,allowed,left):
 global calls
 calls+=1
 if covered==ALL:return []
 if left==0 or weight(ALL^covered)>240*left:return None
 options=None
 for i in range(120):
  if not(covered>>i&1):
   cand=allowed&byw[i]
   if not cand:return None
   if options is None or cand.bit_count()<options.bit_count():options=cand
 while options:
  b=options&-options;options^=b;j=b.bit_length()-1
  allowed^=b
  result=search(covered|Cs[j],allowed&adj[j],left-1)
  if result is not None:return [j]+result
 return None
sol=search(0,(1<<n)-1,4);assert sol is None
# Independent five-AND truth construction; XOR and XNOR calculated using gates.
cover=[[0,0] for _ in range(5)]
for x in range(16):
 a,b,c,d=[bool(x>>i&1) for i in range(4)]
 ins=[(a or b,not a or not b),(a or not b,not a or b),(c or d,not c or not d),(c or not d,not c or d)]
 u,nu,v,nv=[p and q for p,q in ins]
 ins.append((u or v,nu or nv))
 assert (ins[-1][0] and ins[-1][1])==bool(x.bit_count()%2)
 if x in V:
  for j,(p,q) in enumerate(ins):cover[j][0]|=int(p)<<V.index(x);cover[j][1]|=int(q)<<V.index(x)
# Closure proof checks all semifilters via upward closure and the five implications.
for x in T:
 accepted={255}|{sum(1<<j for j,y in enumerate(V) if not((x^y)>>i&1)) for i in range(4)}
 while True:
  enlarged={B for A in accepted for B in range(256) if A&B==A}
  enlarged|={A&B for A,B in cover if A in enlarged and B in enlarged}
  if enlarged==accepted:break
  accepted=enlarged
 assert 0 in accepted
assert hashes=={f:hashlib.sha256((src/f).read_bytes()).hexdigest() for f in files}
result={'status':'pass','source_sha256':hashes,'valid_witnesses':120,'total_scaled_weight':sum(W),'maximum_pair_load':maxload,'all_unordered_pairs':paircount,'eligible_pairs':eligible,'unique_eligible_columns':n,'independent_search':'rarest-uncovered-witness exact cover branching','search_calls':calls,'four_cover_found':False,'five_AND_upper_truth_checks':16,'five_pair_upper_closures':8,'cover':cover,'exact_unrestricted_pair_cover':5}
(out/'independent_result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
