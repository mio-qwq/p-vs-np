import sympy as s
from coefficients import *
from pathlib import Path
import sys
negative_control='--negative-control' in sys.argv
checks=[]
def check(name,a,expected=0):
 if negative_control and name=='771515 C6': expected+=1
 diff=s.factor(a-expected)
 if diff!=0: raise SystemExit(f'Identity failed: {name}; residual={diff}')
 checks.append(name);print('PASS',name,flush=True)
def C(rows,k,ss={}):return s.factor(coeff(rows,k).subs(ss,simultaneous=True))
for rows,value in {
 (3,5,15,15):-(b-c)*(p+q-r),
 (3,7,11,12):-p*(b+1),
 (3,7,11,15):-p*(b-c+1),
 (3,13,14,15):-(q-r)*(b-2*c+1),
 (7,7,11,13):-p-q
}.items():check(f'{rows} C1',C(rows,1),value)
R=(3,5,10,15);A=p+q-r;B=2*p*(p-r)-A;E=2*p*q+A;T=6*p*p*q+5*p*p-6*p*q*r-5*p*q-5*p*r-3*p-3*q+3*r
check('351015 C1',C(R,1),b*(r-p)+c*A-q)
check('351015 C2',C(R,2,{c:(b*(p-r)+q)/A}),-q*(b-1)*(p-r)*(b*B+E)/(2*A*A))
check('351015 C3',C(R,3,{b:-E/B,c:(-E*(p-r)/B+q)/A}),-p*p*q*(p-r)*A*T/(3*B**3))
check('351015 T p=1',T.subs(p,1),-s.Rational(2,3)*((3*q+1)*(3*r+1)-4))
check('351015 T p=-1',T.subs(p,-1),s.Rational(2,3)*((3*q+4)*(3*r+4)-4))
u=s.symbols('u');R=(3,5,14,14)
check('351414 C1',C(R,1),-(b-c)*(p+q-2*r))
check('351414 C2',C(R,2,{r:(p+q)/2}),-(b-c)*(p-q)*((b+c)*(p-q)+2*q)/4)
ss={r:(p+q)/2,b:(u-q)/(p-q),c:(-u-q)/(p-q)}
check('351414 C3',C(R,3,ss),u*(u*u+p*q)/(2*(p-q)))
expr=s.together(C(R,4,ss)+p*q*u*(p+q)/(3*(p-q)**2));check('351414 C4 modulo',s.rem(expr.as_numer_denom()[0],u*u+p*q,u))
R=(3,5,15,15)
check('351515 C2',C(R,2,{r:p+q}),p*q*(b-c)*(b+c-1))
check('351515 C3',C(R,3,{r:p+q,c:1-b}),-b*p*q*(b-1)*(2*b-1)*(p+q+2)/2)
check('351515 C4',C(R,4,{r:-2,q:-p-2,c:1-b}),b*p*(b-1)*(2*b-1)*(p+1)*(p+2)/6)
R=(3,7,11,12)
check('371112 C2',C(R,2,{b:-1}),-p*(c*(q-r)+p-q-r-1))
check('371112 C3',C(R,3,{b:-1,c:(q+r+1-p)/(q-r)}),p*(p-2*q-1)*(p-2*r-1)/(2*(q-r)))
R=(3,7,11,15)
check('371115 C2',C(R,2,{c:b+1}),b*p*(p-q-r-1))
check('371115 C3',C(R,3,{c:b+1,p:q+r+1}),b*(q+r+1)*(b*r*(q+1)+q*(r+1))/2)
ss={p:q+r+1,b:-q*(r+1)/(r*(q+1)),c:1-q*(r+1)/(r*(q+1))}
check('371115 C4',C(R,4,ss),q*q*(r+1)**2*(q+r+1)*(q*q+q+r*r+r)/(6*r*r*(q+1)**2))
R=(3,13,14,15);T=q+r-1
check('3131415 C2',C(R,2,{c:(b+1)/2}),-(b-1)*(q-r)*(T*(b-1)+2*p)/4)
check('3131415 C3',C(R,3,{b:1-2*p/T,c:1-p/T}),p*p*(q-r)*((T+p*(p-1))**2-p*p*(p*p-1))/(2*T**3))
R=(7,7,11,13);L=4*p*p*r+p*p-r*r;N=2*p*p*r+p*r-r*r;F=2*L*(b*b-b)+N;G=(3*p*p-1)*(p*p-r*r)+6*p*p*(p*p-1)*r
check('771113 C2',C(R,2,{q:-p}),p*(b*(p+r)+c*(p-r)-p))
ss={q:-p,c:(p-b*(p+r))/(p-r)}
check('771113 C3',C(R,3,ss),-p*p*F/(2*(p-r)**2))
expr=s.together(C(R,4,ss)-p*p*r*(2*b-1)*G/(6*(p-r)*L));check('771113 C4 modulo',s.rem(expr.as_numer_denom()[0],F,b))
check('771113 L simultaneous zero',L.subs(r,p/(1-2*p)),-4*p**4/(2*p-1)**2)
Tp=9*p**6-9*p**4+3*p*p+1
check('771113 discriminant',s.discriminant(G,r),4*p*p*Tp)
n=s.symbols('n');Tn=Tp.subs(p,n);m=3*n**3-3*n/2
check('771113 even lower',Tn-m*m,3*n*n/4+1)
check('771113 even upper',(m+1)**2-Tn,6*n**3-3*n*n/4-3*n)
m=3*n**3-(3*n+1)/2
check('771113 odd lower',Tn-m*m,3*n**3+3*n*n/4-3*n/2+s.Rational(3,4))
check('771113 odd upper',(m+1)**2-Tn,3*(n-1)*(4*n*n+3*n+1)/4)
R=(7,7,15,15);J=p*p-p*q+q*q;K=(p+q)*(2*p-q)*(p-2*q);AA=K-45*J+135
check('771515 C3',C(R,3),-p*q*(b-c)*(p-q)*(b+c-1)/2)
check('771515 C4',C(R,4,{c:1-b}),-b*p*q*(b-1)*(2*b-1)*(p-q)*(p+q-3*r-3)/6)
check('771515 C6',C(R,6,{c:1-b,r:(p+q-3)/3}),-b*p*q*(b-1)*(2*b-1)*(p-q)*(AA*b*(b-1)-2*K)/3240)
h=s.symbols('h')
check('771515 higher q inequality',(K-5*J+15).subs(q,2*p+h),(9*h-15)*p*(p+h)+(2*h-5)*h*h+15)
check('771515 lower q inequality',(-K-15*J+45).subs(q,2*p-h),9*(h-5)*(p-h-1)*(p+1)+2*h*(h-6)*(h+3))
Path(__file__).with_name('identity_checks.json').write_text(__import__('json').dumps({'passed':checks},indent=2)+'\n')
