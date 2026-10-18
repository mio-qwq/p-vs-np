import sympy as s,math,json
D,T,y=s.symbols('d T y'); q=s.symbols('q')
P=(48*D**2-24240)*T**2+(90*D**4-55860*D**2+1875930)*T+55*D**6-28125*D**4+2236245*D**2-38150575
C=(24235-547*D**2)*T**2+(-435*D**4+37590*D**2-1039395)*T+55*D**6-28125*D**4+2236245*D**2-38150575
F=41*q**4-11300*q**3-5027466*q**2-242872100*q+2999439785
if s.expand(s.discriminant(P,T)+60*F.subs(q,D**2))!=0:raise RuntimeError('disc')
L=(D**2-18*D+17)/2; Tlo=92-4*D**2/s.Integer(5)
checks={'F529':s.Poly(F.subs(q,529+y),y).all_coeffs(),'C0':s.Poly(C.subs(T,0).subs(D,25+y),y).all_coeffs(),'C_L':s.Poly(C.subs(T,L).subs(D,25+y),y).all_coeffs(),'C_Tlo':s.factor(C.subs(T,Tlo))}
if not all(v>0 for v in checks['F529']+checks['C0']):raise RuntimeError('positive')
if not all(v<0 for v in checks['C_L']):raise RuntimeError('negative')
for name,p,ds in [('pair',P,range(1,23,4)),('triple',C,range(1,25,2))]:
 checks[name]=[]
 for d in ds:
  disc=int(s.discriminant(p,T).subs(D,d)); root=math.isqrt(disc) if disc>=0 else None
  if root is not None and root*root==disc:raise RuntimeError('square')
  checks[name].append([d,disc,root])
print(json.dumps(checks,default=str,indent=2))
