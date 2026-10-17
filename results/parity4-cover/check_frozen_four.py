from pathlib import Path
import json,time
OUT=Path(__file__).parent
start=time.monotonic();deadline=start+60
V=[0,3,5,6,9,10,12,15];T=[x for x in range(16) if x.bit_count()%2];Q=256
matches={x:[sum(1<<j for j,y in enumerate(V) if ((x^y)>>i&1)==0) for i in range(4)] for x in T}
up=[sum(1<<B for B in range(Q) if A&B==A) for A in range(Q)]
def closure(x,pairs):
 F=up[255]
 for A in matches[x]:F|=up[A]
 for _ in range(len(pairs)+1):
  old=F
  for A,B in pairs:
   if F>>A&1 and F>>B&1:F|=up[A&B]
  if old==F:break
 return F
# Reconstruct initial weighted witnesses from explicit families, not LP output.
def filt(pred):return sum(1<<S for S in range(Q) if pred(S))
import itertools
canonical=[filt(lambda S,x=x:any(S&B==B for B in matches[x])) for x in T]
triples=[sum(1<<V.index(y) for y in R) for R in itertools.combinations(V,3) if all(a^b!=15 for a,b in itertools.combinations(R,2))]
majorities=[filt(lambda S,R=R:(S&R).bit_count()>=2) for R in triples]
hits=[filt(lambda S,R=255^(1<<V.index(a))^(1<<V.index(b)):bool(S&R)) for a,b in itertools.combinations(V,2) if(a^b).bit_count()==2]
Fs=canonical+majorities+hits;assert len(set(Fs))==64
frozen=json.loads((OUT/'frozen_witnesses.json').read_text())
assert frozen['negative_vertices']==V and frozen['scale']==240
loaded=[int(F) for F in frozen['filter_masks']]
assert loaded[:64]==Fs
assert frozen['integer_weights']==[24]*8+[15]*32+[10]*24+[0]*(len(loaded)-64)
Fs=loaded
# Independently verify every added object is an above-target semifilter.
for F in Fs:
 assert not(F&1) and F>>255&1
 assert all(not(F>>A&1) or(F>>B&1) for A in range(Q) for B in range(Q) if A&B==A)
 assert any(all(F>>B&1 for B in matches[x]) for x in T)
cm=(1<<8)-1;mm=((1<<32)-1)<<8;hm=((1<<24)-1)<<40
weight=lambda C:24*(C&cm).bit_count()+15*(C&mm).bit_count()+10*(C&hm).bit_count()
allw=(1<<len(Fs))-1;assert weight(allw)==912
columns={};checked=0;eligible=0
for A in range(Q):
 for B in range(A,Q):
  C=sum(1<<i for i,F in enumerate(Fs) if F>>A&1 and F>>B&1 and not(F>>(A&B)&1))
  assert weight(C)<=240;checked+=1
  if weight(C)>=192:eligible+=1;columns.setdefault(C,(A,B))
Cs=list(columns);N=len(Cs);adj=[0]*N;edges=0
for i,C in enumerate(Cs):
 for j in range(i+1,N):
  D=Cs[j]
  if weight(C|D)>=432 and weight(C&D)<=48:
   adj[i]|=1<<j;edges+=1
wcolumns=[sum(1<<j for j,C in enumerate(Cs) if C>>i&1) for i in range(len(Fs))]
stats={'nodes':0,'weighted_prunes':0,'coverage_prunes':0,'terminal_candidates':0};found=None;complete=True
class Budget(Exception):pass
def dfs(rem,covered,allowed,chosen):
 global found
 stats['nodes']+=1
 if stats['nodes']%1000==0 and time.monotonic()>deadline:raise Budget
 missing=allw^covered
 if not missing:found=chosen;return True
 if weight(missing)>240*rem:stats['weighted_prunes']+=1;return False
 if not allowed:return False
 if rem==1:
  x=missing
  while x and allowed:
   bit=x&-x;i=bit.bit_length()-1;x-=bit;allowed&=wcolumns[i]
  stats['terminal_candidates']+=allowed.bit_count()
  if allowed:
   j=(allowed&-allowed).bit_length()-1;found=chosen+(j,);return True
  stats['coverage_prunes']+=1;return False
 # Every uncovered witness must have some remaining covering column.
 x=missing
 while x:
  bit=x&-x;i=bit.bit_length()-1;x-=bit
  if not(allowed&wcolumns[i]):stats['coverage_prunes']+=1;return False
 while allowed:
  bit=allowed&-allowed;j=bit.bit_length()-1;allowed-=bit
  if dfs(rem-1,covered|Cs[j],allowed&adj[j],chosen+(j,)):return True
 return False
try:dfs(4,0,(1<<N)-1,())
except Budget:complete=False
solution=[columns[Cs[j]] for j in found] if found else None
if solution:
 C=0
 for j in found:C|=Cs[j]
 assert C==allw
report={'status':'complete' if complete else 'budget exhausted','witness_count':len(Fs),'pairs_checked':checked,'eligible_pairs':eligible,'distinct_eligible_columns':N,'compatibility_edges':edges,'search_stats':stats,'cover_of_witness_subset':solution,'conclusion':'no four-pair cover exists' if complete and not solution else 'not a lower-bound proof','elapsed_seconds':time.monotonic()-start,'filter_masks':[str(F) for F in Fs],'pruning':'scale240: total912; any4cover eachcolumn>=192; anychosenpair union>=432 andintersection<=48'}
(OUT/'standalone_check_result.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='filter_masks'},indent=2))

assert complete, 'INCOMPLETE: budget exhausted'
assert solution is None, 'FAIL: four-cover found'
