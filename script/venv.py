from IPython.display import clear_output, Image, display
from IPython import get_ipython
from pathlib import Path
from nenen88 import download, say, tempe
import os, shlex, subprocess

home = Path.home()
img = home / ".conda/loading.png"
cwd = os.getcwd()

url = 'https://huggingface.co/pantat88/back_up/resolve/main/venv.tar.lz4'
fn = Path(url).name
tmp = Path('/tmp')
vnv = tmp / "venv"

print('checking venv...')

def find():
    dirs = ["asd", "forge", "ComfyUI"]

    for names in dirs:
        paths = home / names
        cmd = f"find {paths} -type d -name .ipynb_checkpoints -exec rm -rf {{}} +"
        subprocess.run(shlex.split(cmd), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def check(folder):
    du = get_ipython().getoutput(f'du -s -b {folder}')
    if du:
        size = int(du[0].split()[0])
        return size
    else:
        return 0

def venv():
    if vnv.exists() and check(vnv) > 7 * 1024**3:
        return
    else:
        os.chdir(tmp)
        get_ipython().system(f'rm -rf {vnv}')

        clear_output(wait=True)
        display(Image(filename=str(img)))
        say('【{red} Downloading VENV{d} 】{red}')
        download(url)

        clear_output(wait=True)
        display(Image(filename=str(img)))
        say('【{red} Installing VENV{d} 】{red}')
        get_ipython().system(f'pv {fn} | lz4 -d | tar xf -')
        Path(fn).unlink()

        get_ipython().system(f'rm -rf {vnv / "bin" / "pip*"}')
        get_ipython().system(f'rm -rf {vnv / "bin" / "python*"}')
        os.system(f'python -m venv {vnv}')
        os.system('/tmp/venv/bin/python3 -m pip install -q --upgrade pip')

tempe()
find()
venv()
clear_output(wait=True)
os.chdir(cwd)
