#!/usr/bin/env python3
"""Reproduce the compact gapped and partial-row auxiliary results, exactly.

Python 3.10+; independent tail audit additionally requires SymPy 1.14.0.
All generated artifacts use temporary paths.
The manifest protects the distributed sources, while explicit normal/-O runs and
physical corruption controls exercise the mathematical checkers.
"""
from hashlib import sha256
from pathlib import Path
import json
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
MANIFEST=HERE/'manifest-gapped-20261018.json'
RESULT_DIRS=('monic-four-gapped','monic-one-partial-row')


def require(condition,message):
    if not condition:
        raise RuntimeError(message)


def digest(data): return sha256(data).hexdigest()


def verify_manifest(root,manifest):
    paths=[]
    for item in manifest['files']:
        rel=Path(item['path'])
        require(not rel.is_absolute() and '..' not in rel.parts,'unsafe manifest path')
        require(item['path'] not in paths,'duplicate manifest path')
        paths.append(item['path'])
        p=root/rel
        require(not p.is_symlink(),'manifest source must not be a symlink: '+str(rel))
        data=p.read_bytes()
        require(len(data)==item['bytes'],'manifest size mismatch: '+str(rel))
        require(digest(data)==item['sha256'],'manifest hash mismatch: '+str(rel))
    for name in RESULT_DIRS:
        actual={str(p.relative_to(root)) for p in (root/name).rglob('*') if p.is_file()
                and '__pycache__' not in p.parts and p.suffix!='.pyc'}
        expected={p for p in paths if p.startswith(name+'/')}
        require(actual==expected,'unexpected/missing result files: '+name)
    require(not any((root/name/'exact_certificate.json').exists() for name in RESULT_DIRS),
            'generated certificate must not be distributed in the compact source')


def run(cwd,script,args=(),optimized=False,expected=0):
    env=dict(os.environ)
    env.pop('PYTHONOPTIMIZE',None)
    env['PYTHONDONTWRITEBYTECODE']='1'
    command=[sys.executable,*(['-O'] if optimized else []),str(script),*map(str,args)]
    result=subprocess.run(command,cwd=cwd,env=env,capture_output=True,timeout=900)
    require(result.returncode==expected,'unexpected exit from '+Path(script).name+': '+
            result.stderr.decode('utf-8',errors='replace'))
    return result


def paired_runs(cwd,script,args=()):
    normal=run(cwd,script,args)
    optimized=run(cwd,script,args,optimized=True)
    require(normal.stdout==optimized.stdout,'ordinary/-O stdout differ: '+Path(script).name)
    return {'normal_exit':0,'optimized_exit':0,'normal_optimized_stdout_identical':True,
            'stdout_sha256':digest(normal.stdout),'stdout_bytes':len(normal.stdout)}


