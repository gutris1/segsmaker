from IPython import get_ipython
from pathlib import Path
import sys, os

ENVHOME = None
env_list = {
    'Colab': ('/content', '/content', 'COLAB_JUPYTER_TOKEN'),
    'Kaggle': ('/kaggle', '/kaggle/working', 'KAGGLE_DATA_PROXY_TOKEN')
}
for envname, (envbase, envhome, envvar) in env_list.items():
    if envvar in os.environ:
        ENVHOME = envhome
        break

HOME = Path(ENVHOME)
SRC = HOME / 'gutris1'
MRK = SRC / 'marking.py'
STR = Path('/root/.ipython/profile_default/startup')

sys.path.append(str(STR))
if MRK.exists():
    get_ipython().run_line_magic('run', f'{MRK}')
