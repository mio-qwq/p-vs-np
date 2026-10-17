"""Run packaged regressions; validation oracles may be exponential on larger inputs."""
from pathlib import Path
import subprocess, sys
ROOT=Path(__file__).resolve().parent
COMMANDS=['base/test.py', 'base/test_distance_two.py', 'quota/test_quota.py', 'blossom/test_blossom.py', 'blossom/test_nested.py', 'blossom/test_integration.py', 'pair/test.py', 'pair/test_certificate.py', 'star/test.py', 'audit-local/check_matching_gadget.py', 'audit-local/check_hardness_transforms.py', 'audit-pair/check.py', 'audit-star/check_simultaneous.py']
for name in COMMANDS:
 print("CHECK", name, flush=True)
 subprocess.run([sys.executable,str(ROOT/name)],cwd=ROOT/name.rsplit("/",1)[0],check=True)
print("ALL 13 CHECKS PASSED",flush=True)
