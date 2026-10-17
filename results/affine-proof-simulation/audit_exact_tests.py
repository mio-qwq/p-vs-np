"""Independent finite semantic checks, NOT an EF/SF proof verifier."""
import importlib.util, inspect, random, itertools, hashlib, json
from pathlib import Path
BASE=Path(__file__).resolve().parent
SRC=BASE.parent/'affine-residual-pc/design/arb_pc.py'
assert hashlib.sha256(SRC.read_bytes()).hexdigest()=='32ba57a17c8af1fc1045314fd89b849743bd6ba810fdfdb96f3a4ac9cde577c5'
spec=importlib.util.spec_from_file_location('audit_arb',SRC)
m=importlib.util.module_from_spec(spec); exec(compile(SRC.read_bytes(),str(SRC),'exec'),m.__dict__)
# Instrument only the dense return to expose precisely its inherited coordinates.
ns=dict(m.__dict__); ns['TRACE']=[]
s=inspect.getsource(m.normalize_base).replace('return len(columns), key_clauses','TRACE.append(tuple(columns))\n        return len(columns), key_clauses')
exec(s,ns); exec(inspect.getsource(m.normalize),ns)
def val(cs,a):
    return all(any(((mask&a).bit_count()%2)^c for mask,c in clause) for clause in cs)
def eqval(es,a):
    return all((mask&a).bit_count()%2==b for mask,b in es)
rng=random.Random(20261017); samples=0; assignment_checks=0; nonterminal=0; false=0; pure_checks=0
for n in range(7):
  for _ in range(600):
    cs=tuple(tuple((rng.randrange(1<<n),rng.randrange(2)) for _ in range(rng.randrange(4))) for _ in range(rng.randrange(9)))
    es=tuple((rng.randrange(1<<n),rng.randrange(2)) for _ in range(rng.randrange(4)))
    ns['TRACE'].clear(); k=ns['normalize'](cs,n,es)
    assert k==m.normalize(cs,n,es)
    mapping=list(range(n))
    for cols in ns['TRACE']: mapping=[mapping[i] for i in cols]
    assert len(set(mapping))==len(mapping)
    samples+=1
    if k is False: false+=1
    elif k is not True:
      nonterminal+=1; assert len(mapping)==k[0]
    for a in range(1<<n):
      if val(cs,a) and eqval(es,a):
        assignment_checks+=1
        assert k is not False
        if k is not True:
          projected=sum(((a>>i)&1)<<j for j,i in enumerate(mapping))
          assert val(k[1],projected)
    base=m.normalize_base(cs,n,es)
    if base is True or base is False: continue
    dim,clauses=base; signs={}; forbidden=0
    for clause in clauses:
      for mask,c in clause:
        if mask.bit_count()!=1: forbidden|=mask
        else: signs.setdefault(mask,set()).add(c)
    pure=tuple((mask,next(iter(v))^1) for mask,v in signs.items() if len(v)==1 and not(mask&forbidden))
    if pure:
      drop={mask for mask,b in pure}
      remaining=tuple(c for c in clauses if not any(mask in drop for mask,b in c))
      assert m.normalize_base(clauses,dim,pure)==m.normalize_base(remaining,dim)
      pure_checks+=1
# Exact long-chain witnesses, all assignments and all polarity vectors through r=8.
chain_checks=0
for r in range(4,9):
  for signs in itertools.product((-1,1),repeat=r):
    clause=tuple(signs[i]*(i+1) for i in range(r))
    ordered=m.ordinary_normalize((clause,))[0]
    expanded,dim=m.to_3cnf((clause,),r)
    for a in range(1<<r):
      truths=[bool((a>>(abs(lit)-1))&1)==(lit>0) for lit in ordered]
      w=a
      for j in range(r-3):
        if not any(truths[:j+2]): w|=1<<(r+j)
      out=all(any(bool((w>>(abs(l)-1))&1)==(l>0) for l in c) for c in expanded)
      assert out==any(truths)
      chain_checks+=1
result={'status':'PASS','normalization_samples':samples,'satisfying_assignment_projection_checks':assignment_checks,'nonterminal_results':nonterminal,'false_results':false,'pure_deletion_comparisons':pure_checks,'chain_witness_checks':chain_checks,'solver_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),'test_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Finite semantic regression only; not a proof-system proof checker or proof of universal simulation.'}
(BASE/'audit_exact_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
