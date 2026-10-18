#!/usr/bin/env python3
"""Independent verifier for a frozen order-four symbolic certificate.

Standard-library exact arithmetic only. This file does not import or execute
producer code. It reconstructs determinants by Laplace minors, scans all 65536
labeled masks, strips factors by synthetic division, and checks Bézout identities.
"""
from collections import Counter
from copy import deepcopy
from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
from itertools import product
from math import comb, factorial
from pathlib import Path
import argparse
import json

HERE=Path(__file__).resolve().parent
EXPECTED={
 'REPORT.md':'a3ce47a4ae7ce64f7e024a3800a0a0688862d39274916553ff65faf364d46b00',
 'check_consecutive_four.py':'1aab46190729e0dde38476aa394c203972660fec298ed077692bd637d1d83cee',
 'exact_certificate.json':'ecb04ae1ae415590634020e7b3965d7c6e3dccb44ccc960512e21a8a507273aa'}

def require(ok, message):
 if not ok: raise AssertionError(message)

# Independent generic multivariate sparse polynomial operations.
def pclean(p):return {m:Q(v) for m,v in p.items() if v}
def padd(p,q):
 ans=p.copy()
 for m,v in q.items():ans[m]=ans.get(m,0)+v
 return pclean(ans)
def pscale(p,k):return pclean({m:v*k for m,v in p.items()})
def pmul(p,q):
 ans={}
 for a,av in p.items():
  for b,bv in q.items():
   m=tuple(x+y for x,y in zip(a,b));ans[m]=ans.get(m,0)+av*bv
 return pclean(ans)
def ppow(p,n):
 ans={(0,)*len(next(iter(p))):Q(1)}
 for _ in range(n):ans=pmul(ans,p)
 return ans

# Each entry is independently built as a binomial in x and a row offset.
def entry(row, exponent):
 if row==0:return {(exponent,0,0):Q(1)}
 if row==1:return {(k,0,0):Q(comb(exponent,k)) for k in range(exponent+1)}
 if row==2:return {(k,exponent-k,0):Q(comb(exponent,k)) for k in range(exponent+1)}
 return {(k,0,exponent-k):Q(comb(exponent,k)) for k in range(exponent+1)}
ENTRIES=[[entry(i,j) for j in range(4)] for i in range(4)]

def symbolic_det(rows):
 @lru_cache(None)
 def minor(i,cols):
  if not cols:return {(0,0,0):Q(1)}
  ans={}
  for position,j in enumerate(cols):
   if rows[i] & (1<<j):
    sub=minor(i+1,cols[:position]+cols[position+1:])
    ans=padd(ans,pscale(pmul(ENTRIES[i][j],sub),(-1)**position))
  return ans
 return minor(0,(0,1,2,3))

def coefficients(rows):
 result=[{} for _ in range(7)]
 for (x,b,c),v in symbolic_det(rows).items():result[x][b,c]=v
 return result

# Scalar Laplace expansion and permanent, independent of enumerating permutations.
def scalar_det(rows):
 @lru_cache(None)
 def minor(i,cols):
  if not cols:return 1
  return sum((-1)**k*minor(i+1,cols[:k]+cols[k+1:]) for k,j in enumerate(cols) if rows[i]&(1<<j))
 return minor(0,tuple(range(len(rows))))

def permanent(rows,cols=None):
 if cols is None:cols=tuple(range(len(rows)))
 @lru_cache(None)
 def recur(i,remaining):
  if not remaining:return 1
  return sum(recur(i+1,remaining[:k]+remaining[k+1:]) for k,j in enumerate(remaining) if rows[i]&(1<<j))
 return recur(0,tuple(cols))

# Allowed edges are checked by smaller matching problems, not by their producer's
# union of permutation lists.
def allowed_rows(rows):
 out=[]
 for i,r in enumerate(rows):
  out.append(sum((1<<j) for j in range(4) if r&(1<<j) and permanent(rows[:i]+rows[i+1:],tuple(k for k in range(4) if k!=j))))
 return tuple(out)

def components(rows):
 unseen=set(range(8));ans=[]
 while unseen:
  frontier=[min(unseen)];reached=set()
  while frontier:
   v=frontier.pop()
   if v in reached:continue
   reached.add(v)
   if v<4:frontier.extend(4+j for j in range(4) if rows[v]&(1<<j))
   else:frontier.extend(i for i in range(4) if rows[i]&(1<<(v-4)))
  unseen-=reached
  rs=tuple(sorted(v for v in reached if v<4));cs=tuple(sorted(v-4 for v in reached if v>=4))
  ans.append((rs,cs))
 return ans

