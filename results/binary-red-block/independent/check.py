import itertools,math,json
from fractions import Fraction

def mul(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return c

def delta(a):
 return math.prod(a[j]-a[i] for i in range(len(a)) for j in range(i+1,len(a)))

def check(a,e,red):
 n=len(a);I=sorted({i for i,j in red});J=sorted({j for i,j in red});k=len(I);D=sum(e);ps=[[0]*(D+1) for _ in range(k+1)];counts=[[0,0] for _ in range(k+1)]
 for p in itertools.permutations(range(n)):
  neg=sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))%2
  t=sum((i,p[i]) in red for i in range(n));counts[t][neg]+=1
  q=[1]
  for i,j in enumerate(p):q=mul(q,[math.comb(e[j],r)*a[i]**(e[j]-r) for r in range(e[j]+1)])
  for r,v in enumerate(q):ps[t][r]+=(-1)**neg*v
 if len(J)!=k:raise ValueError('not square block')
 detB=sum((-1)**sum(p[i]>p[j] for i in range(k) for j in range(i+1,k))*math.prod(int((I[i],J[p[i]]) in red) for i in range(k)) for p in itertools.permutations(range(k)))
 if not detB:raise ValueError('singular red block')
 eps=(-1)**(sum(I)+sum(J))*detB
 ac=[a[i] for i in range(n) if i not in I];ec=[e[j] for j in range(n) if j not in J];m=n-k
 lead=eps*Fraction(delta(ac)*delta(ec),math.prod(math.factorial(r) for r in range(m)));deg=D-m*(m-1)//2
 for t,poly in enumerate(ps):
  actualdeg=max(i for i,x in enumerate(poly) if x)
  if actualdeg!=deg or poly[deg]!=(-1)**(k-t)*math.comb(k,t)*lead: raise ValueError((t,actualdeg,deg,poly[deg],lead))
  if m>=2 and counts[t][0]!=counts[t][1]:raise ValueError('parity')
 return dict(offsets=a,exponents=e,red=sorted(red),degree=deg,leading=[p[deg] for p in ps],counts=counts,polynomials=ps)

if __name__=='__main__':
 cases=[(list(range(6)),list(range(6)),{(i,i) for i in range(3)}),([-3,0,2,7,9],[4,0,7,2,1],{(0,3),(2,0),(4,2)}),([-2,0,3,5],[5,2,0,8],{(0,2),(1,3),(3,1)})]
 cases.extend([(list(range(6)),list(range(6)),{(0,0),(0,1),(1,1),(1,2),(2,2)}),(list(range(6)),list(range(6)),{(i,j) for i in range(3) for j in range(3) if i!=j})])
 out=[check(*c) for c in cases]
 print(json.dumps(out,indent=2))
