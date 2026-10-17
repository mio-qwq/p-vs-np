from pathlib import Path
import json
OUT=Path(__file__).parent
V=[0,3,5,6,9,10,12,15];T=[x for x in range(16) if x.bit_count()%2]
truth=[];pairs_by_input=[]
for x in range(16):
 a,b,c,d=[(x>>i)&1 for i in range(4)]
 pairs=[(a|b,(1-a)|(1-b)),(a|(1-b),(1-a)|b),(c|d,(1-c)|(1-d)),(c|(1-d),(1-c)|d)]
 u,ub,v,vb=[p&q for p,q in pairs]
 pairs.append((u|v,ub|vb));out=pairs[-1][0]&pairs[-1][1]
 assert out==x.bit_count()%2
 truth.append(out);pairs_by_input.append(pairs)
cover=[(sum(pairs_by_input[y][j][0]<<i for i,y in enumerate(V)),sum(pairs_by_input[y][j][1]<<i for i,y in enumerate(V))) for j in range(5)]
up=[sum(1<<B for B in range(256) if A&B==A) for A in range(256)]
closures=[]
for x in T:
 F=up[255]
 for i in range(4):F|=up[sum(1<<j for j,y in enumerate(V) if ((x^y)>>i&1)==0)]
 rounds=0
 while True:
  old=F
  for A,B in cover:
   if F>>A&1 and F>>B&1:F|=up[A&B]
  rounds+=1
  if old==F:break
 assert F&1
 closures.append({'target':x,'rounds':rounds,'empty_derived':True})
r={'status':'all16truthassignmentsand8closuresverified','AND_count':5,'cover_masks':cover,'truth_table':truth,'closures':closures}
(OUT/'upper5_verified.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
