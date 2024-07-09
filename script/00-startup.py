import sys, os
from pathlib import Path
from IPython import get_ipython

home = Path.home()
src = home / '.gutris1'
mark = src / 'marking.py'
zrok_bin = home / '.zrok/bin/zrok'
startup = home / '.ipython/profile_default/startup'

sys.path.append(str(startup))

if zrok_bin.exists():
    if 'zrok' not in os.environ.get('PATH', '') or str(zrok_bin.parent) not in os.environ['PATH']:
        zrok_bin.chmod(0o755)
        os.environ['PATH'] += os.pathsep + str(zrok_bin.parent)

if mark.exists():
    get_ipython().magic(f"run {mark}")

get_ipython().magic(f"run ~/.ipython/profile_default/startup/py.py")