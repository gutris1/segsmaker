from IPython.display import clear_output, Image, display
from IPython import get_ipython
from pathlib import Path
import subprocess, os, shlex
from nenen88 import tempe, say, download

home = Path.home()
img = home / ".gutris1/loading.png"
tmp = Path('/tmp')
vnv = tmp / "venv"

url = 'https://huggingface.co/pantat88/back_up/resolve/main/venv.tar.lz4'
fn = Path(url).name

need_space = 13 * 1024**3
cwd = os.getcwd()

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
    dirs1 = ["asd", "forge", "ComfyUI"]
    dirs2 = ["ckpt", "lora", "controlnet", "svd", "z123"]
    paths = [home / name for name in dirs1] + [tmp / name for name in dirs2]
    for path in paths:
        cmd = f"find {path} -type d -name .ipynb_checkpoints -exec rm -rf {{}} +"
        subprocess.run(shlex.split(cmd), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def venv_install():
    while True:
        if vnv.exists():
            size = check_venv(vnv)
            if size > 7 * 1024**3:
                return
            get_ipython().system(f'rm -rf {vnv}')

        clear_output(wait=True)
        display(Image(filename=str(img)))

        free_space = check_tmp(tmp)
        req_space = need_space - free_space

        if req_space > 0:
            print(f'Need space {req_space / 1024**3:.1f} GB for venv')
            ckpt_tmp, lora_tmp, cn_tmp = tmp / 'ckpt', tmp / 'lora', tmp / 'controlnet'

            req_space -= removing(ckpt_tmp, req_space)
            if req_space > 0:
                req_space -= removing(lora_tmp, req_space)
            if req_space > 0:
                req_space -= removing(cn_tmp, req_space)

        os.chdir(tmp)
        say('<br>【{red} Downloading VENV{d} 】{red}')
        download(url)

        say('<br>【{red} Installing VENV{d} 】{red}')
        get_ipython().system(f'pv {fn} | lz4 -d | tar xf -')
        Path(fn).unlink()

        get_ipython().system(f'rm -rf {vnv / "bin" / "pip*"}')
        get_ipython().system(f'rm -rf {vnv / "bin" / "python*"}')
        get_ipython().system(f'python -m venv {vnv}')
        get_ipython().system('/tmp/venv/bin/python3 -m pip install -q --upgrade pip')

print('checking venv...')
tempe()
trashing()
venv_install()
clear_output(wait=True)
os.chdir(cwd)
