from pathlib import Path
"""Polynomial certificate-backed solver; does NOT discover graphic representations."""
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'quota'))
from quota import solve_quota

def rank(cols):
 p={}
 for x in cols:
  while x:
   i=x.bit_length()-1
   if i in p:x^=p[i]
   else:p[i]=x;break
 return len(p)

def equal_kernels(A,B):
 if len(A)!=len(B):return False
 piv={}
 for a,b in zip(A,B):
  while a:
   i=a.bit_length()-1
   if i in piv:a^=piv[i][0];b^=piv[i][1]
   else:piv[i]=(a,b);break
  if not a and b:return False
 return rank([b for a,b in piv.values()])==len(piv)

def linear_solution(A,target):
 piv={}
 for j,a in enumerate(A):
  mask=1<<j
  while a:
   i=a.bit_length()-1
   if i in piv:a^=piv[i][0];mask^=piv[i][1]
   else:piv[i]=(a,mask);break
 ans=0
 while target:
  i=target.bit_length()-1
  if i not in piv:return None
  target^=piv[i][0];ans^=piv[i][1]
 return ans

def solve_with_certificate(A,pairs,target,n,extended_edges):
 used=set()
 for i,j in pairs:
  if i==j or i in used or j in used:raise ValueError('pairs must be disjoint')
  used|={i,j}
  if not A[i] or not A[j] or A[i]==A[j]:raise ValueError('preprocess dependent pairs first')
 ext=A+[A[i]^A[j] for i,j in pairs]
 if len(ext)!=len(extended_edges):raise ValueError('wrong certificate edge count')
 if any(u==v or min(u,v)<0 or max(u,v)>=n for u,v in extended_edges):raise ValueError('invalid graph endpoints')
 B=[(1<<u)|(1<<v) for u,v in extended_edges]
 if not equal_kernels(ext,B):raise ValueError('graph certificate has different binary kernel')
 original=extended_edges[:len(A)];groups=[]
 for i,j in pairs:
  common=set(original[i])&set(original[j])
  if not common:raise AssertionError('triangle circuit failed to force incidence')
  groups.append((min(common),[i,j],1))
 z=linear_solution(A,target)
 if z is None:return None
 transported=0
 for i,b in enumerate(B[:len(A)]):
  if z>>i&1:transported^=b
 mask=solve_quota(n,original,groups,transported)
 if mask is not None:
  actual=0
  for i,a in enumerate(A):
   if mask>>i&1:actual^=a
  assert actual==target and all(not(mask>>i&1 and mask>>j&1) for i,j in pairs)
 return mask
