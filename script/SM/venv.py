from IPython.display import clear_output, Image, display
from IPython import get_ipython
from pathlib import Path
import subprocess
import shlex
import json
import os

from nenen88 import tempe, say, download
from _segsmaker_ import HOME, SRC, UID

CD = os.chdir
SyS = get_ipython().system

def _del():
    for n in ['tempe', 'say', 'download']:
        globals().pop(n, None)

def _trash():
    f = ['ckpt', 'lora', 'controlnet', 'svd', 'z123']
    for p in [HOME / ui] + [TMP / d for d in f]:
        SyS(f'find {p} -type d -name .ipynb_checkpoints -exec rm -rf {{}} + > /dev/null 2>&1')

def _check():
    try: subprocess.run(['pv', '-V'], capture_output=True, text=True, check=True)
    except Exception: subprocess.run(['mamba', 'install', '-y', 'pv'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def _unused(env):
    v = [p for d in UID.values() if (p := d['py']['p']) != env and p.exists()]
    if v: SyS(f"rm -rf {' '.join(map(str, v))}")

def _install():
    py = UID[ui]['py']
    env, version, url = py['p'], py['v'], py['url']

    if env.exists(): return

    _unused(env)
    _check()

    clear_output(wait=True)
    say(f"<b>【{{red}} {ui.replace('-', ' ')} Python {version}{{d}} 】{{red}}</b>")

    CD(TMP)

    for u in url if isinstance(url, list) else [url]:
        f = TMP / Path(u).name
        download(u)
        SyS(f"pv '{f}' | lz4 -d | tar xf -")
        f.unlink(missing_ok=True)

MARK = SRC / 'marking.json'
TMP = Path('/tmp')
cwd = Path.cwd()

ui = json.load(MARK.open()).get('ui')

print('checking python...')
tempe()
_trash()

_install()
clear_output(wait=True)

_del()
CD(cwd)
