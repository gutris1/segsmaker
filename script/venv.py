from IPython.display import clear_output, Image, display
from IPython import get_ipython
from pathlib import Path
from nenen88 import download, say, tempe
import os

url = 'https://huggingface.co/pantat88/back_up/resolve/main/venv.tar.lz4'
fn = Path(url).name
tmp_ = Path('/tmp')
venv_ = tmp_ / "venv"
home = Path.home()
conda = home / ".conda"
cwd = os.getcwd()

img = conda / "loading.png"
display(Image(filename=str(img)))

def check(folder):
    du = get_ipython().getoutput(f'du -s -b {folder}')
    if du:
        size = int(du[0].split()[0])
        return size
    else:
        return 0

def venv():
    venv_.mkdir(parents=True, exist_ok=True)
    if venv_.exists() and check(venv_) > 7 * 1024**3:
        return
    else:
        say('【{red} Installing VENV{d} 】{red}')
        os.chdir(venv_)
        download(url)
        get_ipython().system(f'pv {fn} | lz4 -d | tar xf -')
        get_ipython().system(f'rm -rf {venv_ / "bin" / "pip*"}')
        get_ipython().system(f'rm -rf {venv_ / "bin" / "python*"}')
        os.system(f'python -m venv {venv_}')
        get_ipython().system(f'rm -rf {fn}')

tempe()
venv()
clear_output()
os.chdir(cwd)
