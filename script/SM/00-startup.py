from IPython import get_ipython
from pathlib import Path
import sys
import os

iRON = os.environ

HOME = Path.home()
MARK = HOME / '.gutris1/marking.py'
zrok = HOME / '.zrok2/zrok2'
ngrok = HOME / '.ngrok/ngrok'

sys.path.append(str(HOME / '.ipython/profile_default/startup'))

if zrok.exists() and str(zrok.parent) not in iRON.get('PATH', ''):
    iRON['PATH'] += ':' + str(zrok.parent)
    zrok.chmod(0o755)

if ngrok.exists() and str(ngrok.parent) not in iRON.get('PATH', ''):
    iRON['PATH'] += ':' + str(ngrok.parent)
    ngrok.chmod(0o755)

if MARK.exists(): get_ipython().run_line_magic('run', str(MARK))
