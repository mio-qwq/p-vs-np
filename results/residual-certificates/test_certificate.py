"""Independent truth-table semantics, replay comparisons and adversarial checks."""
import copy
import itertools
import json
from pathlib import Path
import random
import residual_certificate as rc

rng = random.Random(20261017)
counts = {'cnfs': 0, 'sat': 0, 'unsat': 0, 'affine_semantics': 0, 'corruptions_rejected': 0}

def brute(cnf):
    # Direct dictionaries: no frozen preprocessing, masks or normalization.
    names = sorted({abs(x) for c in cnf for x in c})
    for bits in itertools.product((False, True), repeat=len(names)):
        assignment = dict(zip(names, bits))
        if all(any(assignment[abs(x)] == (x > 0) for x in c) for c in cnf):
            return True
    return False

def test(cnf, n=None):
    expected = brute(cnf)
    cert = rc.generate(cnf, n)
    actual, stats = rc.frozen.solve(cnf, n)
    assert actual == expected
    assert (cert is None) == expected
    if cert is not None:
        assert rc.verify(cnf, json.loads(json.dumps(cert)), n)
    counts['cnfs'] += 1
    counts['sat' if expected else 'unsat'] += 1
    return cert, stats

def H(start):
    a, b = start, start + 1
    result = []
    for z, (r, s) in enumerate([(a,b), (a,-b), (-a,b), (-a,-b)], start + 2):
        result.extend([(r,z),(-z,s)])
    return result

# Exhaustive every formula subset on two variables, including the empty clause.
clauses = []
for signs in itertools.product((0,1,-1), repeat=2):
    clauses.append(tuple((i+1)*s for i,s in enumerate(signs) if s))
for subset in range(1 << len(clauses)):
    test([c for i,c in enumerate(clauses) if (subset >> i) & 1])
# All combinations of at most three nonempty width <= 2 clauses on three vars.
clauses = [tuple((i+1)*s for i,s in enumerate(signs) if s)
           for signs in itertools.product((0,1,-1), repeat=3) if 1 <= sum(s != 0 for s in signs) <= 2]
for size in range(4):
    for cnf in itertools.combinations(clauses, size): test(cnf)
for _ in range(1600):
    n = rng.randrange(1,8)
    cnf = [tuple(rng.choice((-1,1))*rng.randrange(1,n+1) for _ in range(rng.randrange(1,8)))
           for _ in range(rng.randrange(0,38))]
    test(cnf)

shared = [(1,)+c for c in H(2)] + [(-1,)+c for c in H(8)]
shared_cert, stats = test(shared)
assert len(shared_cert['nodes']) == 2 and stats.cache_hits == 1
root = shared_cert['nodes'][shared_cert['root']]
assert root['children'][0] == root['children'][1]
component = H(1) + H(7)
component_cert, stats = test(component)
assert component_cert['nodes'][component_cert['root']]['kind'] == 'component'
# SAT component before UNSAT component (also checks pruning unused proof nodes).
test([(20,21),(-20,-21)] + H(1))
# Sparse labels must not become mask indices, even with enormous declared n.
big = 10**1000
sparse = [[(big+abs(x)*17) * (1 if x>0 else -1) for x in c] for c in shared]
sparse_cert, _ = test(sparse, big+100000)
assert sparse_cert == shared_cert
# Long-clause expansion, parity blocks, units, empty formula/clause, safe purity.
for cnf in [[],[[]],[[1],[-1]],[[1,2],[-1,-2]],
            [[1,2,3,4,5,6]] + [[-i] for i in range(1,7)],
            [[1,2,3,4,5,6],[-1,2],[-2,3]],
            [[1,2],[1,-2]], [[1,-1]], [[1,1,2],[1,-2]], H(1)]:
    test(cnf)
terminal, _ = test([[]])
assert terminal['root'] is None and terminal['nodes'] == []

# Independent semantics of affine clauses/equations against normalized outputs.
def affine_sat(clauses, d, eq=()):
    for a in itertools.product((0,1), repeat=d):
        def val(m): return sum(a[i] for i in range(d) if (m >> i)&1) % 2
        if all(val(m) == b for m,b in eq) and all(any(val(m)^b for m,b in c) for c in clauses):
            return True
    return False
for _ in range(1200):
    d = rng.randrange(0,6)
    cs = [[(rng.randrange(1<<d),rng.randrange(2)) for _ in range(rng.randrange(5))]
          for _ in range(rng.randrange(10))]
    eq = [(rng.randrange(1<<d),rng.randrange(2)) for _ in range(rng.randrange(4))]
    key = rc.frozen.normalize(cs,d,eq)
    actual = key if key is True or key is False else affine_sat(key[1],key[0])
    assert actual == affine_sat(cs,d,eq)
    counts['affine_semantics'] += 1
