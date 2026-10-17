import json,time
from pathlib import Path
from dataclasses import asdict
from arb import solve
from families import selector_stars
results=[]
for k in range(0,11):
    cnf,n=selector_stars(k)
    start=time.perf_counter()
    answer,stats=solve(cnf,n)
    row={'k':k,'n':n,'clauses':len(cnf),'literal_occurrences':sum(map(len,cnf)),
         'answer':answer,'elapsed_seconds':time.perf_counter()-start,**asdict(stats)}
    assert not answer and stats.unique_states>=2**k
    results.append(row)
    print(json.dumps(row),flush=True)
with open(Path(__file__).with_name('growth_results.json'),'w') as f:
    json.dump(results,f,indent=2)