# Dense univariates, with extended Euclid witness tracking.
def utr(p):
 ans=list(map(Q,p))
 while ans and not ans[-1]:ans.pop()
 return tuple(ans)
def uadd(a,b):return utr([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])
def uscale(a,k):return utr([v*k for v in a])
def umul(a,b):
 if not a or not b:return ()
 ans=[Q(0)]*(len(a)+len(b)-1)
 for i,v in enumerate(a):
  for j,w in enumerate(b):ans[i+j]+=v*w
 return utr(ans)
def upow(a,n):
 ans=(Q(1),)
 for _ in range(n):ans=umul(ans,a)
 return ans

def udivide(a,b):
 require(bool(b),'division by zero')
 original=a;answer=();remain=a
 while remain and len(remain)>=len(b):
  next_term=(Q(0),)*(len(remain)-len(b))+(remain[-1]/b[-1],)
  answer=uadd(answer,next_term)
  remain=uadd(remain,uscale(umul(next_term,b),-1))
 require(uadd(umul(answer,b),remain)==original,'univariate division reconstruction')
 require(not remain or len(remain)<len(b),'univariate division remainder degree')
 return answer,remain

def bezout(a,b):
 r0,r1=a,b;s0,s1=(Q(1),),();t0,t1=(),(Q(1),)
 while r1:
  q,r=udivide(r0,r1)
  r0,r1=r1,r;s0,s1=s1,uadd(s0,uscale(umul(q,s1),-1));t0,t1=t1,uadd(t0,uscale(umul(q,t1),-1))
 if r0:
  v=1/r0[-1];r0=uscale(r0,v);s0=uscale(s0,v);t0=uscale(t0,v)
 require(uadd(umul(s0,a),umul(t0,b))==r0,'Bezout identity')
 if r0:
  require(not udivide(a,r0)[1] and not udivide(b,r0)[1],'gcd divides both inputs')
 return r0,s0,t0

def list_gcd(polys):
 g=();witness=[]
 for p in polys:
  new_g,u,v=bezout(g,p)
  witness=[umul(u,w) for w in witness]+[v];g=new_g
 total=()
 for w,p in zip(witness,polys):total=uadd(total,umul(w,p))
 require(total==g,'multi-polynomial Bezout identity')
 require(bool(g),'all substituted coefficients zero')
 for p in polys:require(not udivide(p,g)[1],'gcd divides all substituted coefficients')
 return g,witness

# Synthetic division in one selected variable by that variable minus A(other).
# In particular no generic bivariate lexicographic division is reused here.
FACTORS=[(0,(Q(0),)),(1,(Q(0),)),(0,(Q(1),)),(1,(Q(1),)),(1,(Q(0),Q(1)))]

def linear_factor(var,A):
 p={(1,0) if var==0 else (0,1):Q(1)}
 for i,v in enumerate(A):
  key=(0,i) if var==0 else (i,0)
  p[key]=p.get(key,0)-v
 return pclean(p)

D={(0,0):Q(1)}
for var,A in FACTORS:D=pmul(D,linear_factor(var,A))

def synthetic(p,var,A):
 if not p:return {},{}
 degree=max(m[var] for m in p);coeffs=[]
 for i in range(degree+1):
  row={m[1-var]:v for m,v in p.items() if m[var]==i}
  coeffs.append(utr([row.get(j,0) for j in range(max(row,default=-1)+1)]))
 q=[()]*degree;carry=()
 for k in range(degree,0,-1):
  carry=uadd(coeffs[k],umul(A,carry));q[k-1]=carry
 rem=uadd(coeffs[0],umul(A,carry))
 quotient={}
 for i,cs in enumerate(q):
  for j,v in enumerate(cs):
   if v:quotient[(i,j) if var==0 else (j,i)]=v
 remainder={(0,j) if var==0 else (j,0):v for j,v in enumerate(rem) if v}
 require(padd(pmul(quotient,linear_factor(var,A)),remainder)==p,'synthetic division reconstruction')
 return quotient,remainder

def stripped(p):
 residual=p;factor_product={(0,0):Q(1)};multiplicities=[]
 for var,A in FACTORS:
  exponent=0
  while residual:
   q,r=synthetic(residual,var,A)
   if r:break
   residual=q;exponent+=1;factor_product=pmul(factor_product,linear_factor(var,A))
  multiplicities.append(exponent)
 require(pmul(factor_product,residual)==p,'coefficient factorization reconstruction')
 return residual,multiplicities

