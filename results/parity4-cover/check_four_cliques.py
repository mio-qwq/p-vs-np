from pathlib import Path
import json,runpy,time
start=time.monotonic()
d=runpy.run_path(str(Path(__file__).with_name('check_dual.py')))
expected=[sum(1<<i for i,v in enumerate(f) if v) for f in d['filters']]
r=json.loads(Path(__file__).with_name('frozen_witnesses.json').read_text())
fs=[int(s) for s in r['filter_masks']]
assert fs[:64]==expected and len(set(fs))==len(fs)
V=d['V'];P=d['P']
for f in fs:
 assert 0<=f<(1<<256) and not(f&1) and f>>255&1
 for a in range(256):
  if f>>a&1:
   for i in range(8):assert f>>(a|1<<i)&1
 assert any(all(f>>sum(1<<j for j,y in enumerate(V) if (x>>i&1)==(y>>i&1))&1 for i in range(4)) for x in P)
accepted=[sum(1<<j for j,f in enumerate(fs) if f>>a&1) for a in range(256)]
masks=[(1<<8)-1,((1<<32)-1)<<8,((1<<24)-1)<<40]
def w(c):return sum(a*(b&c).bit_count() for a,b in zip([24,15,10],masks))
cols=set()
for a in range(256):
 for b in range(a,256):
  c=accepted[a]&accepted[b]&~accepted[a&b]
  assert w(c)<=240
  if w(c)>=192:cols.add(c)
cols=sorted(cols);N=len(cols);allbits=(1<<len(fs))-1
adj=[0]*N;edges=0
for i in range(N):
 for j in range(i+1,N):
  if w(cols[i]|cols[j])>=432 and w(cols[i]&cols[j])<=48:
   adj[i]|=1<<j;edges+=1
# Independent algorithm: enumerate all compatible four-cliques,
# without the original depth-first remaining-witness pruning.
triangles=0;cliques=0;covers=[]
for i in range(N):
 js=adj[i]
 while js:
  bit=js&-js;js^=bit;j=bit.bit_length()-1
  common=adj[i]&adj[j];ks=common
  while ks:
   bit=ks&-ks;ks^=bit;k=bit.bit_length()-1;triangles+=1
   ls=common&adj[k]
   while ls:
    bit=ls&-ls;ls^=bit;l=bit.bit_length()-1;cliques+=1
    if cols[i]|cols[j]|cols[k]|cols[l]==allbits:covers.append((i,j,k,l))
   if triangles%100000==0 and time.monotonic()-start>90:raise RuntimeError('INCOMPLETE resource stop')
assert not covers,covers
out={'status':'complete PASS','valid_witnesses':len(fs),'columns':N,'edges':edges,'triangles':triangles,'four_cliques':cliques,'four_covers':0,'elapsed_seconds':time.monotonic()-start,'scope':'exact finite lower bound 5, not P-versus-NP separation'}
Path(__file__).with_name('four_clique_result.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
