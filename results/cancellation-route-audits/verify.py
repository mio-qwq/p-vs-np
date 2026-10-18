#!/usr/bin/env python3
"""Exact frozen-checkpoint verification.

Default: standard-library arithmetic reruns, certificate and inventory checks.
--full: additionally rerun all symbolic source checks; installed SymPy required.
All writes and corruption controls are confined to temporary copies.
"""
import argparse
import copy
import hashlib
import itertools
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent
BASE = 'b4841433f732c0b11bf6fdff5a74ec8e251cb87b'
MODE = int(sys.flags.optimize)
# Filled once from the final selected inventory before freezing.
PAYLOAD = ('PROVENANCE.json', 'README.md', 'RELEASE_NOTES.md', 'STATUS.md', 'five-row/AUDIT.md', 'five-row/PROOF.md', 'five-row/audit_independent.py', 'five-row/audit_independent_receipt.json', 'five-row/audit_next_candidate.py', 'five-row/audit_next_candidate_receipt.json', 'five-row/verification.json', 'five-row/verify.py', 'next-candidate/RESULT.md', 'next-candidate/check.py', 'next-candidate/result.json', 'tied-block/AUDIT.md', 'tied-block/CHECKPOINT.md', 'tied-block/PROOF.md', 'tied-block/RECTANGULAR_OBSTRUCTION.md', 'tied-block/ROOT_REVIEW.md', 'tied-block/SMALL_SQUARE_BACKGROUND.md', 'tied-block/audit-results.json', 'tied-block/audit_exact_checks.py', 'tied-block/check.py', 'tied-block/check_identities.py', 'tied-block/identity-results.json', 'tied-block/results.json', 'verification.json', 'verify.py')
CHECKER_SHA256 = {'tied-block/check.py': '72a682e04a3b1a3311ade98122e2dbb80c9d2da2c3f16821096e2412be8a60f1', 'tied-block/check_identities.py': 'db17b6655d5cc825a8bf7888f982b877dd30eb73e26cbae85e408165a8323869', 'tied-block/audit_exact_checks.py': 'eabc98d778781e1c2965453f544c769e27f2385066a74a0c14ba4099d48d3e5e', 'five-row/verify.py': '17beefc8e6108cbc95081d367176fe9403a00cdbb0a9883a138353ef5bd02484', 'five-row/audit_independent.py': '64c9957cfe9d2213fd376b2ba9e6aa77dffa826a5de127a6b8bbce59c2a042b5', 'five-row/audit_next_candidate.py': 'd721da775b52f66a9035463d94f65c7be2531f36141f5b038257519b5823c5ec', 'next-candidate/check.py': 'e78d95385ab9b78db27f19f0985c25d84b00019929ab317c914cb4b507158d87'}
ALL_FILES = set(PAYLOAD) | {'manifest.json', 'SHA256SUMS'}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    def unique(pairs):
        value = {}
        for key, item in pairs:
            require(key not in value, 'Duplicate JSON key: ' + key)
            value[key] = item
        return value
    def finite(value):
        raise ValueError('Non-finite JSON constant: ' + value)
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique, parse_constant=finite)