def substitute(p,b,c):
 ans=()
 for (i,j),v in p.items():ans=uadd(ans,uscale(umul(upow(b,i),upow(c,j)),v))
 return ans

def load_poly(raw):
 p={}
 for term in raw:
  require(len(term)==3,'polynomial term length')
  i,j,v=term
  require(type(i) is int and i>=0 and type(j) is int and j>=0,'invalid exponent')
  require((i,j) not in p,'duplicate monomial')
  p[i,j]=Q(v);require(bool(p[i,j]),'stored zero monomial')
 return p

def dumpu(p):return [str(v) for v in p]
def dumpp(p):return [[*m,str(v)] for m,v in sorted(p.items())]

@lru_cache(None)
def inventory():
 # Literally every labeled 4x4 mask, including zero rows.
 orbits=Counter()
 for mask in range(1<<16):orbits[tuple(sorted((mask>>(4*i))&15 for i in range(4)))]+=1
 require(sum(orbits.values())==65536,'labeled coverage')
 require(len(orbits)==3876,'all row orbits including zero rows')
 counts=Counter();full=Counter();hard=[];block_shapes=Counter();deleted=0
 for rows,weight in sorted(orbits.items()):
  require(weight==factorial(4)//__import__('functools').reduce(lambda x,y:x*y,(factorial(m) for m in Counter(rows).values()),1),'row-orbit size')
  pm=permanent(rows);det=scalar_det(rows)
  if not all(rows):
   require(pm==0,'zero row cannot match');full['zero_row_masks']+=weight;continue
  counts['nonzero_row_multisets']+=1
  if not pm:
   require(det==0,'determinant without a matching');counts['no_perfect_matching']+=1;full['no_perfect_matching_nonzero_rows']+=weight;continue
  counts['with_perfect_matching']+=1;full['with_perfect_matching']+=weight
  allowed=allowed_rows(rows)
  require(permanent(allowed)==pm,'allowed-edge removal matching count')
  require(scalar_det(allowed)==det,'allowed-edge removal scalar determinant')
  comps=components(allowed)
  require(all(len(rs)==len(cs) and len(rs)>0 for rs,cs in comps),'allowed components balanced')
  if allowed!=rows:deleted+=1
  if det:
   counts['nonzero_top_coefficient']+=1;full['nonzero_top_coefficient']+=weight;continue
  counts['singular_support']+=1
  if len(comps)>1:
   require(max(len(rs) for rs,cs in comps)<=3,'disconnected block too big')
   counts['decomposes_into_orders_at_most_three']+=1;full['decomposes_into_orders_at_most_three']+=weight
   block_shapes[tuple(sorted(len(rs) for rs,cs in comps))]+=1
   # For each diagonal block its perfect matching is inherited, with its original
   # subset of the four distinct column exponents.
   for rs,cs in comps:require(permanent(tuple(allowed[i] for i in rs),cs)>0,'component lacks perfect matching')
  else:
   counts['connected_singular_support']+=1;full['connected_singular_support']+=weight
   hard.append((rows,pm))
 return dict(counts),dict(full),tuple(hard),dict(block_shapes),deleted


def verify_certificate(data, collect=False):
 base,full,hard,shapes,deleted=inventory();result=dict(base);classcounts=Counter();witnesses=[]
 require(len(data['certificates'])==len(hard),'certificate count mismatch')
 byrows={}
 for cert in data['certificates']:
  rows=tuple(cert['rows']);require(rows not in byrows,'duplicate mask certificate');byrows[rows]=cert
 require(set(byrows)=={r for r,n in hard},'wrong certified mask set')
 for rows,pm in hard:
  cert=byrows[rows];require(cert['matching_count']==pm,f'matching count {rows}')
  actual=coefficients(rows)
  require(len(cert['coefficients_by_x_degree'])==7,'coefficient count')
  claimed=[load_poly(p) for p in cert['coefficients_by_x_degree']]
  require(claimed==actual,f'determinant coefficient mismatch {rows}')
  resmult=[stripped(p) for p in actual];residual=[r for r,m in resmult]
  direct=[k for k,p in enumerate(residual) if p and set(p)=={(0,0)}]
  witness={'rows':rows,'stripping_multiplicities':[m for p,m in resmult]}
  if direct:
   require(cert['kind']=='direct','wrong direct classification')
   degree=cert['coefficient_degree'];require(degree in direct,'invalid direct coefficient')
   require(Q(cert['stripped_constant'])==residual[degree][0,0],'incorrect stripped constant')
   classcounts['distinctness_factor_coefficient']+=1
   witness.update(kind='direct',coefficient_degree=degree,constant=cert['stripped_constant'])
  else:
   require(cert['kind']=='linear_reduction','missing linear reduction')
   degree=max(k for k,p in enumerate(residual) if p);L=residual[degree]
   require(load_poly(cert['leading_stripped'])==L,'wrong leading stripped polynomial')
   require(all(sum(m)<=1 for m in L),'not an affine linear equation')
   b=utr(cert['b_of_t']);c=utr(cert['c_of_t'])
   lc=L.get((0,1),0);lb=L.get((1,0),0);l0=L.get((0,0),0)
   if lc:require(b==(Q(0),Q(1)) and c==utr([-l0/lc,-lb/lc]),'line parametrization incomplete')
   else:require(lb and b==utr([-l0/lb]) and c==(Q(0),Q(1)),'vertical line parametrization incomplete')
   require(not substitute(L,b,c),'line does not solve equation')
   polys=[substitute(p,b,c) for p in residual]
   g,bez=list_gcd(polys)
   require(g==utr(cert['reduced_gcd']),'incorrect univariate gcd')
   d=substitute(D,b,c);require(bool(d),'distinctness identically fails on line')
   require(d==utr(cert['distinctness_polynomial']),'incorrect restricted distinctness polynomial')
   residue=g;removed=(Q(1),);steps=[]
   while len(residue)>1:
    common,u,v=bezout(residue,d)
    if len(common)<=1:break
    quotient,rem=udivide(residue,common);require(not rem,'nonexact gcd removal')
    steps.append({'factor':dumpu(common),'bezout_residue':dumpu(u),'bezout_distinctness':dumpu(v)})
    removed=umul(removed,common);residue=quotient
   require(umul(removed,residue)==g,'obstruction factor reconstruction')
   witness.update(kind='linear_reduction',b_of_t=dumpu(b),c_of_t=dumpu(c),gcd=dumpu(g),bezout_combination=[dumpu(v) for v in bez],restricted_coefficients=[dumpu(v) for v in polys],distinctness_polynomial=dumpu(d),removal_steps=steps,residue=dumpu(residue))
   if len(residue)==1:
    require(bool(residue[0]),'zero final constant')
    require('real_obstruction' not in cert,'unneeded or false real obstruction')
    classcounts['linear_reduction_distinctness_obstruction']+=1
   else:
    require(rows==(6,15,15,15),'unexpected complex exceptional support')
    require(residue==(Q(1),Q(1),Q(1)),'unproved real obstruction')
    # Check the supplied positive quadratic against its exact completed square.
    completed=uadd(upow((Q(1,2),Q(1)),2),(Q(3,4),))
    require(residue==completed,'positive quadratic identity')
    require(cert.get('real_obstruction')=='t^2+t+1=(t+1/2)^2+3/4>0','wrong real certificate')
    classcounts['positive_quadratic_obstruction']+=1
  witnesses.append(witness)
 result.update(classcounts)
 require(data['counts']==result,'incorrect class counts')
 return {'status':'PASS','counts':result,'labeled_mask_counts':full,'disconnected_block_shape_counts':{str(k):v for k,v in shapes.items()},'matching_masks_with_deleted_edges':deleted,'witnesses':witnesses if collect else []}


def small_order_inventory():
 dist=Counter();four_masks=[]
 for mask in range(1<<9):
  rows=tuple((mask>>(3*i))&7 for i in range(3));pm=permanent(rows);dist[pm]+=1
  if pm==4:
   require(mask.bit_count()==8,'order-three four matchings does not mean one missing entry')
   four_masks.append(mask)
 require(set(dist)=={0,1,2,3,4,6},'unexpected order-three matching count')
 require(len(four_masks)==9,'order-three one-entry-deleted mask count')
 return dict(sorted(dist.items()))


def negative_controls(data):
 tests=[]
 def rejected(label,mutate):
  bad=deepcopy(data);mutate(bad)
  try:verify_certificate(bad)
  except AssertionError as e:tests.append({'test':label,'outcome':'REJECTED','reason':str(e)})
  else:raise AssertionError('negative control accepted: '+label)
 rejected('corrupt one determinant coefficient',lambda d:d['certificates'][0]['coefficients_by_x_degree'][0][0].__setitem__(2,'999'))
 rejected('delete a mask certificate',lambda d:d['certificates'].pop())
 rejected('duplicate a mask certificate',lambda d:d['certificates'].__setitem__(1,deepcopy(d['certificates'][0])))
 rejected('falsify matching count',lambda d:d['certificates'][0].__setitem__('matching_count',0))
 rejected('falsify a direct obstruction constant',lambda d:next(c for c in d['certificates'] if c['kind']=='direct').__setitem__('stripped_constant','0'))
 rejected('replace exceptional gcd with claimed constant',lambda d:next(c for c in d['certificates'] if c['rows']==[6,15,15,15]).__setitem__('reduced_gcd',['1']))
 rejected('corrupt affine parametrization',lambda d:next(c for c in d['certificates'] if c['kind']=='linear_reduction').__setitem__('c_of_t',['17']))
 rejected('falsify exhaustive class count',lambda d:d['counts'].__setitem__('connected_singular_support',206))
 # Exact complex counterexample: in Q[t]/(t^2+t+1), choose b=t,c=-1-t.
 coeff=coefficients((6,15,15,15));cyclotomic=(Q(1),Q(1),Q(1));b=(Q(0),Q(1));c=(Q(-1),Q(-1))
 require(all(not udivide(substitute(p,b,c),cyclotomic)[1] for p in coeff),'complex zero determinant counterexample failed')
 reduced_distinctness=udivide(substitute(D,b,c),cyclotomic)[1]
 g,_,_=bezout(reduced_distinctness,cyclotomic)
 require(g==(Q(1),),'complex counterexample has colliding offsets')
 tests.append({'test':'false extension to all distinct complex offsets','outcome':'DISPROVED','mask':[6,15,15,15],'offsets':['0','1','t','-1-t'],'relation':'t^2+t+1=0','distinctness_remainder':dumpu(reduced_distinctness)})
 # Exact repeated-offset negative control shows distinctness is essential.
 full_coeff=coefficients((15,15,15,15))
 require(all(not substitute(p,(Q(0),),(Q(2),)) for p in full_coeff),'repeated-offset zero determinant failed')
 tests.append({'test':'false extension allowing repeated offsets','outcome':'DISPROVED','mask':[15,15,15,15],'offsets':[0,1,0,2]})
 return tests


def exceptional_identity():
 # Independent four-variable Laplace expansion for offsets 0,a,b,c.
 def shifted(row,j):
  out={}
  for k in range(j+1):
   ex=[k,0,0,0]
   if row==0:
    if k!=j:continue
   else:ex[row]=j-k
   out[tuple(ex)]=Q(comb(j,k))
  return out
 rows=(6,15,15,15)
 @lru_cache(None)
 def rec(i,cs):
  if not cs:return {(0,0,0,0):Q(1)}
  out={}
  for n,j in enumerate(cs):
   if rows[i]&(1<<j):out=padd(out,pscale(pmul(shifted(i,j),rec(i+1,cs[:n]+cs[n+1:])),(-1)**n))
  return out
 x={(1,0,0,0):Q(1)};a={(0,1,0,0):Q(1)};b={(0,0,1,0):Q(1)};c={(0,0,0,1):Q(1)}
 rhs=x
 for u,v in [(a,b),(a,c),(b,c)]:rhs=pmul(rhs,padd(u,pscale(v,-1)))
 bracket=padd(padd(pmul(a,b),pmul(a,c)),pmul(b,c))
 bracket=padd(bracket,pmul(x,padd(padd(a,b),c)));rhs=pmul(rhs,bracket)
 require(rec(0,(0,1,2,3))==rhs,'exceptional factorization identity mismatch')
 return {'status':'PASS','identity':'x*(a-b)*(a-c)*(b-c)*(a*b+a*c+b*c+x*(a+b+c))'}


def main():
 parser=argparse.ArgumentParser();parser.add_argument('--certificate',type=Path,default=HERE/'input/exact_certificate.json');parser.add_argument('--skip-negative-controls',action='store_true');args=parser.parse_args()
 frozen={name:sha256((HERE/'input'/name).read_bytes()).hexdigest() for name in EXPECTED}
 require(frozen==EXPECTED,'frozen input hash mismatch')
 data=json.loads(args.certificate.read_text());result=verify_certificate(data,collect=True)
 result['frozen_input_sha256']=frozen;result['small_order_three_matching_distribution']=small_order_inventory();result['exceptional_identity']=exceptional_identity()
 if not args.skip_negative_controls:result['negative_controls']=negative_controls(data)
 out=HERE/'audit_results.json';out.write_text(json.dumps(result,indent=2)+'\n')
 summary={k:v for k,v in result.items() if k!='witnesses'}
 print(json.dumps(summary,indent=2));print(f'PASS: independently checked all 65536 labeled masks and all {len(result["witnesses"])} symbolic certificates.')

if __name__=='__main__':main()
