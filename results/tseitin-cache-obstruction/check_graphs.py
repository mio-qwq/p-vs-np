import probe, random,json
rng=random.Random(20261017)
def cubic(n):
    cycle={tuple(sorted((i,(i+1)%n))) for i in range(n)}
    while True:
        a=list(range(n));rng.shuffle(a);match={tuple(sorted(a[i:i+2])) for i in range(0,n,2)}
        if not(cycle&match):return sorted(cycle|match)
rows=[];bad=None
for n in (6,8,10,12,14,16):
 for seed in range(8):
    edges=cubic(n); probe.graph=lambda r,e=edges:e
    f,nv,base=probe.family(n//2)
    res=probe.run(f,True)
    rows.append({'vertices':n,'sample':seed,'edges':edges,**res})
    if res['namespace_changed_hits'] and bad is None:bad=rows[-1]
probe.emit('graph_results.json', {'runs':rows,'first_changed_namespace':bad})
