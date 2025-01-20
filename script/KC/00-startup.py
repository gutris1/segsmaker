from IPython import get_ipython
from pathlib import Path
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

ROOT = Path.home()
SRE = ROOT / 'GUTRIS1'
BIN = str(SRE / 'bin')
PKG = str(SRE / 'lib/python3.10/site-packages')

MRK = Path(ENVHOME) / 'gutris1/marking.py'
STR = str(ROOT / '.ipython/profile_default/startup')

iRON = os.environ

sys.path.append(STR)

if SRE.exists():
    if BIN not in iRON["PATH"]:
        iRON["PATH"] = BIN + ":" + iRON["PATH"]

    if PKG not in iRON["PYTHONPATH"]:
        iRON["PYTHONPATH"] = PKG + ":" + iRON["PYTHONPATH"]

if MRK.exists():
    get_ipython().run_line_magic('run', str(MRK))
