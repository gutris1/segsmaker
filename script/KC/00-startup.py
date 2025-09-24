from IPython import get_ipython
from pathlib import Path
import json
import sys
import os

iRON = os.environ

def getENV():
    env = {
        'Colab': ('/content', '/content', 'COLAB_JUPYTER_TOKEN'),
        'Kaggle': ('/kaggle', '/kaggle/working', 'KAGGLE_DATA_PROXY_TOKEN')
    }
    for name, (base, home, var) in env.items():
        if var in iRON:
            return name, base, home
    return None, None, None

ENVNAME, ENVBASE, ENVHOME = getENV()

PY = Path('/GUTRIS1')
BIN = str(PY / 'bin')

MRK = Path(ENVHOME) / 'gutris1/marking.py'
JS = Path(ENVHOME) / 'gutris1/marking.json'

ui = json.loads(JS.read_text()).get('ui', '')
hao = ui in ['Forge-Classic', 'Forge-Neo']
v = '3.11' if hao else '3.10'
PKG = str(PY / f'lib/python{v}/site-packages')

sys.path.append('/root/.ipython/profile_default/startup')

if PY.exists():
    sys.path.insert(0, PKG)
    if BIN not in iRON["PATH"]: iRON["PATH"] = BIN + ":" + iRON["PATH"]
    if PKG not in iRON["PYTHONPATH"]: iRON["PYTHONPATH"] = PKG + ":" + iRON["PYTHONPATH"]

if MRK.exists():
    get_ipython().run_line_magic('run', str(MRK))