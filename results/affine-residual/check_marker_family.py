"""Independent selector/star adversarial family and exact residual-state census."""
import sys,json,time
from pathlib import Path
from dataclasses import asdict
sys.path.insert(0,str(Path(__file__).resolve().parent))
import arb
from exact_oracle import sat_witness
from test_families import pigeonhole,parity_clause_block,hide_clauses,tseitin_complete4
OUT=Path(__file__).resolve().parent

def marker_family(k):
    selectors=list(range(1,k+1));partners=list(range(k+1,2*k+1))
    php,_=pigeonhole(3)
    cs=[tuple((abs(l)+2*k)*(1 if l>0 else -1) for l in c) for c in php]
    nextvar=2*k+13
    stars=[]
    for i,(x,t) in enumerate(zip(selectors,partners),1):
        cs.append((x,t));a=nextvar;nextvar+=1;leaves=[]
        for _ in range(i):
            b=nextvar;nextvar+=1;leaves.append(b);cs.append((x,a,b))
        stars.append((a,leaves))
    return cs,nextvar-1

def measure(cnf,n,cache=True):
    original=arb.normalize;leaf_keys=set();total_normalize_ns=0;max_mask_bits=0;max_terms_seen=0
    def observed(cs,dim,equations=()):
        nonlocal total_normalize_ns,max_mask_bits,max_terms_seen
        max_mask_bits=max(max_mask_bits,max((m.bit_length() for c in cs for m,b in c),default=0))
        max_terms_seen=max(max_terms_seen,sum(map(len,cs)))
        t=time.perf_counter_ns();key=original(cs,dim,equations);total_normalize_ns+=time.perf_counter_ns()-t
        if type(key) is not bool and sum(len(c)==3 for c in key[1])==4:
            leaf_keys.add(key)
        return key
    arb.normalize=observed;t=time.perf_counter()
    try:answer,stats=arb.solve(cnf,n,cache=cache,max_states=200000)
    finally:arb.normalize=original
    return {'answer':answer,**asdict(stats),'seconds':time.perf_counter()-t,'normalization_seconds':total_normalize_ns/1e9,'four_ternary_keys':len(leaf_keys),'max_mask_bits':max_mask_bits,'max_terms_seen':max_terms_seen}

def main():
    records=[]
    for k in range(11):
        cnf,n=marker_family(k);row={'family':'selector_stars','k':k,'n':n,'input_clauses':len(cnf),'input_literals':sum(map(len,cnf)),**measure(cnf,n)}
        assert row['answer'] is False
        assert row['parity_blocks']==0
        assert row['four_ternary_keys']==2**k,('leaf count',row)
        if k<=1:assert sat_witness(cnf,n) is None
        records.append(row);print(json.dumps(row),flush=True)
        (OUT/'marker_results.json').write_text(json.dumps(records,indent=2))
    hidden=[]
    for name,original,n in [('opposite_xor3',parity_clause_block((1,2,3),0)+parity_clause_block((1,2,3),1),3),('tseitin_K4_odd',*tseitin_complete4(1)),('tseitin_K4_even',*tseitin_complete4(0))]:
        transformed,expanded=hide_clauses(original)
        for variant,cnf,dim in [('raw',original,n),('hidden',transformed,expanded)]:
            row={'family':name,'variant':variant,'n':dim,**measure(cnf,dim)}
            expected=sat_witness(original,n) is not None
            assert row['answer']==expected
            if dim<=12:assert row['answer']==(sat_witness(cnf,dim) is not None)
            if variant=='hidden':assert row['parity_blocks']==0
            hidden.append(row)
    (OUT/'hidden_parity_results.json').write_text(json.dumps(hidden,indent=2));print(json.dumps(hidden,indent=2))
if __name__=='__main__':main()
