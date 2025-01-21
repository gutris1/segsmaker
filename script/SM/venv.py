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
vnv_D = tmp / 'venv'

SyS = get_ipython().system
CD = os.chdir

def aDel():
    for name in ['tempe', 'say', 'download']:
        if name in globals():
            del globals()[name]

def load_config():
    config = json.load(MARK.open('r')) if MARK.exists() else {}
    ui = config.get('ui')

    if ui == 'FaceFusion':
        url = 'https://huggingface.co/pantat88/back_up/resolve/main/venv-fusion.tar.lz4'
        need_space = 13 * 1024**3
        vnv = vnv_FF
    elif ui == 'SDTrainer':
        url = 'https://huggingface.co/pantat88/back_up/resolve/main/venv-sd-trainer.tar.lz4'
        need_space = 14 * 1024**3
        vnv = vnv_SDT
    else:
        url = 'https://huggingface.co/pantat88/back_up/resolve/main/venv-torch251-cu121-SSL.tar.lz4'
        need_space = 14 * 1024**3
        vnv = vnv_D

    fn = Path(url).name
    return ui, url, need_space, vnv, fn

def unused_venv():
    if any(venv.exists() for venv in [vnv_FF, vnv_SDT, vnv_D]):
        vnv_list = {
            vnv_FF: [vnv_SDT, vnv_D],
            vnv_SDT: [vnv_FF, vnv_D],
            vnv_D: [vnv_FF, vnv_SDT]
        }.get(vnv)

        if vnv_list:
            rmf = f'rm -rf {" ".join(f"{venv}/* {venv}" for venv in vnv_list)}'
            SyS(rmf)

def check_venv(folder):
    du = get_ipython().getoutput(f'du -s -b {folder}')
    return int(du[0].split()[0]) if du else 0

def check_tmp(path):
    stats = os.statvfs(path)
    return stats.f_frsize * stats.f_bavail

def listing(directory):
    return [(Path(root) / file, (Path(root) / file).stat().st_size) 
            for root, _, files in os.walk(directory) for file in files]

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

def trashing():
    dirs1 = ["A1111", "Forge", "ComfyUI", "ReForge", "FaceFusion", "SDTrainer", "SwarmUI"]
    dirs2 = ["ckpt", "lora", "controlnet", "svd", "z123"]

    paths = [HOME / name for name in dirs1] + [tmp / name for name in dirs2]
    for path in paths:
        cmd = f"find {path} -type d -name .ipynb_checkpoints -exec rm -rf {{}} +"
        SyS(f'{cmd}>/dev/null 2>&1')

def check_pv():
    try:
        subprocess.run(
            shlex.split('pv -V'),
            capture_output=True,
            text=True,
            check=True
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        subprocess.run(
            shlex.split('conda install -qy pv'),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

def venv_exists(vnv, ui):
    if vnv.exists():
        size = check_venv(vnv)
        if (ui == 'FaceFusion' and size < 7 * 1024**3) or size > 7 * 1024**3:
            return True
    return False

def install_venv(ui, url, need_space, fn):
    clear_output(wait=True)
    display(Image(filename=str(IMG)))

    free_space = check_tmp(tmp)
    req_space = need_space - free_space

    if req_space > 0:
        print(f'Need space {req_space / 1024**3:.1f} GB for VENV')
        for path in [tmp / 'ckpt', tmp / 'lora', tmp / 'controlnet', tmp / 'clip', tmp / 'unet']:
            if req_space > 0:
                req_space -= removing(path, req_space)

    CD(tmp)
    say('<b>【{red} Installing VENV{d} 】{red}</b>')
    check_pv()
    download(url)

    SyS(f'pv {fn} | lz4 -d | tar xf -')
    Path(fn).unlink()

    req = [
        f'rm -f {vnv}/bin/pip* {vnv}/bin/python*',
        f'python3 -m venv {vnv}',
        f'{pip} install -U --force-reinstall pip',
        f'{pip} install ipykernel',
        f'{pip} uninstall -y ngrok pyngrok'
    ]

    [SyS(f'{cmd}>/dev/null 2>&1') for cmd in req]


print('checking venv...')
ui, url, need_space, vnv, fn = load_config()
pip = str(vnv / 'bin/python3 -m pip')

tempe()
trashing()
unused_venv()

if not venv_exists(vnv, ui):
    install_venv(ui, url, need_space, fn)

aDel()
clear_output(wait=True)
CD(cwd)
