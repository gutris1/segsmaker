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

vnv_FF = tmp / 'venv-fusion'
vnv_SDT = tmp / 'venv-sd-trainer'
vnv_C = tmp / 'venv-comfy-swarm'
vnv_FC = tmp / 'python311'
vnv_D = tmp / 'venv'

SyS = get_ipython().system
CD = os.chdir

def aDel():
    for name in ['tempe', 'say', 'download']:
        if name in globals():
            del globals()[name]

def trashing():
    dirs1 = ['A1111', 'Forge', 'ReForge', 'Forge-Classic', 'ComfyUI', 'SwarmUI', 'FaceFusion', 'SDTrainer']
    dirs2 = ['ckpt', 'lora', 'controlnet', 'svd', 'z123']

    paths = [HOME / name for name in dirs1] + [tmp / name for name in dirs2]
    for path in paths:
        cmd = f'find {path} -type d -name .ipynb_checkpoints -exec rm -rf {{}} +'
        SyS(f'{cmd} >/dev/null 2>&1')

def check_pv():
    try:
        cmd = 'pv -V'
        subprocess.run(shlex.split(cmd), capture_output=True, text=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        cmd = 'mamba install -y pv'
        subprocess.run(shlex.split(cmd), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def check_venv(folder):
    return int(du[0].split()[0]) if (du := get_ipython().getoutput(f'du -s -b {folder}')) else 0

def check_tmp(path):
    return (stats := os.statvfs(path)).f_frsize * stats.f_bavail

def listing(directory):
    return [(path := Path(root) / file, path.stat().st_size) for root, _, files in os.walk(directory) for file in files]

def removing(directory, req_space):
    files = listing(directory)
    files.sort(key=lambda x: x[1], reverse=True)
    freed_space = 0

    for file_path, size in files:
        if freed_space >= req_space:
            break

        print(f'Removing {file_path}')
        SyS(f'rm -rf {file_path}')
        freed_space += size
    return freed_space

def unused_venv(vnv):
    vl = [vnv_FF, vnv_SDT, vnv_D, vnv_C, vnv_FC]
    vd = [v for v in vl if v != vnv and v.exists()]
    if vd:
        rmf = f"rm -rf {' '.join(f'{v}/* {v}' for v in vd)}"
        SyS(rmf)

def load_config():
    config = json.load(MARK.open('r')) if MARK.exists() else {}
    ui = config.get('ui')

    if ui == 'FaceFusion':
        url = 'https://huggingface.co/gutris1/webui/resolve/main/env/venv-fusion.tar.lz4'
        need_space = 13 * 1024**3
        vnv = vnv_FF
    elif ui == 'SDTrainer':
        url = 'https://huggingface.co/gutris1/webui/resolve/main/env/venv-sd-trainer.tar.lz4'
        need_space = 14 * 1024**3
        vnv = vnv_SDT
    elif ui in ['ComfyUI', 'SwarmUI']:
        url = 'https://huggingface.co/gutris1/webui/resolve/main/env/SSL-ComfyUI-SwarmUI-Torch260-cu124.tar.lz4'
        need_space = 14 * 1024**3
        vnv = vnv_C
    elif ui == 'Forge-Classic':
        url = 'https://huggingface.co/gutris1/webui/resolve/main/env/SSL-FC-Python311-Torch260-cu124.tar.lz4'
        need_space = 14 * 1024**3
        vnv = vnv_FC
    else:
        url = 'https://huggingface.co/gutris1/webui/resolve/main/env/SSL-Torch260-cu124.tar.lz4'
        need_space = 14 * 1024**3
        vnv = vnv_D

    fn = Path(url).name
    return ui, url, need_space, vnv, fn

def install_venv(ui, url, need_space, vnv, fn):
    unused_venv(vnv)
    check_pv()

    clear_output(wait=True)
    display(Image(filename=str(IMG)))

    free_space = check_tmp(tmp)
    req_space = need_space - free_space

    if req_space > 0:
        print(f'Need space {req_space / 1024**3:.1f} GB for VENV')
        for path in [tmp / 'ckpt', tmp / 'lora', tmp / 'controlnet', tmp / 'clip', tmp / 'unet']:
            if req_space > 0: req_space -= removing(path, req_space)

    CD(tmp)
    msg = 'Installing Forge Classic Python 3.11.13' if ui == 'Forge-Classic' else f'Installing {ui} VENV'
    say(f'<b>【{{red}} {msg}{{d}} 】{{red}}</b>')
    download(url)

    SyS(f'pv {fn} | lz4 -d | tar xf -')
    Path(fn).unlink()

    if ui != 'Forge-Classic':
        for cmd in [
            f'rm -f {vnv}/bin/pip* {vnv}/bin/python*',
            f'python3 -m venv {vnv}',
            f'{pip} install -U --force-reinstall pip',
            f'{pip} install ipykernel matplotlib',
            f'{pip} uninstall -y ngrok pyngrok'
        ]: SyS(f'{cmd} >/dev/null 2>&1')

print('checking env...')
tempe()

ui, url, need_space, vnv, fn = load_config()
pip = f'{vnv}/bin/python3 -m pip'

if not vnv.exists(): install_venv(ui, url, need_space, vnv, fn)

clear_output(wait=True)
trashing()
aDel()
CD(cwd)