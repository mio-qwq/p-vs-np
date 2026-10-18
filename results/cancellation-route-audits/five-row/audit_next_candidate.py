#!/usr/bin/env python3
"""Direct polynomial determinant audit of the separate d=9 candidate."""
import json
from pathlib import Path
import sympy as S
x,v=S.symbols('x v')
e=[0,5,9,12,14]
rows=[[x**a if a in {5,14} else 0 for a in e]]
rows += [[(x+b)**a for a in e] for b in [-1,1,-v,v]]
p=S.Poly(S.expand(S.Matrix(rows).det(method='domain-ge')),x)
relation=209*v**4-1226*v*v+209
expected=90288*v**11-719280*v**9+628992*v**7+628992*v**5-719280*v**3+90288*v
remainder=v*(S.Rational(115205932800,43681)-S.Rational(137735637131520,9129329)*v*v)
if any(S.rem(c,relation,v)!=0 for (power,),c in p.terms() if power>28):
    raise ValueError('Earlier coefficient survived')
if S.expand(p.nth(28)-expected)!=0: raise ValueError('C12 mismatch')
if S.expand(S.rem(p.nth(28),relation,v)-remainder)!=0: raise ValueError('Remainder mismatch')
discriminant=1226**2-4*209**2
if not 1152**2 < discriminant < 1153**2: raise ValueError('Square interval')
receipt={'status':'PASS','method':'direct 5-by-5 polynomial determinant','sympy':S.__version__,'C12':str(p.nth(28)),'remainder':str(remainder),'discriminant':discriminant,'highest_degree':p.degree(),'earlier_coefficients_vanish_mod_relation':True}
Path(__file__).with_name('audit_next_candidate_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
