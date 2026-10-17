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
# Construct raw JSON so the test runner itself need not disable its own limit.
# Valid input has two literals and one distinct variable, despite its long label.
with tempfile.TemporaryDirectory(dir=base) as directory:
    directory = Path(directory)
    source = directory / 'large-label.json'
    certificate = directory / 'certificate.json'
    huge = '1' + '0' * 4999
    source.write_text('{"clauses": [[' + huge + '], [-' + huge + ']]}')
    generated = subprocess.run([sys.executable, str(base/'residual_certificate.py'),
                                'generate', str(source)], capture_output=True, text=True)
    assert generated.returncode == 0, generated
    cert = json.loads(generated.stdout)
    assert cert['root'] is None and cert['nodes'] == [], cert
    certificate.write_text(generated.stdout)
    checked = subprocess.run([sys.executable, str(base/'residual_certificate.py'),
                              'check', str(source), str(certificate)], capture_output=True, text=True)
    assert checked.returncode == 0, checked
    # An equally long *dimension* is invalid and must reach the explicit bound
    # check, rather than fail in JSON parsing or trigger dimension-sized work.
    malformed = json.loads((base/'shared.certificate.json').read_text())
    malformed['nodes'][0]['dimension'] = 'OVERSIZED_DIMENSION'
    certificate.write_text(json.dumps(malformed).replace('"OVERSIZED_DIMENSION"', huge))
    rejected = subprocess.run([sys.executable, str(base/'residual_certificate.py'),
                               'check', str(base/'shared.input.json'), str(certificate)],
                              capture_output=True, text=True)
    assert rejected.returncode == 1 and rejected.stderr.strip() == 'REJECTED: dimension bound', rejected
print('6 malformed CLI input shapes rejected; 5000-digit sparse-label generation/check accepted; 5000-digit certificate dimension rejected by explicit bound')
