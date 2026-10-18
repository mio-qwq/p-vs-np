#!/usr/bin/env python3
"""Recheck prior C6-C9 with the independent falling-factorial/Schur method."""
import contextlib,io,json
from pathlib import Path
import sympy as S
import itertools
with contextlib.redirect_stdout(io.StringIO()):
    from audit_c12 import falling_schur,schur,evaluate
ROOT=Path(__file__).parent
d,R,B,T,E1,E2,E3,E4=S.symbols('d R B T E1 E2 E3 E4')
checks=[]
def equal(label,a,b):
    residual=S.factor(a-b)
    if residual!=0: raise ValueError(f'{label}: {residual}')
    checks.append(label)
def coefficient(k):
    answer=0
    eoffset=(E1,E2,E3,E4)
    ed=(d+R,d*R+B,d*B+T,d*T)
    e0=(R,B,T,0)
    vratio=T-d*B+d*d*R-d**3
    for ks in itertools.combinations(range(k-2),4):
        if sum(ks)!=k: continue
        g=falling_schur(ks)
        answer+=schur(ks,eoffset)*(vratio*evaluate(g,ed)-T*evaluate(g,e0))
    return S.expand(answer)
cs={k:coefficient(k) for k in range(6,10)}
equal('C6 general',cs[6],-d*(d*d-d*R+B)/12)
equal('C7 after C6',cs[7].subs(B,d*R-d*d),E1*T*d/48)
equal('C8 after C6,C7',cs[8].subs(B,d*R-d*d).subs(E1,0),E2*T*d*(2*R-3*d+15)/720)
equal('C9 after C6,C7,C8',cs[9].subs(B,d*R-d*d).subs({E1:0,R:(3*d-15)/2}),-E3*T*d*(d*d+95)/1920)
receipt={'status':'PASS','checks':checks,'method':'double Cauchy-Binet and Schur expansion','general_coefficients':{f'C{k}':str(v) for k,v in cs.items()}}
(ROOT/'reduction_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('PASS:',len(checks),'reduction checks')
for label in checks: print(label)
