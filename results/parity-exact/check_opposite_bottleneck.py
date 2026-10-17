import itertools,json
from pathlib import Path
# Two charged states g,z. A factor mask selects g,z,true constant.
def factor(mask,state):return bool(mask&4 or mask&state)
def output(A,B,C,D,O,l,h):
 s=0
 for _ in range(3):
  ns=int((l or factor(A,s)) and (h or factor(B,s))) | (int(factor(C,s) and factor(D,s))<<1)
  if ns==s:return int(bool(O&s))
  s=ns
 raise AssertionError('failed monotone convergence')
hist={};count=0
for A,B,C,D in itertools.product(range(8),repeat=4):
 for O in range(4):
  table=tuple(output(A,B,C,D,O,l,h) for l,h in ((0,0),(0,1),(1,0),(1,1)))
  assert table!=(0,1,1,1)
  hist[str(table)]=hist.get(str(table),0)+1;count+=1
res={'two_AND_state_systems_checked':count,'OR_minor_found':False,'truth_tables':hist}
Path(__file__).with_name('opposite_bottleneck_result.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
