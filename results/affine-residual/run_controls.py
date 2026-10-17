"""Reproduce parity and counterexample-repair controls; no external dependencies."""
import json
from pathlib import Path
from dataclasses import asdict
from arb import solve, ordinary_normalize
from families import cubic_tseitin, hide_cubic_clauses, selector_stars


def pure_literal_reduce(cnf):
    cs = ordinary_normalize(cnf)
    while True:
        literals = {lit for c in cs for lit in c}
        pure = {lit for lit in literals if -lit not in literals}
        if not pure:
            return cs
        cs = tuple(c for c in cs if not any(lit in pure for lit in c))


def main():
    edges=[(i,j) for i in range(4) for j in range(i+1,4)]
    results=[]
    for odd in [False,True]:
        cnf,n=cubic_tseitin(edges,odd)
        for hidden in [False,True]:
            f,m=hide_cubic_clauses(cnf,n) if hidden else (cnf,n)
            answer,stats=solve(f,m)
            assert answer == (not odd)
            results.append({'graph':'K4','odd_charge':odd,'hidden':hidden,
                            'answer':answer,'n':m,'clauses':len(f),'stats':asdict(stats)})
    Path(__file__).with_name('parity_controls.json').write_text(json.dumps(results,indent=2))
    repairs=[]
    for k in range(11):
        cnf,n=selector_stars(k)
        reduced=pure_literal_reduce(cnf)
        answer,stats=solve(reduced,n)
        assert answer is False and len(reduced)==22 and stats.unique_states==5
        repairs.append({'k':k,'clauses_after_pure_literal_reduction':len(reduced),
                        'answer':answer,'unique_states':stats.unique_states})
    Path(__file__).with_name('repair_controls.json').write_text(json.dumps(repairs,indent=2))
    print('Passed 4 parity controls and 11 pure-literal repair controls.')

if __name__=='__main__':
    main()
