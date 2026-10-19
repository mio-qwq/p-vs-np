from pathlib import Path
import json
import sympy as s
L=s.symbols('L')
cases=[
 ('signed_kernel',[-3,-1,1,3],[0,1,2,4],1),
 ('gapped_odd',[-4,-1,2,5],[0,2,3,8],2),
 ('all_even',[-3,-1,1,3],[0,2,6,10],2),
 ('lower_odd',[-3,-1,1,3],[0,3,7,9],0),
 ('shifted_gapped',[-4,-2,1,3],[3,5,6,11],2),
 ('five_rows',[-4,-2,0,2,4],[0,2,5,8,12],2),
]
results=[]
for label,a,e,c in cases:
 n=len(a);k=e[c];b=e[:c]+e[c+1:];h=min(b);ell=k-h
 if any((v-h)%2 for v in b):raise RuntimeError('Case not in parity class')
 T=[]
 for row in range(n):
  minor=s.Matrix([[(L+a[t])**e[j] for j in range(n) if j!=c] for t in range(n) if t!=row])
  T.append(s.Poly(s.expand((-1)**(row+c)*(L+a[row])**k*minor.det(method='domain-ge')),L))
 degree=max(t.degree() for t in T)
 C=s.Matrix([[t.nth(d) for t in T] for d in range(degree+1)])
 kernel=C.nullspace()
 if k<h or ell%2==0:
  if kernel:raise RuntimeError('Expected full independence failed')
 else:
  if len(kernel)>1 or any(v[0]+v[1]!=0 or v[0]==0 for v in kernel):raise RuntimeError('Odd-kernel conclusion failed')
 x=[L+v for v in a];G=s.prod(v**h for v in x);Delta=s.prod(x[j]**2-x[i]**2 for i in range(n) for j in range(i+1,n));K=(-1)**(n-1+c)
 R=[s.cancel(t.as_expr()/(K*G*Delta)) for t in T]
 checked=0
 for i in range(n):
  for j in range(i+1,n):
   tau=-s.Rational(a[i]+a[j],2)
   ri=s.cancel((L-tau)*R[i]).subs(L,tau)
   rj=s.cancel((L-tau)*R[j]).subs(L,tau)
   if ri==0 or s.simplify(rj-s.Integer(-1)**(ell+1)*ri)!=0:raise RuntimeError(f'Pair residue parity failed: {label} {i} {j} {ri} {rj}')
   checked+=1
 results.append({'label':label,'offsets':a,'exponents':e,'column':c,'h':h,'ell':ell,'rank':C.rank(),'kernel':[[str(v) for v in z] for z in kernel],'pair_residues_checked':checked})
out={'status':'passed','cases':results,'scope':'Checks corroborate the universal proof; arbitrary mixed-parity exponent lists remain outside it.'}
Path(__file__).with_name('results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
