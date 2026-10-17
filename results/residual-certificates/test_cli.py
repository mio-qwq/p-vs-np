"""Check clean rejection of malformed external CLI inputs (no broad catches)."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile

base = Path(__file__).resolve().parent
cases = [[], None, 3, {}, {'clauses': [], 'unknown': True}, {'clauses': [[True]]}]
for data in cases:
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', dir=base) as f:
        json.dump(data, f)
        f.flush()
        result = subprocess.run([sys.executable, str(base/'residual_certificate.py'), 'generate', f.name], capture_output=True, text=True)
        assert result.returncode == 1 and result.stderr.startswith('REJECTED: ') and 'Traceback' not in result.stderr, result
print('6 malformed CLI input cases cleanly rejected')
