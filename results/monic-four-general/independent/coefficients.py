import sympy as s
from itertools import permutations,product
from functools import lru_cache
p,q,r,b,c=s.symbols('p q r b c')
E=[0,p,q,r];A=[0,1,b,c]
def partitions(k,n):
 if n==1:yield (k,);return
 for i in range(k+1):
  for tail in partitions(k-i,n-1):yield (i,)+tail
@lru_cache(None)
def binom(z,k):return s.prod(z-j for j in range(k))/s.factorial(k)
@lru_cache(None)
def coeff(rows,k):
 total=0
 # Independent construction: coefficient by row multilinearity and exact 4x4 determinant.
 for ds in partitions(k,3):
  ds=(0,)+ds
  matrix=s.Matrix([[((rows[i]>>j)&1)*binom(E[j],ds[i])*A[i]**ds[i] for j in range(4)] for i in range(4)])
  total+=matrix.det(method='domain-ge')
 return s.factor(total)
if __name__=='__main__':
 import json
 from pathlib import Path
 orbs=json.loads(Path(__file__).with_name('orbit_results.json').read_text())['orbits']
 with Path(__file__).with_name('leading_coefficients.txt').open('w') as f:
  for item in orbs:
   rows=tuple(item['rows'])
   for k in range(1,7):
    C=coeff(rows,k)
    if C:
     line=f'{rows}: C{k} = {C}\n';print(line,flush=True);f.write(line);f.flush();break
