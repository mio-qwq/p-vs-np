#!/usr/bin/env python3
"""Known-wrong expected formulas must be rejected, even under python -O."""
from pathlib import Path
import json
import check_independent as full
import check_qclosed as closed

def main():
    found=[]
    original_q=full.qval
    full.qval=lambda a,I,l: -original_q(a,I,l)
    try:
        full.run(full.cases[0])
    except RuntimeError as error:
        if 'candidate mismatch' not in str(error):raise
        found.append({'control':'reverse candidate leading sign','caught':True,'error':str(error)})
    else:raise RuntimeError('negative control incorrectly accepted sign reversal')
    finally:full.qval=original_q

    original_factorial=closed.factorial
    closed.factorial=lambda n:original_factorial(n)+(1 if n==3 else 0)
    try:
        closed.check(3,0,1)
    except RuntimeError as error:
        found.append({'control':'replace third-order factorial by seven','caught':True,'error':str(error)})
    else:raise RuntimeError('negative control incorrectly accepted wrong factorial')
    finally:closed.factorial=original_factorial
    Path(__file__).with_name('negative-control-results.json').write_text(json.dumps(found,indent=2)+'\n')
    print('PASS: two deliberately wrong normalizations were rejected.')

if __name__=='__main__':main()