def integrity(root):
    actual = set()
    allowed_dirs = {str(PurePosixPath(name).parent) for name in ALL_FILES} - {'.'}
    for item in root.rglob('*'):
        name = item.relative_to(root).as_posix()
        require(not item.is_symlink(), 'Symlink not permitted: ' + name)
        if item.is_dir():
            require(name in allowed_dirs, 'Unexpected directory: ' + name)
        else:
            require(item.is_file(), 'Non-regular file: ' + name)
            actual.add(name)
    require(actual == ALL_FILES, 'File inventory mismatch: missing=' + str(sorted(ALL_FILES-actual)) + ', unexpected=' + str(sorted(actual-ALL_FILES)))
    manifest = read_json(root/'manifest.json')
    require(manifest['schema'] == 'cancellation-route-audits-manifest-v1', 'Manifest schema mismatch')
    require(manifest['algorithm'] == 'sha256' and manifest['expected_base_commit'] == BASE, 'Manifest algorithm/base mismatch')
    require([e['path'] for e in manifest['files']] == sorted(PAYLOAD), 'Manifest inventory mismatch')
    for entry in manifest['files']:
        content = (root/entry['path']).read_bytes()
        require(len(content) == entry['bytes'] and sha(content) == entry['sha256'], 'File size/hash mismatch: ' + entry['path'])
    sums = ''.join(sha((root/name).read_bytes())+'  '+name+'\n' for name in sorted(set(PAYLOAD)|{'manifest.json'}))
    require((root/'SHA256SUMS').read_text(encoding='utf-8') == sums, 'SHA256SUMS mismatch')
    for name, digest in CHECKER_SHA256.items():
        require(sha((root/name).read_bytes()) == digest, 'Original checker changed: ' + name)
    for entry in read_json(root/'PROVENANCE.json')['files']:
        name = entry['packaged_path']
        require(name in ALL_FILES, 'Unknown provenance path: ' + name)
        content = (root/name).read_bytes()
        require(len(content) == entry['packaged_bytes'] and sha(content) == entry['packaged_sha256'], 'Provenance mismatch: ' + name)
        if name in CHECKER_SHA256:
            require(entry['byte_for_byte'] is True and entry['source_sha256'] == sha(content), 'Checker provenance mismatch: ' + name)
    return len(actual)


def internal_links(root):
    checked = 0
    for name in sorted(ALL_FILES):
        if not name.endswith('.md'):
            continue
        path = root/name
        prose = path.read_text(encoding='utf-8')
        prose = re.sub(r'\\\[.*?\\\]|\\\(.*?\\\)', '', prose, flags=re.S)
        prose = re.sub(r'`[^`]*`', '', prose)
        prose = re.sub(r'^(?: {4}|\t).*$', '', prose, flags=re.M)
        for target in re.findall(r'\[[^\]]*\]\(([^\s)]+)\)', prose):
            parts = urlsplit(target)
            if parts.scheme in ('http', 'https'):
                continue
            require(not parts.scheme and not parts.netloc and not parts.path.startswith('/'), 'Non-relative internal link: ' + target)
            if parts.path:
                resolved = (path.parent/unquote(parts.path)).resolve()
                require(resolved.is_relative_to(root.resolve()) and resolved.is_file(), 'Broken or escaping link: ' + name+' -> '+target)
                checked += 1
    return checked


