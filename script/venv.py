from IPython.display import clear_output, Image, display
from IPython import get_ipython
from pathlib import Path
from nenen88 import download, say, tempe
import os

url = 'https://huggingface.co/pantat88/back_up/resolve/main/venv.tar.lz4'
fn = Path(url).name
tmp = Path('/tmp')
vnv = tmp / "venv"
home = Path.home()
img = home / ".conda/loading.png"
cwd = os.getcwd()

print('checking venv...')

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
        clear_output(wait=True)
        display(Image(filename=str(img)))

        say('【{red} Installing VENV{d} 】{red}')
        os.chdir(tmp)
        download(url)

        get_ipython().system(f'pv {fn} | lz4 -d | tar xf -')
        get_ipython().system(f'rm -rf {vnv / "bin" / "pip*"}')
        get_ipython().system(f'rm -rf {vnv / "bin" / "python*"}')
        os.system(f'python -m venv {vnv}')
        get_ipython().system(f'rm -rf {fn}')

tempe()
venv()
clear_output(wait=True)
os.chdir(cwd)
