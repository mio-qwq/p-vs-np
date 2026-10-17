import probe,json
# GF(2) multilinear polynomials, represented by monomial-support masks.
def add(*ps):
    r=set()
    for p in ps:r.symmetric_difference_update(p)
    return r
def mul(a,b):
    r=set()
    for x in a:
        for y in b:r.symmetric_difference_update({x|y})
    return r
def false_literal(l):return {0,1<<(l-1)} if l>0 else {1<<(-l-1)}
def false_clause(c):
    p={0}
    for l in c:p=mul(p,false_literal(l))
    return p
count=0
for r in range(3,10):
 f,n,base=probe.family(r);derived=[]
 for j,(a,b,c) in enumerate(base):
    q1,q2=map(false_clause,f[2*j:2*j+2])
    term1=mul(false_literal(c),q1)
    term2=mul(mul(false_literal(a),false_literal(b)),q2)
    assert max(map(int.bit_count,term1|term2),default=0)<=4
    q=add(term1,term2);assert q==false_clause((a,b,c));derived.append(q);count+=1
 # Each consecutive four original clauses encode one vertex parity.
 vertex_equations=[]
 for v in range(2*r):
    e=add(*derived[4*v:4*v+4]);assert max(map(int.bit_count,e),default=0)<=1
    vertex_equations.append(e)
 assert add(*vertex_equations)=={0} # constant one, contradiction
probe.emit('pc_degree_results.json', {'split_clause_identities':count,'prism_vertices_checked':[6,8,10,12,14,16,18], 'largest_PC_degree_needed':4,'final_polynomial':'1'})