# Explicit purity hazard: variable in singleton and multi-coordinate forms.
for cs in [[[(1,0),(3,0)],[(1,0),(3,1)],[(2,0),(1,1)]],
           [[(1,0),(2,0)],[(1,0),(2,1)]]]:
    key=rc.frozen.normalize(cs,2)
    actual=key if type(key) is bool else affine_sat(key[1],key[0])
    assert actual == affine_sat(cs,2)
    counts['affine_semantics'] += 1

def reject(cnf, cert, label):
    try: rc.verify(cnf,cert)
    except rc.InvalidCertificate: counts['corruptions_rejected'] += 1
    else: raise AssertionError('accepted corruption: ' + label)

def mutate(label, fn, cnf=shared, original=shared_cert):
    cert=copy.deepcopy(original)
    fn(cert)
    reject(cnf,cert,label)

mutate('wrong root',lambda c: c.update(root=0))
mutate('FALSE root',lambda c: c.update(root=None))
mutate('negative root',lambda c: c.update(root=-1))
mutate('bool root',lambda c: c.update(root=True))
mutate('large root',lambda c: c.update(root=10**100))
mutate('float root',lambda c: c.update(root=1.0))
mutate('string ref',lambda c: c['nodes'][-1].update(children=['0',0]))
mutate('bool ref',lambda c: c['nodes'][-1].update(children=[False,0]))
mutate('bad FALSE leaf',lambda c: c['nodes'][-1].update(children=[None,0]))
mutate('self cycle',lambda c: c['nodes'][-1].update(children=[1,0]))
mutate('two-node cycle',lambda c: c['nodes'][0].update(children=[1,None]))
for value in [-1, True, 10**1000, 1.0]:
    mutate('dimension type/bound',lambda c,v=value: c['nodes'][0].update(dimension=v))
for value in [-1, True, 1<<10000, 1.0]:
    mutate('mask type/bound',lambda c,v=value: c['nodes'][0]['clauses'][0][0].__setitem__(0,v))
for value in [-1, True, 2, 0.0]:
    mutate('constant type/bound',lambda c,v=value: c['nodes'][0]['clauses'][0][0].__setitem__(1,v))
mutate('noncanonical order',lambda c: c['nodes'][0]['clauses'].reverse())
mutate('empty residual',lambda c: c['nodes'][0].update(clauses=[]))
mutate('wrong query',lambda c: c['nodes'][-1].update(query=[2,0]))
mutate('zero query',lambda c: c['nodes'][-1].update(query=[0,0]))
mutate('branch arity',lambda c: c['nodes'][-1].update(children=[0]))
mutate('wrong solver',lambda c: c.update(solver_sha256='0'*64))
mutate('bool version',lambda c: c.update(version=True))
mutate('extra fields',lambda c: c.update(trust_me=True))
mutate('unreachable node',lambda c: c['nodes'].append(copy.deepcopy(c['nodes'][0])))
for value in [True,-1,999,1.0]:
    mutate('bad component index',lambda c,v=value: c['nodes'][-1].update(index=v),component,component_cert)
mutate('invalid component FALSE',lambda c: c['nodes'][-1].update(child=None),component,component_cert)
reject([[1]],terminal,'SAT with FALSE certificate')
reject([],terminal,'TRUE root')
# Validate bounds/ranks BEFORE any supplied-key normalization or splitting.
for label, change in [('huge dimension',lambda c:c['nodes'][0].update(dimension=10**1000)),
                      ('huge mask',lambda c:c['nodes'][0]['clauses'][0][0].__setitem__(0,1<<10000)),
                      ('cycle',lambda c:c['nodes'][-1].update(children=[1,0]))]:
    original_normalize=rc.frozen.normalize
    def fail(*a,**k): raise AssertionError('normalization called before structural validation')
    rc.frozen.normalize=fail
    try: mutate(label,change)
    finally: rc.frozen.normalize=original_normalize
for cnf in [[[True]], [[0]], [[1.0]], [["1"]]]:
    try: rc.generate(cnf)
    except rc.InvalidCertificate: counts['corruptions_rejected'] += 1
    else: raise AssertionError('invalid CNF accepted')

base=Path(__file__).parent
for name,cnf,cert in [('shared',shared,shared_cert),('component',component,component_cert),('terminal',[[]],terminal)]:
    (base/(name+'.input.json')).write_text(json.dumps({'clauses':cnf},sort_keys=True)+'\n')
    (base/(name+'.certificate.json')).write_text(json.dumps(cert,sort_keys=True)+'\n')
print(json.dumps({'counts':counts,'shared_nodes':len(shared_cert['nodes']),
                  'shared_root_children':root['children'],'solver_sha256':rc.FROZEN_SHA256},sort_keys=True))
