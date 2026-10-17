import sys,json,random,time,types
from dataclasses import asdict
from itertools import product,combinations
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'design'))
import arb_pc as arb
from exact_oracle import sat_witness,canonical_formulas
from test_families import parity_clause_block,hide_clauses,tseitin_complete4,xor_chain,pigeonhole
OUT=Path(__file__).resolve().parent

def ordinary_value(cnf,assignment):
    return all(any(bool(assignment>>(abs(l)-1)&1)==(l>0) for l in c) for c in cnf)
def affine_value(cs,eq,a):
    return all((a&m).bit_count()%2==b for m,b in eq) and all(any(((a&m).bit_count()%2)^b for m,b in c) for c in cs)
def affine_sat(cs,eq,n):return any(affine_value(cs,eq,a) for a in range(1<<n))
def normalized_sat(result):
    if type(result) is bool:return result
    n,cs=result;return affine_sat(cs,(),n)

def run():
    rng=random.Random(11072026);summary={};start=time.time();count=0
    for n,m in [(0,None),(1,None),(2,None),(3,4)]:
        for cs in canonical_formulas(n,m):
            expected=sat_witness(cs,n) is not None
            actual,_=arb.solve(cs,n)
            assert actual==expected,('canonical',cs,n,actual,expected)
            count+=1
    summary['canonical_solver_cases']=count
    count=0
    for n in range(1,9):
        for _ in range(250):
            cs=[tuple(rng.choice((-1,1))*rng.randint(1,n) for _ in range(rng.randint(0,7))) for _ in range(rng.randint(0,28))]
            assert arb.solve(cs,n)[0]==(sat_witness(cs,n) is not None),('random',cs,n)
            count+=1
    summary['random_solver_cases']=count
    # Pointwise extraction equivalence, including incomplete and overlapping blocks.
    count=0
    full=parity_clause_block((1,2,3),0)+parity_clause_block((1,2,3),1)
    extraction_cases=[([full[i] for i in range(8) if subset>>i&1],3) for subset in range(256)]
    for _ in range(300):
        cs=[tuple(rng.choice((-1,1))*v for v in rng.sample(range(1,6),rng.randint(0,3))) for _ in range(rng.randint(0,20))]
        extraction_cases.append((cs,5))
    for cs,n in extraction_cases:
        norm=arb.ordinary_normalize(cs);ac,eq,blocks=arb.extract_parity(norm)
        for a in range(1<<n):assert ordinary_value(cs,a)==affine_value(ac,eq,a),('extraction',cs,ac,eq,a)
        count+=1
    summary['pointwise_extraction_formulas']=count
    # Gaussian substitution and unit-saturation checked against original affine semantics.
    count=0
    for n in range(0,7):
        for _ in range(400):
            cs=tuple(tuple((rng.randrange(1<<n),rng.randrange(2)) for _ in range(rng.randrange(5))) for _ in range(rng.randrange(10)))
            eq=tuple((rng.randrange(1<<n),rng.randrange(2)) for _ in range(rng.randrange(5)))
            result=arb.normalize(cs,n,eq)
            assert normalized_sat(result)==affine_sat(cs,eq,n),('affine_normalize',n,cs,eq,result)
            count+=1
    summary['affine_normalization_cases']=count
    # Exact existential projection for conversion, each original assignment separately.
    count=0;assignments=0
    for n in (4,5,6):
        for _ in range(60):
            cs=[tuple(rng.choice((-1,1))*v for v in rng.sample(range(1,n+1),rng.randint(2,n))) for _ in range(rng.randint(1,3))]
            converted,expanded=arb.to_3cnf(cs,n)
            for a in range(1<<n):
                projected=any(ordinary_value(converted,a|(ext<<n)) for ext in range(1<<(expanded-n)))
                assert projected==ordinary_value(cs,a),('conversion',cs,n,a,converted)
                assignments+=1
            count+=1
    summary['conversion_formulas']=count;summary['conversion_assignments']=assignments
    # Semantic edge cases and API validation.
    invalid=[(((0,),),None),(((2,),),1),((),-1)]
    for cs,n in invalid:
        try:arb.solve(cs,n)
        except ValueError:pass
        else:raise AssertionError(('invalid accepted',cs,n))
    summary['invalid_inputs_rejected']=len(invalid)
    # Deliberately introduce real implementation bugs; harness must detect them.
    source=Path(arb.__file__).read_text();negative=[]
    changes=[('wrong_chain_sign','out.append((-y, c[-2], c[-1]))','out.append((y, c[-2], c[-1]))',[(1,2,3,4),(-1,),(-2,),(-3,),(-4,)],4),
             ('wrong_parity_rhs','equations.append((sum(1 << (v-1) for v in support), rhs))','equations.append((sum(1 << (v-1) for v in support), rhs ^ 1))',parity_clause_block((1,2),0)+[(1,),(2,)],2)]
    for name,old,new,cs,n in changes:
        assert old in source
        module=types.ModuleType('mutant_'+name);sys.modules[module.__name__]=module
        exec(compile(source.replace(old,new),module.__name__,'exec'),module.__dict__)
        expected=sat_witness(cs,n) is not None;got=module.solve(cs,n)[0]
        assert got!=expected,('mutant not caught',name)
        negative.append({'name':name,'cnf':cs,'n':n,'expected':expected,'mutant':got})
    # Direct affine mutation control for incorrect Gaussian constant substitution.
    name='wrong_gaussian_constant';module=types.ModuleType('mutant_'+name);sys.modules[module.__name__]=module
    exec(compile(source.replace('const ^= b','const ^= 0'),module.__name__,'exec'),module.__dict__)
    cs=(((1,0),),);eq=((1,1),)
    expected=affine_sat(cs,eq,1);got=normalized_sat(module.normalize(cs,1,eq))
    assert expected!=got
    negative.append({'name':name,'affine_clauses':cs,'equations':eq,'expected':expected,'mutant':got})
    summary['negative_controls']=negative
    summary['elapsed_seconds']=time.time()-start
    (OUT/'correctness_results.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary,indent=2),flush=True)
if __name__=='__main__':run()
