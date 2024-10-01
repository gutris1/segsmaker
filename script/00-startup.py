import sys, os
from pathlib import Path
from IPython import get_ipython

home = Path.home()
gutris1 = home / '.gutris1'
marking = gutris1 / 'marking.py'
zrok_bin = home / '.zrok/bin/zrok'
startup = home / '.ipython/profile_default/startup'

sys.path.append(str(startup))
if zrok_bin.exists():
    if 'zrok' not in os.environ.get('PATH', '') or str(zrok_bin.parent) not in os.environ['PATH']:
        zrok_bin.chmod(0o755)
        os.environ['PATH'] += os.pathsep + str(zrok_bin.parent)

if marking.exists():
    get_ipython().run_line_magic('run', f'{marking}')
