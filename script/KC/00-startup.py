from IPython import get_ipython
from pathlib import Path
import json
import sys
import os

ENVNAME, ENVBASE, ENVHOME = None, None, None
env_list = {
    'Colab': ('/content', '/content', 'COLAB_JUPYTER_TOKEN'),
    'Kaggle': ('/kaggle', '/kaggle/working', 'KAGGLE_DATA_PROXY_TOKEN')
}
for envname, (envbase, envhome, envvar) in env_list.items():
    if envvar in os.environ:
        ENVNAME = envname
        ENVBASE = envbase
        ENVHOME = envhome
        break

iRON = os.environ

PY = Path('/GUTRIS1')
BIN = str(PY / 'bin')

MRK = Path(ENVHOME) / 'gutris1/marking.py'
JS = Path(ENVHOME) / 'gutris1/marking.json'

ui = json.loads(JS.read_text()).get('ui', '')
v = '3.11' if webui == 'Forge-Classic' else '3.10'
PKG = str(PY / f'lib/python{v}/site-packages')

STR = str(Path.home() / '.ipython/profile_default/startup')
sys.path.append(STR)

if PY.exists():
    sys.path.insert(0, PKG)
    if BIN not in iRON["PATH"]: iRON["PATH"] = BIN + ":" + iRON["PATH"]
    if PKG not in iRON["PYTHONPATH"]: iRON["PYTHONPATH"] = PKG + ":" + iRON["PYTHONPATH"]

if MRK.exists():
    get_ipython().run_line_magic('run', str(MRK))