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
HOME = Path(ENVHOME)
SRC = HOME / 'gutris1'
MRK = SRC / 'marking.py'
STR = ROOT / '.ipython/profile_default/startup'

iRON = os.environ

if ENVNAME == 'Colab':
    bi = ROOT / 'GUTRIS1/bin'
    iRON["PATH"] = str(bi) + ":" + iRON["PATH"]
    iRON["PYTHONPATH"] = str(bi) + ":" + iRON.get("PYTHONPATH", "")

sys.path.append(str(STR))

if MRK.exists():
    get_ipython().run_line_magic('run', str(MRK))
