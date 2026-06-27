from IPython.display import clear_output, Image, display
from IPython import get_ipython
from pathlib import Path
import subprocess
import shlex
import json
import os

from nenen88 import tempe, say, download

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

def unused_python(py):
    venvs = [TMP / 'venv', TMP / 'venv-comfy-swarm', TMP / 'python311', TMP / 'NEO']
    unused = [v for v in venvs if v != py and v.exists()]
    if unused: SyS(f"rm -rf {' '.join(str(v) for v in unused)}")

def install_python():
    py = UI_CFG[ui]['py']
    if py.exists(): return

    unused_python(py)
    check_pv()

    CD(TMP)

    clear_output(wait=True)
    display(Image(filename=str(IMG)))
    say(f'<b>Installing {ui} Python</b>')

    url = UI_CFG[ui]['url']
    l = zip(url, [Path(u).name for u in url]) if isinstance(url, list) else [(url, Path(url).name)]

    for u, f in l:
        t = TMP / f
        download(u)
        SyS(f'pv "{t}" | lz4 -d | tar xf -')
        t.unlink(missing_ok=True)

    if ui not in ['Forge-Classic', 'Forge-Neo']:
        pi = f'{py}/bin/python3 -m pip install'

        for c in [
            f'rm -f {py}/bin/pip* {py}/bin/python*',
            f'python3 -m venv {py}',
            f'{pi} -U pip'
            f'{pi} ipykernel matplotlib pyyaml',
            f'{pi} -q comfy-aimdo'
        ]: SyS(f'{c} > /dev/null 2>&1')

HOME = Path.home()
SRC = HOME / '.gutris1'
MARK = SRC / 'marking.json'
IMG = SRC / 'loading.png'
TMP = Path('/tmp')
cwd = Path.cwd()

SyS = get_ipython().system
CD = os.chdir

ui = json.load(MARK.open()).get('ui')

URL = {
    'D': [
        'https://huggingface.co/gutris1/webui/resolve/main/env/SSL-Torch2120-cu130-part1.tar.lz4',
        'https://huggingface.co/gutris1/webui/resolve/main/env/SSL-Torch2120-cu130-part2.tar.lz4'
    ],
    'FC': 'https://huggingface.co/gutris1/webui/resolve/main/env/SSL-FC-Python311-Torch260-cu124.tar.lz4',
    'FN': [
        'https://huggingface.co/gutris1/webui/resolve/main/env/SSL-FN-Torch2121-cu130-part1.tar.lz4',
        'https://huggingface.co/gutris1/webui/resolve/main/env/SSL-FN-Torch2121-cu130-part2.tar.lz4'
    ],
    'CS': 'https://huggingface.co/gutris1/webui/resolve/main/env/SSL-ComfyUI-SwarmUI-Torch260-cu124.tar.lz4',
}

UI_CFG = {
    'A1111': {'py': TMP / 'venv', 'url': URL['D']},
    'Forge': {'py': TMP / 'venv', 'url': URL['D']},
    'ReForge': {'py': TMP / 'venv', 'url': URL['D']},
    'ReForge-old': {'py': TMP / 'venv', 'url': URL['D']},
    'Forge-Classic': {'py': TMP / 'python311', 'url': URL['FC']},
    'Forge-Neo': {'py': TMP / 'NEO', 'url': URL['FN']},
    'ComfyUI': {'py': TMP / 'venv-comfy-swarm', 'url': URL['CS']},
    'SwarmUI': {'py': TMP / 'venv-comfy-swarm', 'url': URL['CS']},
}

print('checking python...')
tempe()
trashing()

install_python()

clear_output(wait=True)
aDel()
CD(cwd)
