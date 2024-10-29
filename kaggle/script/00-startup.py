import sys, os
from pathlib import Path
from IPython import get_ipython

env, HOME = 'Unknown', None
env_list = {'Colab': '/content', 'Kaggle': '/kaggle/working'}

for env_name, path in env_list.items():
    if os.getenv(env_name.upper() + '_JUPYTER_TRANSPORT') or os.getenv(env_name.upper() + '_DATA_PROXY_TOKEN'):
        env, HOME = env_name, path
        break

HOME = Path(HOME)
SRC = HOME / 'gutris1'
MRK = SRC / 'marking.py'
STR = Path('/root/.ipython/profile_default/startup')

sys.path.append(str(STR))
#if marking.exists():
    #get_ipython().run_line_magic('run', f'{marking}')
