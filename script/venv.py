from IPython.display import clear_output, Image, display
from IPython import get_ipython
from pathlib import Path
import subprocess, os, shlex, json
from nenen88 import tempe, say, download

HOME = Path.home()
SRC = HOME / '.gutris1'
MARK = SRC / 'marking.json'
IMG = SRC / 'loading.png'

tmp = Path('/tmp')
cwd = Path.cwd()

vnv_FF = tmp / "venv-fusion"
vnv_SDT = tmp / "venv-sd-trainer"
vnv_D = tmp / "venv"

def load_config():
    config = json.load(MARK.open('r')) if MARK.exists() else {}
    ui = config.get('ui')

    if ui == 'FaceFusion':
        url = 'https://huggingface.co/pantat88/back_up/resolve/main/venv-fusion.tar.lz4'
        need_space = 12 * 1024**3
        vnv = vnv_FF
    elif ui == 'SDTrainer':
        url = 'https://huggingface.co/pantat88/back_up/resolve/main/venv-sd-trainer.tar.lz4'
        need_space = 14 * 1024**3
        vnv = vnv_SDT
    else:
        url = 'https://huggingface.co/pantat88/back_up/resolve/main/venv_torch231.tar.lz4'
        need_space = 13 * 1024**3
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
            get_ipython().system(rmf)

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
        get_ipython().system(f'rm -rf {file_path}')
        freed_space += size

    return freed_space

def trashing():
    dirs1 = ["A1111", "Forge", "ComfyUI", "ReForge", "FaceFusion", "SDTrainer"]
    dirs2 = ["ckpt", "lora", "controlnet", "svd", "z123"]
    paths = [HOME / name for name in dirs1] + [tmp / name for name in dirs2]
    for path in paths:
        cmd = f"find {path} -type d -name .ipynb_checkpoints -exec rm -rf {{}} +"
        subprocess.run(shlex.split(cmd), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def venv_install(ui, url, need_space, fn):
    while True:
        if vnv.exists():
            size = check_venv(vnv)

            if ui == 'FaceFusion' and size < 7 * 1024**3:
                return
            elif size > 7 * 1024**3:
                return

            get_ipython().system(f'rm -rf {vnv}/* {vnv}')

        clear_output(wait=True)
        display(Image(filename=str(IMG)))

        free_space = check_tmp(tmp)
        req_space = need_space - free_space

        if req_space > 0:
            print(f'Need space {req_space / 1024**3:.1f} GB for venv')
            req_space -= removing(tmp / 'ckpt', req_space)
            if req_space > 0:
                req_space -= removing(tmp / 'lora', req_space)
            if req_space > 0:
                req_space -= removing(tmp / 'controlnet', req_space)

        os.chdir(tmp)
        say('<br>【{red} Installing VENV{d} 】{red}')
        download(url)
        get_ipython().system(f'pv {fn} | lz4 -d | tar xf -')
        Path(fn).unlink()

        get_ipython().system(f'rm -rf {vnv / "bin" / "pip*"}')
        get_ipython().system(f'rm -rf {vnv / "bin" / "python*"}')
        get_ipython().system(f'python3 -m venv {vnv}')
        get_ipython().system(f'{vnv / "bin" / "python3"} -m pip install -q --upgrade --force-reinstall pip')

print('checking venv...')
ui, url, need_space, vnv, fn = load_config()

tempe()
trashing()
unused_venv()
venv_install(ui, url, need_space, fn)

clear_output(wait=True)
os.chdir(cwd)
