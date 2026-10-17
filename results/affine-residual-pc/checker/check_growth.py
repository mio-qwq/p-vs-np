import sys,json,time,hashlib
from pathlib import Path
from dataclasses import asdict
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'design'))
import arb_pc as arb
from connected_family import connected_cycles,pure_literals,graph_components
ROOT=Path(__file__).resolve().parent

def measure(k):
    cnf,n=connected_cycles(k);original=arb.normalize;prefix=set();leaves=set();normalization_ns=0
    def observe(cs,dim,equations=(),stats=None):
        nonlocal normalization_ns
        before=stats.pure_assignments if stats else 0
        t=time.perf_counter_ns();key=original(cs,dim,equations,stats);normalization_ns+=time.perf_counter_ns()-t
        if type(key) is not bool:
            ternary=sum(len(c)==3 for c in key[1])
            if ternary>=4:
                assert stats is None or stats.pure_assignments==before
                assert len(arb.split_components(key))==1
                ordinary=[]
                for c in key[1]:
                    assert all(m.bit_count()==1 for m,b in c)
                    ordinary.append(tuple(m.bit_length()*(1 if b==0 else -1) for m,b in c))
                assert pure_literals(ordinary)==[] and len(graph_components(ordinary))==1
                prefix.add(key)
                if ternary==4:leaves.add(key)
        return key
    arb.normalize=observe;t=time.perf_counter()
    try:answer,stats=arb.solve(cnf,n)
    finally:arb.normalize=original
    assert answer is False and stats.parity_blocks==0
    assert len(prefix)==2**(k+1)-1
    assert len(leaves)==2**k
    return {'k':k,'input_variables':n,'input_clauses':len(cnf),'input_literals':sum(map(len,cnf)),
            'answer':answer,**asdict(stats),'prefix_keys':len(prefix),'selector_complete_keys':len(leaves),
            'seconds':time.perf_counter()-t,'normalization_seconds':normalization_ns/1e9}

rows=[]
for k in range(11):
    row=measure(k);rows.append(row);print(json.dumps(row),flush=True)
    (ROOT/'growth_results.json').write_text(json.dumps(rows,indent=2))
(ROOT/'candidate_sha256.txt').write_text(hashlib.sha256(Path(arb.__file__).read_bytes()).hexdigest()+'\n')
