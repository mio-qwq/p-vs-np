"""Independent connected/nonpure cycle-gated candidate obstruction."""
from test_families import pigeonhole

def connected_cycles(k):
    # x first, selector u/v next, fixed PHP core, marker a/b last.
    core_offset=3*k
    core,_=pigeonhole(3)
    cnf=[tuple((abs(l)+core_offset)*(1 if l>0 else -1) for l in c) for c in core]
    h=core_offset+1
    for i in range(k):
        x=i+1;u=k+2*i+1;v=k+2*i+2
        a=core_offset+12+2*i+1;b=a+1
        cnf.extend([(-x,u),(-u,v),(-v,x),(-h,a),(-a,b),(-b,h),(x,a,b)])
    return cnf,5*k+12

def graph_components(cnf):
    vars={abs(l) for c in cnf for l in c};adj={v:set() for v in vars}
    for c in cnf:
        support={abs(l) for l in c}
        for v in support:adj[v]|=support-{v}
    result=[]
    while vars:
        start=min(vars);todo=[start];component=set()
        while todo:
            v=todo.pop()
            if v in component:continue
            component.add(v);todo.extend(adj[v]-component)
        vars-=component;result.append(component)
    return result

def pure_literals(cnf):
    literals={l for c in cnf for l in c}
    return sorted(l for l in literals if -l not in literals)
