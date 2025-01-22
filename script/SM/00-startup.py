from IPython import get_ipython
from pathlib import Path
import sys
import os

home = Path.home()
marking = home / '.gutris1/marking.py'
zrok_bin = home / '.zrok/bin/zrok'
ngrok_bin = home / '.ngrok/bin/ngrok'
startup = home / '.ipython/profile_default/startup'

iRON = os.environ

sys.path.append(str(startup))

if zrok_bin.exists() and str(zrok_bin.parent) not in iRON.get('PATH', ''):
    zrok_bin.chmod(0o755)
    iRON['PATH'] += ':' + str(zrok_bin.parent)

if ngrok_bin.exists() and str(ngrok_bin.parent) not in iRON.get('PATH', ''):
        ngrok_bin.chmod(0o755)
        iRON['PATH'] += ':' + str(ngrok_bin.parent)

if marking.exists(): get_ipython().run_line_magic('run', str(marking))
