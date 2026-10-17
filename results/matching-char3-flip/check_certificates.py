"""Independent standard-library verification, no elimination or orbit code."""
import json,itertools,collections,copy
from pathlib import Path
HERE=Path(__file__).parent

def normalize(es):return tuple(sorted(tuple(sorted(e)) for e in es))
def all_matchings(vs):
 if not vs:yield ();return
 a=vs[0]
 for i in range(1,len(vs)):
  for tail in all_matchings(vs[1:i]+vs[i+1:]):yield ((a,vs[i]),)+tail

def flip_ball(n,r):
 base=tuple((2*i,2*i+1) for i in range(n));dist={base:0};front=[base]
 for d in range(1,r+1):
  nxt=[]
  for m in front:
   for i,j in itertools.combinations(range(n),2):
    a,b=m[i];c,e=m[j];rest=m[:i]+m[i+1:j]+m[j+1:]
    for pairs in (((a,c),(b,e)),((a,e),(b,c))):
     z=normalize(rest+pairs)
     if z not in dist:dist[z]=d;nxt.append(z)
  front=nxt
 return dist

def verify_upper(cert,ball):
 n=cert['n'];balance=collections.Counter()
 def add(m,c):
  assert len(m)==n and sorted(v for e in m for v in e)==list(range(2*n))
  for d in range(3):
   for mon in itertools.combinations(m,d):balance[mon]+=c
 target=normalize(cert['target']);assert target not in ball;add(target,-1)
 for t in cert['terms']:
  for raw in t['matchings']:
   m=normalize(raw);assert m in ball;add(m,t['coefficient'])
 assert all(v%3==0 for v in balance.values())
 # Monomials absent from balance evaluate zero on every matching in identity.
 return len(balance)

def verify_lower(w,ball):
 terms=[(t['coefficient'],frozenset(tuple(e) for e in mon)) for t in w['terms'] for mon in t['monomials']]
 assert all(len(mon)<=2 for c,mon in terms)
 def ev(m):
  s=set(m);return sum(c for c,mon in terms if mon<=s)%3
 target=normalize(w['target']);assert ev(target)==1
 assert target not in ball
 # Four explicit flips are checked by independent radius-four BFS membership.
 assert target in flip_ball(w['n'],4)
 for m in ball:assert ev(m)==0
 return len(terms)

if __name__=='__main__':
 cert=json.loads((HERE/'certificate_mod3_n7.json').read_text());b7=flip_ball(7,3)
 print('Upper n=7: BFS ball',len(b7),'nonzero-tested monomials',verify_upper(cert,b7))
 corrupt=copy.deepcopy(cert);corrupt['terms'][0]['coefficient']+=1
 try:verify_upper(corrupt,b7)
 except AssertionError:print('Corrupted upper certificate rejected')
 else:raise AssertionError('corruption accepted')
 for n in (5,6):
  w=json.loads((HERE/f'witness_n{n}.json').read_text());b=flip_ball(n,3)
  print('Lower n='+str(n)+': BFS ball',len(b),'polynomial monomials',verify_lower(w,b))
 print('All exact checks passed.')
