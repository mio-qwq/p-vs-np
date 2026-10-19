#!/usr/bin/env python3
"""Persist an exact middle-fiber polynomial for the four-top-cancellation case."""
import hashlib
import json
from pathlib import Path
from audit_checker import evaluate

P,F,T,D,v=evaluate([0,2,4,14,15],[0,7,10,17,22],0,3,2)
S=F-P
coefficients=[str(P.nth(j)) for j in range(P.degree()+1)]
canonical=','.join(coefficients).encode('ascii')
certificate={
    'offsets':[0,2,4,14,15],
    'exponents':[0,7,10,17,22],
    'zero_rows':[0,3],
    'zero_column':2,
    'indices_are_zero_based':True,
    'main_D':D,
    'middle_degree':P.degree(),
    'middle_leading_coefficient':str(P.LC()),
    'full_determinant_degree':F.degree(),
    'full_determinant_leading_coefficient':str(F.LC()),
    'deleted_contribution_degree':S.degree(),
    'deleted_contribution_leading_coefficient':str(S.LC()),
    'deleted_contribution_coefficients_D_through_D_minus_3':[str(S.nth(j)) for j in range(D,D-4,-1)],
    'middle_coefficients_ascending':coefficients,
    'middle_coefficient_sha256':hashlib.sha256(canonical).hexdigest(),
    'hash_encoding':'ASCII comma-separated ascending integer coefficients, no spaces or newline'
}
path=Path(__file__).with_name('residual_stress_test.json')
path.write_text(json.dumps(certificate,indent=2)+'\n')
print(path)
print(certificate['middle_coefficient_sha256'])
