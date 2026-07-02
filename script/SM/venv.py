from IPython.display import clear_output, Image, display
from IPython import get_ipython
from pathlib import Path
import subprocess
import shlex
import json
import os

from nenen88 import tempe, say, download
from ssl_uid import UID

SyS = get_ipython().system
CD = os.chdir

HOME = Path.home()
SRC = HOME / '.gutris1'
MARK = SRC / 'marking.json'
TMP = Path('/tmp')
cwd = Path.cwd()

ui = json.load(MARK.open()).get('ui')

def aDel():
    for name in ['tempe', 'say', 'download']:
        globals().pop(name, None)

def trashing():
    f = ['ckpt', 'lora', 'controlnet', 'svd', 'z123']
    for p in [HOME / ui] + [TMP / d for d in f]:
        SyS(f'find {p} -type d -name .ipynb_checkpoints -exec rm -rf {{}} + > /dev/null 2>&1')

def check_pv():
    try:
        subprocess.run(['pv', '-V'], capture_output=True, text=True, check=True)
    except Exception:
        subprocess.run(['mamba', 'install', '-y', 'pv'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def unused_python(env):
    unused = [d['env'] for d in UID.values() if d['env'] != env and d['env'].exists()]
    if unused: SyS(f"rm -rf {' '.join(map(str, unused))}")

def install_python():
    env = UID[ui]['env']
    if env.exists(): return

    unused_python(env)
    check_pv()

    CD(TMP)

    clear_output(wait=True)
    say(f"<b>【{{red}} Installing {ui.replace('-', ' ')} Python{{d}} 】{{red}}</b>")

    url = UID[ui]['url']
    l = zip(url, [Path(u).name for u in url]) if isinstance(url, list) else [(url, Path(url).name)]

    for u, f in l:
        t = TMP / f
        download(u)
        SyS(f'pv "{t}" | lz4 -d | tar xf -')
        t.unlink(missing_ok=True)

    if ui not in ['Forge-Classic', 'Forge-Neo']:
        pi = f'{env}/bin/python3 -m pip install'

        for c in [
            f'rm -f {env}/bin/pip* {env}/bin/python*',
            f'python3 -m venv {env}',
            f'{pi} -U pip',
            f'{pi} ipykernel matplotlib pyyaml',
            f'{pi} -q comfy-aimdo'
        ]:
            SyS(f'{c} > /dev/null 2>&1')

print('checking python...')
tempe()
trashing()

install_python()

clear_output(wait=True)
aDel()
CD(cwd)
