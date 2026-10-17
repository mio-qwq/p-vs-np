"""Random regression for the unique opposite-operand bottleneck lemma."""
import random,json
from pathlib import Path
r=random.Random(17062026)
def output(gates,inputs,out):
    L=len(inputs);s=[False]*len(gates)
    def ev(a): return any(inputs[i] if i<L else s[i-L] for i in a)
    for _ in range(len(gates)+1):
        t=[ev(a) and ev(b) for a,b in gates]
        if t==s: return int(ev(out))
        assert all(not u or v for u,v in zip(s,t))
        s=t
    raise AssertionError('No convergence')
allowed={(0,0,0,0),(1,1,1,1),(0,0,1,1),(0,1,0,1),(0,0,0,1)}
hist={str(x):0 for x in sorted(allowed)}
cases=0
for k in range(1,9):
    for _ in range(2500):
        L=8;j=r.randrange(k)
        gates=[(set(i for i in range(2,L+k) if r.randrange(4)==0),set(i for i in range(2,L+k) if r.randrange(4)==0)) for _ in range(k)]
        gates[j][0].add(0);gates[j][1].add(1)
        out={i for i in range(2,L+k) if r.randrange(3)==0}
        rest=[bool(r.randrange(2)) for _ in range(L-2)]
        table=tuple(output(gates,[a,b]+rest,out) for a,b in ((False,False),(False,True),(True,False),(True,True)))
        assert table in allowed, (k,j,gates,out,rest,table)
        hist[str(table)]+=1;cases+=1
result={'seed':17062026,'circuits_and_fixed_contexts':cases,'input_evaluations':cases*4,'allowed_truth_tables_only':True,'histogram':hist,'scope':'finite randomized regression; proof separate'}
Path(__file__).with_name('bottleneck_minor_result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
