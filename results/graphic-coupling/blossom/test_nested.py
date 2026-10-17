"""Instrument without modifying backend to prove nested contraction execution."""
import inspect
import random
import sys
from collections import Counter
from itertools import combinations
from blossom import maximum_matching, verify_matching

source, first_line = inspect.getsourcelines(maximum_matching)
contraction_line = next(first_line+i for i,line in enumerate(source) if 'for w in range(n):' in line)
coverage = {'contractions':0,'nested_contractions':0}

def tracer(frame,event,arg):
    if event=='line' and frame.f_code.co_name=='augment_from' and frame.f_lineno==contraction_line:
        # This line repeats during its loop, so count only entry from mark_arm.
        previous = tracer.previous
        if previous != contraction_line and previous == contraction_line-1:
            groups=Counter(frame.f_locals['base'])
            marked=frame.f_locals['in_blossom']
            coverage['contractions']+=1
            if any(size>1 and marked[base] for base,size in groups.items()):
                coverage['nested_contractions']+=1
        tracer.previous=contraction_line
    elif frame.f_code.co_name=='augment_from' and event=='line':
        tracer.previous=frame.f_lineno
    return tracer
tracer.previous=-1

# Two concentric alternating odd cycles: the inner triangle is contracted
# before its base participates in the outer cycle.
n=9
edges=[(0,1),(1,2),(2,0),(2,3),(3,4),(4,5),(5,6),(6,0),(3,7),(7,8)]
rng=random.Random(715)
for attempt in range(1000):
    perm=list(range(n));rng.shuffle(perm)
    relabelled=[(perm[u],perm[v]) for u,v in edges]
    sys.settrace(tracer)
    mate=maximum_matching(n,relabelled)
    sys.settrace(None)
    assert verify_matching(n,relabelled,mate)
    if coverage['nested_contractions']:
        assert sum(u!=-1 for u in mate)//2==4
        print('PASS',coverage,'attempts=',attempt+1)
        print('Nested contraction fixture:',n,relabelled)
        break
else:
    raise AssertionError(('No nested contraction observed',coverage))
