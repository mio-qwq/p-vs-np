#!/usr/bin/env python3
"""Required boundary/negative controls and order-three support enumeration."""
from itertools import permutations
from pathlib import Path
from fractions import Fraction as F
import json
import subprocess
import sys
import argparse
import tempfile
import check_tail_gap as C

def require(condition,message):
 if not condition: raise ValueError(message)

# This is the only finite combinatorial fact used by the arbitrary-exponent
# smaller-order proof: exactly the full 3x3 masks minus one edge have four PMs.
p3=list(permutations(range(3)))
counts={}
for mask in range(512):
 rows=[(mask>>(3*i))&7 for i in range(3)]
 number=sum(all((rows[i]>>p[i])&1 for i in range(3)) for p in p3)
 counts[number]=counts.get(number,0)+1
 if number==4:require(mask.bit_count()==8,'four-matching 3x3 mask not full minus one')
require(counts=={0:265,1:150,2:69,3:18,4:9,6:1},'wrong order-three support classification')
print('PASS: all 512 order-three masks classified; four-matchings implies exactly one missing entry.')

# The finite method must refuse the known genuinely complex m=3 obstruction.
try:C.prove_exponent(3)
except ValueError as error:
 message=str(error)
 require('unresolved coefficient gcd: 3, (6, 15, 15, 15)' in message,'m=3 rejected for wrong reason: '+message)
 require('Fraction(1, 1), Fraction(1, 1), Fraction(1, 1)' in message,'wrong exceptional quadratic')
 print('PASS: m=3 complex-field extension rejected at (6,15,15,15), with gcd 1+t+t^2.')
else:raise ValueError('m=3 complex-field extension unexpectedly accepted')

def determinant(rows,exponents):
 total=sum(exponents);coefficients=[{} for _ in range(total+1)]
 for p in C.matchings(rows):
  term=[C.scale(C.ONE,C.sign(p))]
  for i,j in enumerate(p):term=C.xmul(term,C.shifted_power(i,exponents[j]))
  for i,q in enumerate(term):coefficients[i]=C.add(coefficients[i],q)
 return coefficients

# Explicit counterexample over Q[t]/(t^2+t+1), with offsets 0,1,t,-1-t.
quad=(F(1),F(1),F(1));b=(F(0),F(1));c=(F(-1),F(-1))
for polynomial in determinant((6,15,15,15),(0,1,2,3)):
 require(not C.udivrem(C.substitute(polynomial,b,c),quad)[1], 'complex counterexample not zero')
d=C.substitute(C.D,b,c)
require(len(C.ugcd(d,quad))==1,'complex counterexample offsets not distinct')
print('PASS: exact distinct complex-offset zero determinant reproduced modulo t^2+t+1.')

# Allowing repeated offsets would also make the claimed statement false.
for polynomial in determinant((15,15,15,15),(0,1,2,4)):
 require(not C.substitute(polynomial,(F(0),),(F(2),)),'repeated-offset determinant not zero')
require(not C.substitute(C.D,(F(0),),(F(2),)),'repeated offsets not excluded by D')
print('PASS: repeated-offset full-mask zero determinant reproduced, outside D != 0 domain.')

# An altered coefficient in a saved certificate must fail normal verification.
base=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--certificate',type=Path,help='optional already-generated certificate')
args=parser.parse_args()
flags=['-O'] if sys.flags.optimize else []
with tempfile.TemporaryDirectory(prefix='tail-gap-negative-') as temp:
 temporary=Path(temp)
 certificate_path=args.certificate
 if certificate_path is None:
  certificate_path=temporary/'exact_certificate.json'
  generated=subprocess.run([sys.executable,*flags,str(base/'check_tail_gap.py'),'--write',str(certificate_path)],capture_output=True,text=True)
  require(generated.returncode==0,'certificate generation failed: '+generated.stderr)
 certificate=json.loads(certificate_path.read_text())
 first=certificate['cases'][0]['certificates'][0]
 require(first['kind']=='direct','first witness unexpectedly not direct')
 first['coefficient'][0][2]=str(F(first['coefficient'][0][2])+1)
 corrupt=temporary/'corrupt_certificate.json'
 corrupt.write_text(json.dumps(certificate,separators=(',',':'))+'\n')
 result=subprocess.run([sys.executable,*flags,str(base/'check_tail_gap.py'),'--check',str(corrupt)],capture_output=True,text=True)
 require(result.returncode!=0 and 'certificate mismatch' in result.stderr,'corrupt coefficient was not rejected')
 print('PASS: physical saved-certificate coefficient corruption rejected with nonzero exit status.')
