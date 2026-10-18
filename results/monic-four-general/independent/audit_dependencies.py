import sympy as s,itertools,json
from pathlib import Path
from coefficients import *
checks=[]
def check(name,actual,expected=0):
 residue=s.factor(actual-expected)
 if residue!=0: raise RuntimeError(f'{name}: {residue}')
 checks.append(name);print('PASS',name,flush=True)
# Exact lower-order support classification: all 512 masks.
perms=list(itertools.permutations(range(3)))
counts={}
for bits in range(512):
 M=[[bits>>(3*i+j)&1 for j in range(3)] for i in range(3)]
 match=[pp for pp in perms if all(M[i][pp[i]] for i in range(3))]
 counts[len(match)]=counts.get(len(match),0)+1
 if len(match)==4 and sum(map(sum,M))!=8:raise RuntimeError('Four-matching 3x3 mask is not full minus one')
if set(counts)!={0,1,2,3,4,6}:raise RuntimeError('Unexpected 3x3 matching count')
checks.append('all 512 lower-order masks classified')
# Immediate coefficient cases, including every earlier coefficient stated zero.
immediate={
 (3,7,12,15):(1,c*p), (3,7,13,13):(1,-r*(b-c)),
 (3,7,15,15):(1,-p*(b-c)),(3,12,15,15):(2,-p*(b-c)*(q-r)),
 (3,13,13,14):(1,-2*(b-1)*(q-r)),(3,13,13,15):(1,-(b-1)*(q-r)),
 (3,13,15,15):(1,-(b-c)*(q-r)),(7,7,11,11):(2,-p*(b-c)*(q-r)),
 (7,7,11,15):(1,-p),(7,11,15,15):(1,p*(b-c)),
 (7,15,15,15):(3,p*q*(b-1)*(b-c)*(c-1)*(p-q)/2),
 (15,15,15,15):(6,b*c*p*q*r*(b-1)*(b-c)*(c-1)*(p-q)*(p-r)*(q-r)/12)}
for rows,(k,value) in immediate.items():
 for j in range(k):check(f'{rows} prior C{j}',coeff(rows,j))
 check(f'{rows} C{k}',coeff(rows,k),value)
for rows in [(3,5,10,15),(3,5,11,13),(3,5,14,14),(3,5,15,15),(3,7,11,12),(3,7,11,15),(3,13,14,15),(7,7,11,13)]:
 check(f'{rows} C0',coeff(rows,0))
for k in range(3):check(f'771515 prior C{k}',coeff((7,7,15,15),k))
# Match counts and structural cofactors for the valuation arguments.
all_perms=list(itertools.permutations(range(4)))
for rows,target in {
 (3,5,11,13):[[1,3,0,0],[1,0,3,0],[1,1,0,2],[1,0,1,2]],
 (3,5,10,15):[[2,2,0,0],[1,0,3,0],[0,1,0,3],[1,1,1,1]]
}.items():
 match=[pp for pp in all_perms if all(rows[i]>>pp[i]&1 for i in range(4))]
 got=[[sum(pp[i]==j for pp in match) for j in range(4)] for i in range(4)]
 if got!=target:raise RuntimeError(f'Matching entry counts: {rows}: {got}')
 checks.append(f'{rows} entry matching counts')
