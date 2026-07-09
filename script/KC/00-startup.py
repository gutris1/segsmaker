from IPython import get_ipython
from pathlib import Path
import json
import sys
import os

from _segsmaker_ import HOME, SRC, UID

iRON = os.environ

MRK = SRC / 'marking.py'
MARK = SRC / 'marking.json'
ui = json.load(MARK.open()).get('ui')

PY = UID[ui]['py']['p']
V = UID[ui]['py']['v']
BIN = str(PY / 'bin')
PKG = str(PY / 'lib' / f"python{V.rsplit('.', 1)[0]}" / 'site-packages')

sys.path.append('/root/.ipython/profile_default/startup')

if PY.exists():
    sys.path.insert(0, PKG)

    if BIN not in iRON.get('PATH', ''): iRON['PATH'] = BIN + ':' + iRON.get('PATH', '')
    if PKG not in iRON.get('PYTHONPATH', ''): iRON['PYTHONPATH'] = PKG + ':' + iRON.get('PYTHONPATH', '')

if MRK.exists(): get_ipython().run_line_magic('run', str(MRK))