def run(root, script, args=(), expect_success=True):
    flags = ['-B'] + (['-'+'O'*MODE] if MODE else [])
    process = subprocess.run([sys.executable]+flags+[str(root/script)]+list(args), cwd=str((root/script).parent), env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0'), capture_output=True, timeout=900)
    if expect_success:
        require(process.returncode == 0 and not process.stderr, script+' failed: '+process.stderr.decode(errors='replace'))
    return process


def compare(fresh, candidate, label):
    require(fresh == candidate, label + ' differs from exact fresh recomputation')


def rejected_math(fresh, altered, label):
    try:
        compare(fresh, altered, label)
    except ValueError as error:
        require('differs from exact fresh recomputation' in str(error), 'Unexpected mathematical rejection')
        return label
    raise ValueError('Modified mathematical certificate accepted: ' + label)


def engineered_candidate():
    """Raw 5-row permutation/binomial coefficients, independent of SymPy.

    For exponents (0,3,5,8,9), support exponent values {0,3,9}, and
    offsets (0,-1,1,-v,v), recover C0,...,C12 as integer v-polynomials.
    """
    exponents = [0,3,5,8,9]
    keep = {0,1,4}
    coeff = [dict() for _ in range(13)]
    for perm in itertools.permutations(range(5)):
        if perm[0] not in keep:
            continue
        sign = (-1)**sum(perm[i]>perm[j] for i in range(5) for j in range(i+1,5))
        poly = {(0,0):1}
        for row in range(1,5):
            new = {}
            degree = exponents[perm[row]]
            for (order,power), value in poly.items():
                for h in range(min(degree,12-order)+1):
                    key = (order+h,power+(h if row>=3 else 0))
                    term = value*math.comb(degree,h)*((-1)**h if row in (1,3) else 1)
                    new[key] = new.get(key,0)+term
            poly = {k:v for k,v in new.items() if v}
        for (order,power), value in poly.items():
            coeff[order][power] = coeff[order].get(power,0)+sign*value
    coeff = [{str(k):v for k,v in sorted(p.items()) if v} for p in coeff]
    def multiply(a,b):
        out = {}
        for k,v in a.items():
            for l,w in b.items():
                out[k+l] = out.get(k+l,0)+v*w
        return {k:v for k,v in out.items() if v}
    common = multiply({1:1},multiply({2:1,0:-1},{2:1,0:-1}))
    c10 = {str(k):-864*v for k,v in multiply(common,{4:1,2:-9,0:1}).items()}
    c12 = {str(k):36*v for k,v in multiply(multiply(common,{2:1,0:1}),{4:23,2:-282,0:23}).items()}
    require(all(not coeff[k] for k in range(10)) and not coeff[11], 'Engineered candidate earlier coefficient differs')
    compare(coeff[10],c10,'engineered C10')
    compare(coeff[12],c12,'engineered C12')
    def reduce(poly):
        p={int(k):Fraction(v) for k,v in poly.items()}
        for k in range(max(p,default=0),3,-1):
            c=p.pop(k,Fraction(0))
            p[k-2]=p.get(k-2,Fraction(0))+9*c
            p[k-4]=p.get(k-4,Fraction(0))-c
        return {k:v for k,v in p.items() if v}
    require(not reduce(coeff[10]), 'Engineered candidate C10 reduction')
    remainder=reduce(coeff[12])
    expected=multiply({3:-2700},multiply(multiply({2:1,0:-1},{2:1,0:-1}),{2:1,0:1}))
    compare(remainder,reduce(expected),'engineered nonzero C12 reduction')
    require(bool(remainder), 'Engineered candidate lost its surviving coefficient')
    return {'status':'PASS','method':'raw permutation/binomial expansion without symbolic dependencies','coefficients_0_through_12':coeff,'C12_remainder':{str(k):str(v) for k,v in sorted(remainder.items())}}


def mathematics(root, full):
    controls = []
    summary = {}
    with tempfile.TemporaryDirectory(prefix='cancellation-routes-math-') as directory:
        work = Path(directory)/'package'
        shutil.copytree(root,work)
        output = json.loads(run(work,'tied-block/check.py').stdout)
        supplied = read_json(work/'tied-block/results.json')
        compare(supplied,read_json(root/'tied-block/results.json'),'complete bivariate certificate')
        require((work/'tied-block/results.json').read_bytes() == (root/'tied-block/results.json').read_bytes(), 'Bivariate certificate bytes differ')
        compare(output,{g:[{k:v for k,v in c.items() if k!='polynomial'} for c in cases] for g,cases in supplied.items()},'bivariate stdout')
        require(len(supplied['square_cases']) == 5 and len(supplied['rectangle_cases']) == 5,'Bivariate case counts')
        identities = json.loads(run(work,'tied-block/check_identities.py').stdout)
        compare(identities,read_json(root/'tied-block/identity-results.json'),'structural identities')
        independent = json.loads(run(work,'tied-block/audit_exact_checks.py').stdout)
        compare(independent,read_json(root/'tied-block/audit-results.json'),'independent interpolation certificate')
        n8 = next(c for c in supplied['rectangle_cases'] if c['name']=='n8_standard_3x4_top_zero')
        require(n8['candidate_degree']==15 and n8['column_sum']=='0','n8 candidate coefficient')
        require([n8['actual_targets'][str(t)]['degree'] for t in range(4)]==[14]*4,'n8 exact degrees')
        recovered = {f'{power},{t}':str(value) for t,coeffs in enumerate(independent['n8_source_standard']['fiber_coefficients_ascending_lambda']) for power,value in enumerate(coeffs) if value}
        compare(recovered,n8['polynomial'],'all n8 interpolation coefficients')
        require(len(recovered)==58,'n8 nonzero coefficient count')
        next_candidate = json.loads(run(work,'next-candidate/check.py').stdout)
        compare(next_candidate,read_json(root/'next-candidate/result.json'),'next-candidate exact moments')
        require(next_candidate[-1]['moment']==12 and next_candidate[-1]['lambda_degree']==28,'next-candidate first survivor')
        require(all(not c['remainder_mod_209v4_1226v2_209'] for c in next_candidate[:-1]),'next-candidate earlier remainder')
        require(1152**2 < 1226**2-4*209**2 < 1153**2,'next-candidate nonsquare discriminant')
        engineered = engineered_candidate()
        # Deliberately alter numeric certificates after skipping integrity/hashes.
        altered = copy.deepcopy(supplied)
        altered['rectangle_cases'][2]['polynomial']['14,0']='-967679'
        controls.append(rejected_math(supplied,altered,'bivariate_coefficient'))
        altered = copy.deepcopy(independent)
        altered['n8_source_standard']['fiber_coefficients_ascending_lambda'][0][14]+=1
        controls.append(rejected_math(independent,altered,'independent_interpolation_coefficient'))
        altered = copy.deepcopy(next_candidate)
        altered[-1]['remainder_mod_209v4_1226v2_209']['1']='0'
        controls.append(rejected_math(next_candidate,altered,'next_candidate_remainder'))
        altered = copy.deepcopy(engineered)
        altered['coefficients_0_through_12'][12]['1']+=1
        controls.append(rejected_math(engineered,altered,'engineered_candidate_coefficient'))
        summary.update({
            'complete_bivariate_cases':10,'structural_identity_cases':len(identities),
            'independent_quotient_identity_cases':independent['quotient_identity_cases'],
            'independent_weighted_identity_cases':independent['weighted_identity_cases'],
            'independent_minor_first_two_coefficient_cases':independent['translated_minor_first_two_coefficients_cases'],
            'n8_nonzero_coefficients_independently_reconstructed':58,
            'n8_degree':14,'n8_target_leading_coefficients':[-967680,2903040,-2903040,967680],
            'engineered_candidate':engineered,
            'next_candidate':{'first_surviving_moment':12,'lambda_degree':28,'discriminant':1328352,'all_recorded_moments_recomputed':True},
        })
        if full:
            try:
                import sympy
            except ImportError as error:
                raise ValueError('--full requires installed SymPy; no symbolic checks were skipped') from error
            original = json.loads(run(work,'five-row/verify.py').stdout)
            expected = read_json(root/'five-row/verification.json')
            require(original['optimized'] == bool(MODE),'Symbolic checker optimization flag')
            require(original['sympy'] == sympy.__version__,'Symbolic checker SymPy version')
            original_normalized = {k:v for k,v in original.items() if k not in ('optimized','sympy')}
            compare(original_normalized,{k:v for k,v in expected.items() if k not in ('optimized','sympy')},'symbolic source checks')
            require(original['checks']==31,'Symbolic source check count')
            run(work,'five-row/audit_independent.py')
            audit = read_json(work/'five-row/audit_independent_receipt.json')
            expected_audit = read_json(root/'five-row/audit_independent_receipt.json')
            compare({k:v for k,v in audit.items() if k!='sympy'},{k:v for k,v in expected_audit.items() if k!='sympy'},'independent symbolic audit')
            run(work,'five-row/audit_next_candidate.py')
            candidate_audit = read_json(work/'five-row/audit_next_candidate_receipt.json')
            compare({k:v for k,v in candidate_audit.items() if k!='sympy'},{k:v for k,v in read_json(root/'five-row/audit_next_candidate_receipt.json').items() if k!='sympy'},'direct next-candidate determinant audit')
            # This source-provided negative control changes a mathematical identity
            # before checking it, so a hash comparison cannot be its rejection cause.
            negative = run(work,'five-row/verify.py',args=('--negative-control',),expect_success=False)
            require(negative.returncode != 0 and b'C9 after C6,C7,C8: residual = -1' in negative.stderr,'Symbolic C9 negative control not rejected for the expected reason')
            controls.append('symbolic_C9_identity_negative_control')
            summary['symbolic_verification']={'status':'PASS','sympy':sympy.__version__,'original_checks':31,'independent_checks':len(audit['checks']),'direct_next_candidate_determinant':'PASS','source_negative_control':'REJECTED'}
        else:
            summary['symbolic_verification']={'status':'NOT_RUN','reason':'Default mode has no SymPy dependency; use --full to rerun the general symbolic identities and symbolic reviewer checks. Frozen symbolic receipts are hash-checked only in default mode.'}
    summary['modified_mathematical_certificates_rejected']=controls
    summary['mathematical_controls_independent_of_inventory_hashes']=True
    return summary


def corruption_controls(root):
    rejected=[]
    for kind in ('modified_file','missing_file','unexpected_file','altered_manifest'):
        with tempfile.TemporaryDirectory(prefix='cancellation-routes-corruption-') as directory:
            work=Path(directory)/'package'
            shutil.copytree(root,work)
            if kind=='modified_file':
                path=work/'README.md'; path.write_bytes(path.read_bytes()+b'corrupt\n')
            elif kind=='missing_file':
                (work/'next-candidate/result.json').unlink()
            elif kind=='unexpected_file':
                (work/'unlisted.txt').write_text('unexpected\n')
            else:
                path=work/'manifest.json'; data=read_json(path); data['files'][0]['sha256']='0'*64; path.write_text(json.dumps(data))
            try:
                integrity(work)
            except (ValueError,KeyError,OSError):
                rejected.append(kind)
            else:
                raise ValueError('Corruption accepted: '+kind)
    return rejected


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--full',action='store_true',help='Also rerun source symbolic identities and reviewer checks; installed SymPy is required.')
    args=parser.parse_args()
    if args.full:
        # Fail before costly arithmetic if the requested dependency is absent.
        try:
            import sympy
        except ImportError as error:
            raise ValueError('--full requires installed SymPy; install SymPy and rerun. No symbolic checks were skipped.') from error
    count=integrity(ROOT)
    links=internal_links(ROOT)
    mathematical=mathematics(ROOT,args.full)
    corruptions=corruption_controls(ROOT)
    integrity(ROOT)
    print(json.dumps({'status':'PASS','verification_mode':'full' if args.full else 'default','optimization':MODE,'python':sys.version.split()[0],'file_count':count,'integrity':'PASS','internal_relative_links_checked':links,'original_mathematical_checkers_unchanged':True,'source_files_unchanged':True,'mathematical_checks':mathematical,'rejected_packaging_corruptions':corruptions,'scope':'Square reductions, rectangular leading-coefficient route obstruction, five-row necessary conditions, and two exact failed candidates. No identically-zero ASNC polynomial, whole-five-row proof, general ASNC conclusion, or P-versus-NP result.'},indent=2,sort_keys=True))


if __name__=='__main__':
    try:
        main()
    except (ValueError,KeyError,TypeError,OSError,subprocess.SubprocessError) as error:
        print('FAIL: '+str(error),file=sys.stderr)
        sys.exit(1)
