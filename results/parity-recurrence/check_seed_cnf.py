import json,itertools
from pathlib import Path
# literal token 2*i+b is true exactly when input coordinate i equals b.
def matchings(tokens):
 if not tokens:yield ();return
 a,*rest=tokens
 yield from matchings(rest)
 for j,b in enumerate(rest):
  for P in matchings(rest[:j]+rest[j+1:]):yield ((a,b),)+P
res=[]
for m in (1,3,5):
 count=0;bad=[]
 for P in matchings(list(range(2*m))):
  # H forbids simultaneous truth of each paired seed literal.
  found=any(x.bit_count()%2 and all(not(((x>>(a//2))&1)==a%2 and ((x>>(b//2))&1)==b%2) for a,b in P) for x in range(1<<m))
  count+=1
  if not found:bad.append(P)
 assert not bad
 res.append({'variables':m,'all_partial_literal_matchings':count,'without_odd_satisfying_assignment':len(bad)})
# Sharp obstruction to extending this exact lemma to even dimension.
m=4;P=((0,3),(1,2),(4,7),(5,6))
solutions=[x for x in range(1<<m) if all(not(((x>>(a//2))&1)==a%2 and ((x>>(b//2))&1)==b%2) for a,b in P)]
assert solutions==[0,3,12,15]
report={'odd_dimension_tests':res,'even_counterexample':{'variables':m,'seed_literal_pairs':P,'solutions':solutions}}
Path(__file__).with_name('seed_cnf_result.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
