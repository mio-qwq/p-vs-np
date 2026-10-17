from pathlib import Path
import tempfile,shutil,json,subprocess,sys
here=Path(__file__).resolve().parent
with tempfile.TemporaryDirectory() as td:
 p=Path(td)
 for n in ['check_frozen_four.py','frozen_witnesses.json']:shutil.copy2(here/n,p/n)
 original=json.loads((p/'frozen_witnesses.json').read_text())
 for kind in ['accept_empty','wrong_weight']:
  data=json.loads(json.dumps(original))
  if kind=='accept_empty':data['filter_masks'][-1]=str(int(data['filter_masks'][-1])|1)
  else:data['integer_weights'][0]+=1
  (p/'frozen_witnesses.json').write_text(json.dumps(data))
  result=subprocess.run([sys.executable,str(p/'check_frozen_four.py')],capture_output=True,timeout=20)
  assert result.returncode!=0,kind
  print('PASS rejected',kind)
 source=(here/'verify_upper5.py').read_text()
 assert 'out=pairs[-1][0]&pairs[-1][1]' in source
 (p/'bad_upper.py').write_text(source.replace('out=pairs[-1][0]&pairs[-1][1]','out=pairs[-1][0]|pairs[-1][1]'))
 result=subprocess.run([sys.executable,str(p/'bad_upper.py')],capture_output=True,timeout=20)
 assert result.returncode!=0
 print('PASS rejected incorrect OR output gate')
