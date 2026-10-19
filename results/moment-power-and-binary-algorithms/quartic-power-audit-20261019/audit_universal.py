#!/usr/bin/env python3
"""Independently reproduce the other worker's universal separator certificate.
Uses this directory's independently derived coefficient formulas/checker.
"""
from check import *
r=s.factor((n+53)/(n+50)*y0)
D=s.factor(k*k*(f*y+g)-y*y*(k*k-e*y))
universal={}
expressions={'k²-e*r':k*k-e*r,'3ef-k²':3*e*f-k*k,'-D(r)':-D.subs(y,r)}
expressions.update({f'R coefficient u^{q}':s.diff(R,y,q).subs(y,r)/s.factorial(q) for q in range(3)})
expressions.update({f'T coefficient u^{q}':s.diff(T,y,q).subs(y,r)/s.factorial(q) for q in range(5)})
for label,expr in expressions.items():
    universal[label]=positive_rational(expr,label,2)
    print(label,'PASS',len(universal[label]['shifted_numerator_coefficients_descending'])-1)
equal(s.diff(D,y),3*e*y*y-2*k*k*y+k*k*f,'D derivative')
equal(s.discriminant(s.diff(D,y),y),4*k*k*(k*k-3*e*f),'D derivative discriminant')
Path(__file__).with_name('universal_audit_certificate.json').write_text(json.dumps(universal,indent=2)+'\n')
print('PASS: all eleven universal certificates independently reconstructed.')
