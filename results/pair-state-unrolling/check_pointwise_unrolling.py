import itertools,json
rows=[]
for k in range(1,4):
 vals=range(1<<k)
 fs=[table for table in itertools.product((0,1),repeat=1<<k) if all(not table[a] or table[b] for a in vals for b in vals if a&b==a)]
 count=0; maxround=0
 for network in itertools.product(fs,repeat=k):
  def F(x): return sum(table[x]<<j for j,table in enumerate(network))
  x=0
  for t in range(k): x=F(x)
  assert F(x)==x
  count+=1
  x=0;t=0
  while F(x)!=x:x=F(x);t+=1
  maxround=max(maxround,t)
 rows.append({'coordinates':k,'monotone_component_functions':len(fs),'networks_tested':count,'maximum_strict_rounds':maxround})
print(json.dumps(rows,indent=2))
