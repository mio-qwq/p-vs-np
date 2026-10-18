#!/usr/bin/env python3
"""Reject a corrupted exact identity and reproduce exact theorem boundaries.

Python standard library only. Generated files remain in temporary storage.
Optimization is propagated to the subprocess, so -O cannot disable the tests.
"""
from fractions import Fraction as F
from itertools import permutations
from math import comb
from pathlib import Path
import os
import subprocess
import sys
import tempfile


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


# Exact field Q[w]/(w^2+w+1), where w is a primitive cube root of unity.
# Each pair (a,b) represents a+b*w; polynomial arrays are in increasing x degree.
ZERO=(F(0),F(0))
ONE=(F(1),F(0))

def add(a,b): return (a[0]+b[0],a[1]+b[1])
def neg(a): return (-a[0],-a[1])
def mul(a,b):
    return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]-a[1]*b[1])
def power(a,n):
    value=ONE
    for _ in range(n): value=mul(value,a)
    return value

def pmul(a,b):
    out=[ZERO]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): out[i+j]=add(out[i+j],mul(x,y))
    return out

def determinant(rows, exponents, offsets):
    out=[ZERO]*(sum(exponents)+1)
    for p in permutations(range(4)):
        if not all((rows[i]>>p[i])&1 for i in range(4)): continue
        sign=(-1)**sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))
        term=[(F(sign),F(0))]
        for i,j in enumerate(p):
            e=exponents[j]
            term=pmul(term,[mul((F(comb(e,k)),F(0)),power(offsets[i],e-k)) for k in range(e+1)])
        for i,value in enumerate(term): out[i]=add(out[i],value)
    return out

def is_zero(values): return all(v==ZERO for v in values)


def main():
    offsets=[ZERO,ONE,(F(0),F(1)),(F(-1),F(-1))]
    require(len(set(offsets))==4, 'complex offsets are not distinct')
    require(is_zero(determinant((6,15,15,15),(0,1,2,3),offsets)),
            'complex-boundary determinant not identically zero')
    print('PASS: real-field extension fails at four distinct offsets over Q[w]/(w^2+w+1).')
    repeated=[ZERO,ONE,ZERO,(F(2),F(0))]
    require(is_zero(determinant((15,15,15,15),(0,1,2,4),repeated)),
            'repeated-offset full determinant not zero')
    print('PASS: repeated-offset counterexample confirms the distinctness hypothesis.')
    real=[(F(i),F(0)) for i in range(4)]
    require(is_zero(determinant((0,15,15,15),(0,1,2,4),real)),
            'empty-row determinant not zero')
    print('PASS: empty-row counterexample confirms the nonempty-subset hypothesis.')
    # Actual numeric witnesses here are only boundary counterexamples. The theorem
    # itself uses coefficientwise symbolic identities in verify_identities.py.
    source=(Path(__file__).resolve().parent/'verify_identities.py').read_text()
    before='((0,1,3), B/6)'
    require(source.count(before)==1, 'identity mutation target not unique')
    altered=source.replace(before,'((0,1,3), B/7)')
    flags=['-O'] if sys.flags.optimize else []
    env=dict(os.environ)
    env.pop('PYTHONOPTIMIZE',None)
    env['PYTHONDONTWRITEBYTECODE']='1'
    with tempfile.TemporaryDirectory(prefix='partial-row-negative-') as temp:
        path=Path(temp)/'corrupt_identity.py'
        path.write_text(altered)
        result=subprocess.run([sys.executable,*flags,str(path)],capture_output=True,
                              text=True,env=env,timeout=60)
        require(result.returncode!=0, 'corrupted identity was accepted')
        require('exceptional middle pair C(0, 1, 3)' in result.stderr,
                'corrupted identity failed for an unexpected reason: '+result.stderr)
    print('PASS: physical B/6 to B/7 identity corruption rejected by explicit coefficient comparison.')


if __name__=='__main__': main()
