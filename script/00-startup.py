import sys, os
from pathlib import Path

sys.path.append("/home/studio-lab-user/.ipython/profile_default/startup")

zrok_bin = Path('/home/studio-lab-user/.zrok/bin/zrok')
if zrok_bin.exists():
    if 'zrok' not in os.environ.get('PATH', '') or str(zrok_bin.parent) not in os.environ['PATH']:
        os.system(f'chmod +x {zrok_bin}')
        os.environ['PATH'] += os.pathsep + str(zrok_bin.parent)
else:
    pass