def main():
    require(sys.version_info>=(3,10),'Python 3.10+ is required')
    require(importlib.util.find_spec('sympy') is not None,
            'Independent audit requires SymPy 1.14.0; install requirements-gapped-20261018.txt')
    import sympy
    require(sympy.__version__=='1.14.0','This audited reproduction pins SymPy 1.14.0')
    manifest=json.loads(MANIFEST.read_text())
    verify_manifest(HERE,manifest)
    with tempfile.TemporaryDirectory(prefix='gapped-publication-') as temp:
        root=Path(temp)/'results'
        root.mkdir()
        # Copy only these new package sources, even inside the full repository.
        for item in manifest['files']:
            rel=Path(item['path'])
            (root/rel).parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(HERE/rel,root/rel)
        shutil.copyfile(MANIFEST,root/MANIFEST.name)
        verify_manifest(root,manifest)
        gapped=root/'monic-four-gapped'
        partial=root/'monic-one-partial-row'
        generated=json.loads((gapped/'GENERATED.json').read_text())['artifacts']['exact_certificate.json']
        certificate=Path(temp)/'exact_certificate.json'
        other=Path(temp)/'optimized_certificate.json'
        producer=run(gapped,'check_tail_gap.py',('--write',certificate))
        producer_opt=run(gapped,'check_tail_gap.py',('--write',other),optimized=True)
        data=certificate.read_bytes()
        require(len(data)==generated['bytes'] and digest(data)==generated['sha256'],
                'regenerated certificate differs from frozen bytes')
        require(data==other.read_bytes(),'optimized certificate differs from ordinary certificate')
        require(producer.stdout==producer_opt.stdout,'producer ordinary/-O stdout differ')
        cases=json.loads(data)['cases']
        require(len(cases)==8 and sum(len(c['certificates']) for c in cases)==1656,
                'wrong finite certificate count')
        tail_neg=paired_runs(gapped,'check_negative_controls.py',('--certificate',certificate))
        small_order=paired_runs(gapped,'check_symbolic_identities.py')
        identities=paired_runs(partial,'verify_identities.py')
        partial_neg=paired_runs(partial,'check_negative_controls.py')
        # Independent audit descriptor pins the invocation used in this release.
        audit_config=json.loads((gapped/'AUDIT_CONFIG.json').read_text())
        require(Path(audit_config['script']).name==audit_config['script'], 'unsafe audit script path')
        audit_records=[]
        audit_stdout=[]
        audit_generated=[]
        for optimized in (False,True):
            output_dir=Path(temp)/('independent-optimized' if optimized else 'independent-normal')
            output_dir.mkdir()
            replacements={'{certificate}':str(certificate),'{audit_output}':str(output_dir)}
            audit_args=[replacements.get(a,a) for a in audit_config['args']]
            audited=run(gapped,audit_config['script'],audit_args,optimized=optimized)
            raw=(output_dir/'independent_results.json').read_bytes()
            semantic=json.loads(raw)
            semantic.pop('elapsed_seconds',None)
            audit_records.append(semantic)
            normalized=re.sub(rb'complete independent exact audit in [0-9.]+ seconds',
                              b'complete independent exact audit in [elapsed] seconds',audited.stdout)
            audit_stdout.append(normalized)
            audit_generated.append(output_dir)
        require(audit_records[0]==audit_records[1],
                'independent ordinary/-O results differ beyond elapsed time')
        require(audit_stdout[0]==audit_stdout[1],
                'independent ordinary/-O stdout differ beyond elapsed time')
        independent_data=audit_records[0]
        require(independent_data['labelled_counts']['all_labelled_masks']==65536,
                'independent audit omitted labelled masks')
        require(sum(len(c['proofs']) for c in independent_data['cases'])==1656,
                'independent audit omitted symbolic cases')
        semantic_bytes=(json.dumps(independent_data,sort_keys=True,separators=(',',':'))+'\n').encode()
        expected_independent=json.loads((gapped/'GENERATED.json').read_text())['artifacts']['independent_results.json']
        require(digest(semantic_bytes)==expected_independent['semantic_sha256_excluding_elapsed_seconds'],
                'independent mathematical output differs from frozen expected hash')
        for optimized,output_dir in zip((False,True),audit_generated):
            bad_dir=Path(temp)/('independent-bad-optimized' if optimized else 'independent-bad-normal')
            bad_dir.mkdir()
            bad_args=('--certificate',output_dir/'corrupt_certificate.json','--output-dir',bad_dir)
            bad=run(gapped,audit_config['script'],bad_args,optimized=optimized,expected=1)
            require(b'Stored direct coefficient is incorrect' in bad.stderr,
                    'independent physical corruption failed for an unexpected reason')
        empty=Path(temp)/'empty_certificate.json'
        empty.write_text('{}\n')
        for optimized in (False,True):
            bad_args=('--certificate',empty,'--output-dir',Path(temp)/'malformed-output')
            bad=run(gapped,audit_config['script'],bad_args,optimized=optimized,expected=1)
            require(b'Malformed saved certificate' in bad.stderr,
                    'empty certificate was not rejected for its malformed structure')
        independent={
          'normal_exit':0,'optimized_exit':0,
          'normal_optimized_mathematical_results_identical':True,
          'normal_optimized_stdout_identical_except_elapsed_time':True,
          'normalized_stdout_sha256':digest(audit_stdout[0]),
          'semantic_results_sha256':digest(semantic_bytes),
          'semantic_normalization':'Remove only elapsed_seconds; compact JSON with sorted keys and final newline',
          'physical_corrupt_certificate_rejected_normal_and_optimized':True,
          'malformed_empty_certificate_rejected_normal_and_optimized':True,
          'all_labelled_masks':65536,
        }
        target=partial/'README.md'
        old=target.read_bytes()
        target.write_bytes(old+b'\nDeliberate publication manifest corruption.\n')
        try:
            verify_manifest(root,manifest)
        except RuntimeError as error:
            require('manifest ' in str(error),'wrong manifest negative-control failure')
        else:
            raise RuntimeError('manifest accepted an altered proof')
        target.write_bytes(old)
        verify_manifest(root,manifest)
        result={
          'status':'PASS',
          'arithmetic':'Exact integers/Fraction in primary checkers; independent tail audit uses SymPy 1.14.0 exact rational polynomials',
          'clean_temporary_copy':True,
          'manifest_files_verified':len(manifest['files']),
          'generated_certificates_excluded_from_source':True,
          'manifest_corruption_rejected':True,
          'tail_gap':{
            'symbolic_cases':1656,
            'finite_tail_exponents':list(range(4,12)),
            'certificate_bytes':len(data),
            'certificate_sha256':digest(data),
            'certificate_ordinary_optimized_byte_identical':True,
            'producer_ordinary_optimized_stdout_identical':True,
            'producer_stdout_sha256':digest(producer.stdout),
            'negative_controls':tail_neg,
            'small_order_symbolic_identities':small_order,
            'independent_audit':independent,
          },
          'one_partial_row':{'coefficientwise_identities':38,
                             'exact_identity_checks':identities,'negative_controls':partial_neg},
          'proof_scope':'Auxiliary determinant theorems only; no P-versus-NP, ASNC, novelty, human-review, or Lean claim.',
        }
    verify_manifest(HERE,manifest)
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':main()
