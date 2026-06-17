from IPython.display import clear_output, Image, display
from IPython import get_ipython
from pathlib import Path
import subprocess
import shlex
import json
import os

from nenen88 import tempe, say, download

HOME = Path.home()
SRC = HOME / '.gutris1'
MARK = SRC / 'marking.json'
IMG = SRC / 'loading.png'

tmp = Path('/tmp')
cwd = Path.cwd()

vnv_D = tmp / 'venv'
vnv_C = tmp / 'venv-comfy-swarm'
vnv_FC = tmp / 'python311'

SyS = get_ipython().system
CD = os.chdir

def aDel():
    for name in ['tempe', 'say', 'download']:
        globals().pop(name, None)

def trashing():
    dirs1 = ['A1111', 'Forge', 'ReForge', 'Forge-Classic', 'ComfyUI', 'SwarmUI']
    dirs2 = ['ckpt', 'lora', 'controlnet', 'svd', 'z123']

    for path in [HOME / d for d in dirs1] + [tmp / d for d in dirs2]:
        SyS(f'find {path} -type d -name .ipynb_checkpoints -exec rm -rf {{}} + > /dev/null 2>&1')

def check_pv():
    try:
        cmd = 'pv -V'
        subprocess.run(shlex.split(cmd), capture_output=True, text=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        cmd = 'mamba install -y pv'
        subprocess.run(shlex.split(cmd), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def unused_venv(vnv):
    venvs = [vnv_D, vnv_C, vnv_FC]
    unused = [v for v in venvs if v != vnv and v.exists()]

    if unused:
        SyS(f"rm -rf {' '.join(f'{v}/* {v}' for v in unused)}")

def load_config():
    config = json.load(MARK.open('r')) if MARK.exists() else {}
    ui = config.get('ui')

    if ui in ['ComfyUI', 'SwarmUI']:
        url = 'https://huggingface.co/gutris1/webui/resolve/main/env/SSL-ComfyUI-SwarmUI-Torch260-cu124.tar.lz4'
        vnv = vnv_C

    elif ui == 'Forge-Classic':
        url = 'https://huggingface.co/gutris1/webui/resolve/main/env/SSL-FC-Python311-Torch260-cu124.tar.lz4'
        vnv = vnv_FC

    else:
        url = [
            'https://huggingface.co/gutris1/webui/resolve/main/env/SSL-Torch2120-cu130-part1.tar.lz4',
            'https://huggingface.co/gutris1/webui/resolve/main/env/SSL-Torch2120-cu130-part2.tar.lz4'
        ]
        vnv = vnv_D

    fn = [Path(u).name for u in url] if isinstance(url, list) else Path(url).name
    return ui, url, vnv, fn

def install_venv(ui, url, vnv, fn):
    unused_venv(vnv)
    check_pv()

    clear_output(wait=True)
    display(Image(filename=str(IMG)))

    CD(HOME)

    msg = 'Installing Forge Classic Python 3.11.13' if ui == 'Forge-Classic' else f'Installing {ui} VENV'
    say(f'<b>【{{red}} {msg}{{d}} 】{{red}}</b>')

    if isinstance(url, list):
        for u, f in zip(url, fn):
            download(u)
            SyS(f'cd {tmp} && pv "{HOME / f}" | lz4 -d | tar xf -')
            Path(HOME / f).unlink(missing_ok=True)

    else:
        download(url)
        SyS(f'cd {tmp} && pv "{HOME / fn}" | lz4 -d | tar xf -')
        Path(HOME / fn).unlink(missing_ok=True)

    if ui != 'Forge-Classic':
        for cmd in [
            f'rm -f {vnv}/bin/pip* {vnv}/bin/python*',
            f'python3 -m venv {vnv}',
            f'{pip} install -U --force-reinstall pip',
            f'{pip} install ipykernel matplotlib pyyaml',
            f'{pip} install -q comfy-aimdo'
        ]:
            SyS(f'{cmd} > /dev/null 2>&1')

print('checking env...')
tempe()

ui, url, vnv, fn = load_config()
pip = f'{vnv}/bin/python3 -m pip'

if not vnv.exists():
    install_venv(ui, url, vnv, fn)

clear_output(wait=True)
trashing()
aDel()
CD(cwd)
