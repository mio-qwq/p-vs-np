#!/usr/bin/env python3
"""Compare every printed primitive quadratic/discriminant bound with recomputation."""
import re,json,math
from pathlib import Path
import sympy as S
ROOT=Path(__file__).parent
source=ROOT.parent/'five-row-c12-20261018'/'PROOF.md'
d,T=S.symbols('d T')
pair=S.sympify(json.loads((ROOT/'audit_receipt.json').read_text())['pair_half_resultant'])
comp=S.sympify(json.loads((ROOT/'complement_receipt.json').read_text())['half_resultant'])
rows=re.findall(r'\| (\d+) \| `([^`]+)` \| (-?\d+) \| (\w+) \|',source.read_text())
if len(rows)!=18: raise ValueError(f'Expected 18 table rows, found {len(rows)}')
checked=[]
for i,(dd,polytext,delta_text,ntext) in enumerate(rows):
    dd=int(dd); expr=re.sub(r'(?<=\d)(?=T)','*',polytext.replace('²','**2'))
    actual=S.sympify(expr)
    expected=S.Poly((pair if i<6 else comp).subs(d,dd),T).primitive()[1]
    if expected.LC()<0: expected=-expected
    if S.expand(actual-expected.as_expr())!=0: raise ValueError(f'Bad table polynomial: {i}, {dd}')
    delta=int(S.discriminant(actual,T))
    if delta!=int(delta_text): raise ValueError(f'Bad table discriminant: {i}, {dd}')
    if delta<0:
        if ntext!='negative': raise ValueError('Wrong negative label')
    elif not (int(ntext)==math.isqrt(delta) and int(ntext)**2<delta<(int(ntext)+1)**2):
        raise ValueError(f'Bad table square bound: {i}, {dd}')
    checked.append({'branch':'pair' if i<6 else 'complement','d':dd})
(ROOT/'final_table_receipt.json').write_text(json.dumps({'status':'PASS','rows':checked},indent=2)+'\n')
print('PASS: all 18 printed primitive quadratic, discriminant, and consecutive-square rows')
