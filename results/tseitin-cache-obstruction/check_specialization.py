import probe,itertools,random,json
rng=random.Random(4471);count=0
for n in range(1,7):
 for trial in range(300):
    f=[]
    for _ in range(rng.randrange(15)):
        vs=rng.sample(range(1,n+1),rng.randrange(min(3,n)+1))
        f.append(tuple(v*rng.choice((-1,1)) for v in vs))
    oracle=any(all(any(x[abs(a)-1]==(a>0) for a in c) for c in f) for x in itertools.product((False,True),repeat=n))
    assert probe.run(f,False)['sat']==oracle
    assert probe.run(f,True)['sat']==oracle
    count+=1
# Split gadget projects pointwise, for every assignment to its three literals.
gadgets=0
for a,b,c in itertools.product((False,True),repeat=3):
    assert any((a or b or y) and ((not y) or c) for y in (False,True))==(a or b or c)
    gadgets+=1
probe.emit('specialization_results.json', {'random_original_cnf_oracle_cases':count,'both_scc_modes_checked':True,'gadget_projection_cases':gadgets})
