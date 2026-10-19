"""Exact certificate for repeated nonreal roots of a translated h_6.
No floats, assertions, algebraic-root guessing, or remote state required.
"""
import sympy as s
u,y,L=s.symbols('u y L')
P=(12827754466*u**6+6383624352*u**5+1082672647*u**4+
   114597802*u**3+4936407*u**2+164108*u-236)
lo,hi=s.Rational(1,729),s.Rational(1,700)
def require(v,msg):
 if not v: raise RuntimeError(msg)

# Four opposite pairs have squared positive knots 1,u,4u,9u.
b=(s.Integer(1),u,4*u,9*u)
h=[s.Integer(1)]
for j in range(1,4):
 h.append(s.expand(sum(sum(x**k for x in b)*h[j-k] for k in range(1,j+1))/j))
A=s.Integer(3003);B=1001*(14*u+1);C=91*(147*u**2+14*u+1);D=1408*u**3+147*u**2+14*u+1
F=A*y**3+B*y**2+C*y+D
require(s.expand(F-sum(s.binomial(14,6-2*j)*h[j]*y**(3-j) for j in range(4)))==0,'translation formula')
require(s.expand(s.discriminant(F,y)-364364*P)==0,'discriminant')
require(P.subs(u,lo)<0 and P.subs(u,hi)>0,'positive-root isolating interval')
require(all(v>0 for v in s.Poly(P,u).all_coeffs()[:-1]),'positive derivative on u>0')
require(hi<s.Rational(1,9),'distinctness interval')
E=s.factor(B**2-3*A*C)
require(s.expand(E-91091*(833*u**2+182*u+2))==0,'nontriple condition')
r=s.factor((9*A*D-B*C)/(2*E));q=s.factor(-B/A-2*r)
for coefficient in s.Poly(s.together(F-A*(y-r)**2*(y-q)),y).all_coeffs():
 numerator=s.fraction(s.cancel(coefficient))[0]
 require(s.rem(numerator,P,u)==0,'factorization modulo defining polynomial')
require(s.cancel(r+(74631*u**3+13622*u**2+1085*u+32)/(91*(833*u**2+182*u+2)))==0,'double root formula')
separation=389563*u**3+185073*u**2+9345*u-106
require(s.cancel(r-q-separation/(273*(833*u**2+182*u+2)))==0,'root ordering formula')
require(separation.subs(u,hi)<0,'double root is outer')
# q<0 follows directly on isolating interval, without invoking positivity theorem.
qnum=613456*u**3+225939*u**2+12600*u-10
require(s.cancel(q+qnum/(273*(833*u**2+182*u+2)))==0,'simple root formula')
require(qnum.subs(u,lo)>0,'simple root negative')
# Rational integer knots produce an explicit symmetric/off-axis example.
integer_knots=(-30,-3,-2,-1,0,1,2,3,30)
p=[sum(s.Integer(a)**j for a in integer_knots) for j in range(7)]
hfull=[s.Integer(1)]
for j in range(1,7): hfull.append(s.expand(sum(p[k]*hfull[j-k] for k in range(1,j+1))/j))
H=sum(s.binomial(14,6-j)*hfull[j]*L**(6-j) for j in range(7))
require(s.expand(H)==3003*L**6+914914*L**4+74869977*L**2+740473708,'integer knot polynomial')
Fi=3003*y**3+914914*y**2+74869977*y+740473708
require(s.discriminant(Fi,y)==-9179328219383127985355176,'rational example discriminant')
require(s.degree(s.gcd(Fi,s.diff(Fi,y)),y)==0,'rational example simple y roots')
print('PASS: exact distinct-knot nonreal double roots; outer simple-root claim refuted.')
print('PASS: exact symmetric integer knots yield four off-imaginary-axis roots.')
print('Neither example is a proper polynomial power or a Laplace-kernel example.')
# Generic positive compact measure counterexample; NOT a simplex projection.
y1=(945-s.sqrt(639695))/47
y2=(945+s.sqrt(639695))/47
v=s.Rational(16,5)
w1=(y2-v)/(y1*(y2-y1));w2=(v-y1)/(y2*(y2-y1))
w0=s.simplify(1-w1-w2)
require(w0==s.Rational(9126,13475),'atomic weight at zero')
quadratic=47*y*y-1890*y+5390
require(quadratic.subs(y,3)>0 and quadratic.subs(y,v)<0,'smaller positive atom interval')
require(quadratic.subs(y,37)<0 and quadratic.subs(y,38)>0,'larger positive atom interval')
for k,target in [(1,1),(2,s.Rational(16,5)),(3,14),(4,196)]:
 require(s.simplify(w1*y1**k+w2*y2**k-target)==0,'atomic exact moment')
atomic=L**8+28*L**6+224*L**4+392*L**2+196
require(s.expand(atomic-(L**4+14*L**2+14)**2)==0,'generic compact-measure proper power')
print('PASS: compact symmetric atomic measure has exact degree-eight proper-power moment polynomial.')
