from pathlib import Path
import json
import sympy as s
x,Q=s.symbols('x Q');b=[0,8,9,21,22];k=10
mu=s.Rational(sum(b),5);C2=sum((v-mu)**2 for v in b);C3=sum((v-mu)**3 for v in b);nu=(C2-10)/120
# Exact normalized character from the confluent formula, rather than moment assumptions.
char=s.cancel(24*sum(x**v/s.prod(v-w for w in b if w!=v) for v in b)/(x-1)**4)
char=s.Poly(char,x)
if char.eval(1)!=1 or any(c<0 for c in char.all_coeffs()):raise RuntimeError('Character normalization failed')
E=[sum(s.Rational(coef)*power**j for (power,),coef in char.terms()) for j in range(4)]
var=s.expand(E[2]-E[1]**2);tau=s.expand(E[3]-3*E[1]*E[2]+2*E[1]**3)
if E[1]!=k or var!=4*nu or tau!=C3/105:raise RuntimeError('Moment formula failed')
alpha=s.diff(char.as_expr(),x,2).subs(x,1)/2
alpha3=s.diff(char.as_expr(),x,3).subs(x,1)/6
beta=k*k-nu
beta21=((5*k-2)*alpha-3*alpha3)/4
gamma=((5*k-2)*beta-4*beta21)/3
S2=alpha*(1+2*Q)+beta*(-Q)
S3=alpha3+2*beta21*Q-gamma*Q
H3=s.expand(S3-k*S2+s.binomial(k,2)*k-s.binomial(k,3))
closed=s.expand(nu*(Q-2)+C3*(2-5*Q)/1260)
if s.expand(H3-closed)!=0 or H3!=(67*Q-122)/21:raise RuntimeError('Mixed derivative formula failed')
Q0=s.Rational(122,67)
if H3.subs(Q,Q0)!=0:raise RuntimeError('Exact vanishing failed')
if not 0<s.Rational(60,67)<s.Rational(62,67)<1:raise RuntimeError('Offset admissibility failed')
out={'status':'passed','exponents':[0,8,9,10,21,22],'minor_exponents':b,'mean':str(mu),'centered_second_sum':str(C2),'centered_third_sum':str(C3),'nu':str(nu),'third_centered_weight_moment':str(tau),'u_squared':'60/67','v_squared':'62/67','Q':str(Q0),'normalized_degree57_coefficient':str(H3),'specialized_degree57_coefficient':'0','masked_degree_upper_bound':55,'zero_polynomial_claim':False,'character_coefficients_descending':[str(c) for c in char.all_coeffs()]}
Path(__file__).with_name('results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
