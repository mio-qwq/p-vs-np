from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parent.parent
COMMANDS=['colorful-parity/test.py', 'colorful-parity/test_cover.py', 'colorful-parity/test_general.py', 'colorful-parity/audit-colorful/check.py', 'colorful-parity/audit-colorful/check_hash.py', 'colorful-parity/audit-colorful/check_root.py', 'colorful-parity/audit-cover/check.py', 'colorful-parity/audit-general/check.py', 'matching-polynomial-radius/support-upper/check.py', 'matching-polynomial-radius/support-char2/check.py', 'matching-polynomial-radius/flip-radius/check.py', 'permutation-cayley-radius/transposition_radius_test.py', 'permutation-cayley-radius/audit/check.py']
for name in COMMANDS:
 print("CHECK",name,flush=True)
 f=ROOT/name
 r=subprocess.run([sys.executable,str(f)],cwd=f.parent,capture_output=True,text=True)
 print(r.stdout,flush=True)
 if r.returncode:print(r.stderr);raise SystemExit(r.returncode)
print("ALL 13 CHECKS PASSED",flush=True)
