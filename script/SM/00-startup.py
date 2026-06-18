from IPython import get_ipython
from pathlib import Path
import sys
import os

iRON = os.environ

home = Path.home()
m = home / '.gutris1/marking.py'
zrok = home / '.zrok2/zrok2'
ngrok = home / '.ngrok/ngrok'
startup = home / '.ipython/profile_default/startup'
sys.path.append(str(startup))

if zrok.exists() and str(zrok.parent) not in iRON.get('PATH', ''):
    zrok.chmod(0o755)
    iRON['PATH'] += ':' + str(zrok.parent)

if ngrok.exists() and str(ngrok.parent) not in iRON.get('PATH', ''):
        ngrok.chmod(0o755)
        iRON['PATH'] += ':' + str(ngrok.parent)

if m.exists(): get_ipython().run_line_magic('run', str(m))
