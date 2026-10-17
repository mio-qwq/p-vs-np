import sys,json,types,random,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'design'))
import arb_pc as arb
from check_arb_pc import affine_sat,normalized_sat
from test_families import pigeonhole
ROOT=Path(__file__).resolve().parent

def mutant(name,old,new):
    source=Path(arb.__file__).read_text();assert old in source
    mod=types.ModuleType('mutant_'+name);sys.modules[mod.__name__]=mod
    exec(compile(source.replace(old,new),mod.__name__,'exec'),mod.__dict__)
    return mod

def main():
    rng=random.Random(24007);count=0;split_count=0
    for n in range(2,7):
        for _ in range(600):
            cs=tuple(tuple((rng.randrange(1,1<<n),rng.randrange(2)) for _ in range(rng.randrange(2,4))) for _ in range(rng.randrange(2,12)))
            expected=affine_sat(cs,(),n);key=arb.normalize(cs,n)
            assert normalized_sat(key)==expected,('purity',cs,n,key)
            if type(key) is not bool:
                parts=arb.split_components(key)
                assert all(normalized_sat(p) for p in parts)==expected,('decomposition',cs,n,key,parts)
                split_count+=len(parts)>1
            count+=1
    disjoint_cases=0
    for _ in range(500):
        cs=[]
        for shift in (0,3):
            cs.extend(tuple((rng.randrange(1,8)<<shift,rng.randrange(2)) for _ in range(2)) for _ in range(rng.randrange(2,8)))
        key=(6,tuple(cs));parts=arb.split_components(key)
        assert len(parts)>=2
        assert all(normalized_sat(p) for p in parts)==affine_sat(cs,(),6)
        disjoint_cases+=1
    # Specific mixed-coordinate purity counterexample for an unsafe implementation.
    cs=(((3,0),(4,0)),((3,0),(4,1)),((2,0),(8,0)),((2,0),(8,1)),((1,0),(16,0)))
    assert affine_sat(cs,(),5) and normalized_sat(arb.normalize(cs,5))
    broken=mutant('ignore_affine_dependencies','and not (mask & forbidden)','and True')
    assert normalized_sat(broken.normalize(cs,5)) is False
    # Independent SAT and UNSAT components must combine by AND, not OR.
    sat_cycle=[(-1,2),(-2,3),(-3,1)]
    php,n=pigeonhole(3)
    disjoint=sat_cycle+[tuple((abs(l)+3)*(1 if l>0 else -1) for l in c) for c in php]
    answer,stats=arb.solve(disjoint,15);assert answer is False and stats.component_splits>=1
    broken_and=mutant('components_as_or',"mode = 'and'","mode = 'or'")
    assert broken_and.solve(disjoint,15)[0] is True
    # Disjoint satisfiable nonpure components and two unsatisfiable components.
    sat2=sat_cycle+[tuple((abs(l)+3)*(1 if l>0 else -1) for l in c) for c in sat_cycle]
    assert arb.solve(sat2,6)[0] is True
    unsat2=php+[tuple((abs(l)+12)*(1 if l>0 else -1) for l in c) for c in php]
    assert arb.solve(unsat2,24)[0] is False
    out={'targeted_affine_cases':count,'deliberately_disjoint_affine_cases':disjoint_cases,'random_cases_with_multiple_components':split_count,
         'mixed_affine_purity_negative_control':{'clauses':cs,'n':5,'expected':True,'unsafe_mutant':False},
         'component_and_negative_control':{'cnf':disjoint,'n':15,'expected':False,'or_mutant':True},
         'additional_component_combinations':['SAT AND SAT -> SAT','UNSAT AND UNSAT -> UNSAT'],
         'candidate_sha256':hashlib.sha256(Path(arb.__file__).read_bytes()).hexdigest()}
    (ROOT/'repair_results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
if __name__=='__main__':main()
