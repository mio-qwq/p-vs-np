import importlib.util,sys,json,itertools,hashlib,os
from pathlib import Path
HERE = Path(__file__).resolve().parent
EXPECTED_SOLVER_SHA256 = '32ba57a17c8af1fc1045314fd89b849743bd6ba810fdfdb96f3a4ac9cde577c5'
P = Path(os.environ.get('ARB_PC_SOURCE', str(HERE.parent / 'affine-residual-pc' / 'design' / 'arb_pc.py'))).resolve()
source = P.read_bytes()
actual_sha256 = hashlib.sha256(source).hexdigest()
if actual_sha256 != EXPECTED_SOLVER_SHA256:
    raise RuntimeError('Frozen solver SHA256 mismatch: refusing to execute source')

def emit(name, value):
    text = json.dumps(value, indent=2) + '\n'
    (HERE / name).write_text(text)
    print(text, end='')

spec=importlib.util.spec_from_file_location('arb',P);arb=importlib.util.module_from_spec(spec);sys.modules['arb']=arb;exec(compile(source,str(P),'exec'),arb.__dict__)
def graph(r):
    return sorted({tuple(sorted(e)) for i in range(r) for e in [(i,(i+1)%r),(r+i,r+(i+1)%r),(i,r+i)]})
def family(r):
    edges=graph(r); base=[]
    for v in range(2*r):
        inc=[i+1 for i,e in enumerate(edges) if v in e]
        assert len(inc)==3
        for bits in itertools.product((0,1),repeat=3):
            if sum(bits)%2 != (v==0):
                base.append(tuple(-a if b else a for a,b in zip(inc,bits)))
    f=[];n=len(edges)
    for a,b,c in base:
        n+=1;f.extend([(a,b,n),(-n,c)])
    return f,n,base

def scc_map(cs):
    vs={abs(a) for c in cs for a in c};nodes=sorted(vs|{-a for a in vs});adj={a:[] for a in nodes}
    for c in cs:
        if len(c)==2:
            a,b=c;adj[-a].append(b);adj[-b].append(a)
    # Reachability is deliberately simple, polynomial, and independent of Tarjan.
    reach={}
    for a in nodes:
        seen={a}; todo=[a]
        while todo:
            for b in adj[todo.pop()]:
                if b not in seen:seen.add(b);todo.append(b)
        reach[a]=seen
    if any(-a in reach[a] and a in reach[-a] for a in vs):return None
    mp={}
    for a in nodes:
        equiv=[b for b in reach[a] if a in reach[b]]
        rep=min(equiv,key=lambda x:abs(x));mp[a]=rep
    return mp

def norm(cs,scc=False):
    cs={frozenset(c) for c in cs if not any(-a in c for a in c)}
    while True:
        if frozenset() in cs:return False
        if not cs:return True
        units={next(iter(c)) for c in cs if len(c)==1}
        if any(-a in units for a in units):return False
        if units:
            cs={frozenset(a for a in c if -a not in units) for c in cs if not(c&units)};continue
        cs={c for c in cs if not any(d<c for d in cs)}
        occ=set().union(*cs);pure={a for a in occ if -a not in occ}
        if pure:cs={c for c in cs if not(c&pure)};continue
        if scc:
            mp=scc_map(cs)
            if mp is None:return False
            if any(mp[a]!=a for a in mp):
                cs={frozenset(mp[a] for a in c) for c in cs}
                cs={c for c in cs if not any(-a in c for a in c)};continue
        return cs

def canonical(cs):
    names=sorted({abs(a) for c in cs for a in c});ids={a:i for i,a in enumerate(names)}
    key=(len(names),tuple(sorted((tuple(sorted((1<<ids[abs(a)],int(a<0)) for a in c)) for c in cs),key=lambda c:(len(c),c))))
    return key,names

def comps(cs):
    vs={abs(a) for c in cs for a in c}; adj={a:set() for a in vs}
    for c in cs:
        s={abs(a) for a in c}
        for a in s:adj[a]|=s
    out=[]
    while vs:
        seen={min(vs)};todo=list(seen)
        while todo:
            for a in adj[todo.pop()]:
                if a not in seen:seen.add(a);todo.append(a)
        vs-=seen;out.append({c for c in cs if abs(next(iter(c))) in seen})
    return sorted(out,key=lambda cs:(canonical(cs)[0][0],len(cs),canonical(cs)[0]))

def run(f,scc):
    cache={};witness=None;first_hit=None;hits=changed=branches=0
    def dfs(cs,path):
        nonlocal witness,first_hit,hits,changed,branches
        cs=norm(cs,scc)
        if isinstance(cs,bool):return cs
        key,names=canonical(cs)
        if key in cache:
            result,oldnames,oldpath,oldcs=cache[key];hits+=1
            if first_hit is None:
                first_hit={"first_path":oldpath,"second_path":path,"same_interface":names==oldnames,"first_context_clause":[-a for a in oldpath],"first_context_clause_already_true_on_second":any(-a in path for a in oldpath)}
            if names!=oldnames:
                changed+=1
                if witness is None:witness={'first_path':oldpath,'second_path':path,'first_names':oldnames,'second_names':names,'canonical_key':key,'first_original_clauses':[sorted(c) for c in sorted(oldcs,key=lambda c:sorted(c))],'second_original_clauses':[sorted(c) for c in sorted(cs,key=lambda c:sorted(c))]}
            return result
        parts=comps(cs)
        if len(parts)>1:result=all(dfs(p,path) for p in parts)
        else:
            branches+=1;mask,const=key[1][0][0];a=names[mask.bit_length()-1]
            result=False
            for b in (0,1):
                lit=a if b^const else -a
                if dfs(cs|{frozenset([lit])},path+[lit]):result=True;break
        cache[key]=(result,names,path,cs);return result
    result=dfs(f,[])
    return {'sat':result,'states':len(cache),'cache_hits':hits,'namespace_changed_hits':changed,'branches':branches,'witness':witness,'first_hit':first_hit}
if __name__=='__main__':
    out=[]
    for r in range(3,9):
        f,n,base=family(r);aff,eq,blocks=arb.extract_parity(arb.ordinary_normalize(f));assert blocks==0
        mp=scc_map(f);assert mp and all(a==b for a,b in mp.items());assert norm(f,True)=={frozenset(c) for c in f};assert len(comps(norm(f,True)))==1
        x=run(f,False);res,stats=arb.solve(f,n=n);assert res==x['sat']==False;assert stats.unique_states==x['states'];assert stats.cache_hits==x['cache_hits'];y=run(f,True);assert y['sat']==False
        # Every split clause projects to original C plus tautology under y_C:=c.
        for j,c in enumerate(base):
            yvar=len(graph(r))+j+1;mp={yvar:c[2],-yvar:-c[2]}
            image=[frozenset(mp.get(a,a) for a in d) for d in f[2*j:2*j+2]]
            assert image[0]==frozenset(c);assert any(-a in image[1] for a in image[1])
        out.append({'prism_r':r,'vertices':2*r,'variables':n,'clauses':len(f),'initial_blocks':blocks,'original':x,'with_scc':y})
    emit('results.json', {'solver_sha256':actual_sha256,'runs':out})
