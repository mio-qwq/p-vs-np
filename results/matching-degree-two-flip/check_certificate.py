import json
from pathlib import Path
from itertools import combinations
from collections import deque

def canonical(edges):return tuple(sorted(tuple(sorted(e)) for e in edges))
def bfs():
 start=tuple((i,i+1) for i in range(0,10,2));d={start:0};q=deque([start])
 while q:
  m=q.popleft()
  for i,j in combinations(range(5),2):
   a,b=m[i];c,e=m[j];rest=[x for z,x in enumerate(m) if z not in (i,j)]
   for pair in [((a,c),(b,e)),((a,e),(b,c))]:
    nxt=canonical(rest+list(pair))
    if nxt not in d:d[nxt]=d[m]+1;q.append(nxt)
 assert len(d)==945
 return d

def check(cert,dist):
 target=canonical(cert['target']);D=cert['denominator'];assert D==48 and dist[target]==4
 terms=[]
 for item in cert['terms']:
  c=item['coefficient'];assert type(c)is int
  for raw in item['matchings']:
   m=canonical(raw);assert sorted(v for e in m for v in e)==list(range(10))
   assert dist[m]<=3
   terms.append((c,set(m)))
 target=set(target);edges=list(combinations(range(10),2));count=0
 for degree in range(3):
  for mon in combinations(edges,degree):
   if len({v for e in mon for v in e})!=2*degree:continue
   mon=set(mon);assert D*int(mon<=target)==sum(c for c,m in terms if mon<=m),(degree,mon)
   count+=1
 return count,len(terms)

if __name__=='__main__':
 cert=json.loads(Path(__file__).with_name('orbit_certificate.json').read_text());dist=bfs()
 print('PASS',check(cert,dist),'BFS matching count',len(dist))
 broken=json.loads(json.dumps(cert));broken['terms'][0]['coefficient']+=1
 try:check(broken,dist)
 except AssertionError:print('PASS corrupted coefficient rejected')
 else:raise AssertionError('negative test failed')
