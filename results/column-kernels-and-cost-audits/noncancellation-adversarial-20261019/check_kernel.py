"""Exact independent raw-minor checks; no randomized or floating-point tests."""
import json
import sympy as s
x=s.symbols('x')

def check(a,d=0,expected_nullity=None):
 n=len(a);c=1;mean=sum(a)/s.Integer(n);b=[s.simplify(v-mean)for v in a]
 e=[d+j for j in range(n-1)]+[d+n]
 V=s.Matrix([[(x+a[i])**e[j]for j in range(n)]for i in range(n)])
 common=s.prod((x+a[i])**d for i in range(n))
 ts=[]
 for r in range(n):
  T=(-1)**(r+c)*V[r,c]*V.minor_submatrix(r,c).det(method='domain-ge')
  ts.append(s.Poly(s.cancel(T/common),x))
 delta=s.prod(b[j]-b[i]for i in range(n)for j in range(i+1,n))
 X=x+mean;f=s.prod(x+v for v in b).expand();fp=s.diff(f,x)
 for r in range(n):
  hp=s.prod(b[r]-b[j]for j in range(n)if j!=r)
  expr=(-1)**(n-2)*delta*((((n-1)*x-b[r])*fp-n*x*s.cancel(f/(x+b[r])))/hp)
  if s.simplify(ts[r].as_expr()-expr.subs(x,X))!=0:raise RuntimeError('identity failure')
 C=s.Matrix([[T.nth(k) for T in ts]for k in range(n+1)])
 null=C.nullspace();exception=all(v!=0 for v in b)and s.simplify(fp.subs(x,0))==0
 if len(null)!=int(exception):raise RuntimeError('nullity mismatch')
 if expected_nullity is not None and len(null)!=expected_nullity:raise RuntimeError('wrong expected nullity')
 if exception:
  w=[s.prod(b[r]-b[j]for j in range(n)if j!=r)/b[r]for r in range(n)]
  if any(s.simplify(v)!=0 for v in C*s.Matrix(w)):raise RuntimeError('candidate kernel failure')
  if not(any(v>0 for v in w)and any(v<0 for v in w)):raise RuntimeError('mixedness failure')
 return {'offsets':[str(v)for v in a],'shift':d,'nullity':len(null),'rank':C.rank()}

cases=[((-2,0,2),0,0),((-3,-1,1,3),0,1),((-3,-1,1,3),2,1),((0,1,4,9),0,0),((-5,-3,-1,1,3,5),0,1),((-7,-5,-3,-1,1,3,5,7),0,1),((0,1,2,3,4),0,0)]
# The n5 algebraic example is separately checked using its defining monic
# polynomial, avoiding expensive symbolic determinants over radicals.
res=[check(a,d,r)for a,d,r in cases]
t=s.symbols('t');h=s.expand((t+1)*(t+2)*(t+3)*(t*t-6*t+s.Rational(36,11)))
if h.coeff(t,4)!=0 or h.coeff(t,1)!=0 or h.subs(t,0)==0:raise RuntimeError('n5 defining polynomial failed')
# The last two roots are 3 +/- sqrt(63/11), distinct positive and different from negative roots.
res.append({'nonsymmetric_n5_defining_polynomial':str(h),'real_distinct_roots':['-3','-2','-1','3-sqrt(63/11)','3+sqrt(63/11)'],'centroid_zero':True,'reciprocal_sum_zero':True,'scope':'exact defining-polynomial check; universal theorem supplies its kernel'})
open('kernel_checks.json','w').write(json.dumps(res,indent=2)+'\n')
print('PASS:',len(cases),'independent raw-cofactor cases plus exact n5 defining-polynomial certificate')
