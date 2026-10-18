#!/usr/bin/env python3
"""Check the small-order leading coefficient identities with symbolic exponents."""
from sympy import Matrix, symbols, prod, expand

for k in (2,3):
 e=symbols('e0:'+str(k));a=symbols('a0:'+str(k))
 binom=Matrix([[prod(e[j]-s for s in range(i))/prod(range(1,i+1))
                for j in range(k)] for i in range(k)])
 v=prod(e[j]-e[i] for i in range(k) for j in range(i+1,k)) / prod(
       prod(range(1,l+1)) for l in range(k))
 if expand(binom.det()-v)!=0:raise RuntimeError('Exponent Vandermonde failed')
 av=Matrix([[a[i]**l for l in range(k)] for i in range(k)])
 if expand(av.det()-prod(a[j]-a[i] for i in range(k) for j in range(i+1,k)))!=0:
  raise RuntimeError('Offset Vandermonde failed')
 print(f'PASS: order {k} coefficient Vandermonde identity holds for symbolic offsets and symbolic exponents')