rows=(3,5,10,12)
if sum(all(rows[i]>>pp[i]&1 for i in range(4)) for pp in all_perms)!=2:raise RuntimeError('Two-matching orbit count failed')
checks.append('351012 has exactly two matchings')
U=s.symbols('U0:4');V=s.symbols('V0:4');W=s.symbols('W0:4')
def abstract(rows):return s.Matrix([[(rows[i]>>j&1)*[1,U[i],V[i],W[i]][j] for j in range(4)] for i in range(4)])
M=abstract((3,5,11,13))
check('351113 row0 exponent0 unit',M.cofactor(0,0),-U[2]*V[1]*W[3])
check('351113 row1 exponent0 unit',M.cofactor(1,0),U[0]*V[3]*W[2])
check('351113 row2 exponentp unit',M.cofactor(2,1),-V[1]*W[3])
check('351113 row3 exponentq unit',M.cofactor(3,2),U[0]*W[2])
check('351113 row2 exponentr binomial',M.cofactor(2,3),U[0]*(V[3]-V[1]))
check('351113 row3 exponentr binomial',M.cofactor(3,3),V[1]*(U[0]-U[2]))
M=abstract((3,5,10,15))
check('351015 row1 exponent0 unit',M.cofactor(1,0),U[0]*V[3]*W[2])
check('351015 row2 exponentp unit',M.cofactor(2,1),-V[1]*W[3])
check('351015 row0 exponent0 binomial',M.cofactor(0,0),V[1]*(W[2]*U[3]-U[2]*W[3]))
check('351015 row0 exponentp binomial',M.cofactor(0,1),W[2]*(V[3]-V[1]))
# One partial row: arbitrary subset, not just the representative subset.
a=s.symbols('a');Vabc=(b-a)*(c-a)*(c-b);B=p*q*(p-q)*(p+q)
weights=[(q-p)*(r-p)*(r-q),-q*r*(r-q),p*r*(r-p),-p*q*(q-p)]
for mask in range(1,16):
 for k in range(3):check(f'partial row {mask} prior C{k}',coeff((mask,15,15,15),k))
 check(f'partial row {mask} C3',coeff((mask,15,15,15),3),(b-1)*(c-1)*(c-b)*sum(weights[j] for j in range(4) if mask>>j&1)/2)
check('partial weights sum',sum(weights))
check('partial opposite pair 01',weights[0]+weights[1],-p*(r-q)*(q+r-p))
check('partial opposite pair 03',weights[0]+weights[3],r*(q-p)*(r-p-q))
check('partial opposite pair 12',weights[1]+weights[2],r*(p-q)*(r-p-q))
check('partial opposite pair 23',weights[2]+weights[3],p*(r-q)*(r+q-p))
def gen(k):return s.factor(a**k*coeff((6,15,15,15),k).subs({b:b/a,c:c/a}).subs(r,p+q))
check('partial exceptional C4',gen(4),Vabc*B*(a+b+c)/6)
check('partial exceptional C5 after sum zero',(gen(5)-Vabc*B*(a*b+a*c+b*c)/6).subs(c,-a-b))
# Independent centered derivative calculation, with parity encoded algebraically.
t,X,Y,Z=s.symbols('t X Y Z')
expected={(0,0,1):4*Z*(-X*q+Y*p-p+q),
(0,1,0):-4*Z*((r-p)*X+p*Y*t-r)/t,
(1,0,0):4*Z*(q*X*t+(r-q)*Y-r)/t,
(1,1,1):4*Z*((r-p)*X+(q-r)*Y+(p-q)*t)/t}
for parity,value in expected.items():
 ep,eq,er=parity
 rows=[[1,(-1)**ep,(-1)**eq,0],[1,1,1,0],[1,(-1)**ep*X,(-1)**eq*Y,(-1)**er*Z],[1,X,Y,Z]]
 derivative=0
 for i,ai in enumerate([-1,1,-t,t]):
  rr=[row[:] for row in rows];rr[i]=[v*e/ai for v,e in zip(rows[i],[0,p,q,r])]
  derivative+=s.Matrix(rr).det(method='domain-ge')
 check(f'center derivative parity {parity}',derivative,value)
check('last mixed derivative at 1',(q*(p+1)/2-(q-r)*q/2).subs(r,(p+q-3)/3),q*(2*p-q)/3)
Path(__file__).with_name('dependency_checks.json').write_text(json.dumps({'passed':checks,'order_three_matching_counts':counts},indent=2)+'\n')
