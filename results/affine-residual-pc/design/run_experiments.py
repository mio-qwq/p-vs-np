"""Reproduce repaired and connected-marker family experiments."""
import json,time
from pathlib import Path
from dataclasses import asdict
from arb_pc import solve, ordinary_normalize
from families import selector_stars, connected_markers, pigeonhole


def collapse_family_cycles(k):
    """Explicit verified identity for the known family, not a general SCC solver.

    Selector implication cycles force u_i=v_i=x_i. Marker implication cycles
    force a_i=b_i=h. Substitute precisely these identities in original CNF.
    """
    cnf,n=connected_markers(k)
    h=3*k+1
    mapping={v:v for v in range(1,n+1)}
    for i in range(1,k+1):
        mapping[k+2*i-1]=i
        mapping[k+2*i]=i
        mapping[3*k+12+2*i-1]=h
        mapping[3*k+12+2*i]=h
    return ordinary_normalize(tuple(tuple(mapping[abs(lit)] if lit>0 else -mapping[abs(lit)]
                                           for lit in c) for c in cnf)),n


def main():
    results=[]
    repairs=[]
    for k in range(13):
        cnf,n=connected_markers(k)
        start=time.perf_counter()
        answer,stats=solve(cnf,n)
        assert not answer and stats.unique_states>=2**k
        row={'k':k,'n':n,'clauses':len(cnf),'literal_occurrences':sum(map(len,cnf)),
             'answer':answer,'elapsed_seconds':time.perf_counter()-start,**asdict(stats)}
        results.append(row)
        print(json.dumps(row),flush=True)
        old,m=selector_stars(k)
        old_answer,old_stats=solve(old,m)
        collapsed,m=collapse_family_cycles(k)
        collapsed_answer,collapsed_stats=solve(collapsed,m)
        assert not old_answer and not collapsed_answer
        assert old_stats.unique_states==collapsed_stats.unique_states==3
        repairs.append({'k':k,'old_star_states':old_stats.unique_states,
                        'cycle_collapsed_states':collapsed_stats.unique_states})
    Path(__file__).with_name('growth_results.json').write_text(json.dumps(results,indent=2))
    Path(__file__).with_name('repair_controls.json').write_text(json.dumps(repairs,indent=2))

if __name__=='__main__':
    main()
