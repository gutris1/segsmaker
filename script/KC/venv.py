from IPython import get_ipython
from pathlib import Path
from nenen88 import tempe, say, download
from KANDANG import HOMEPATH, TEMPPATH, VENVPATH, BASEPATH, ENVNAME
import subprocess, os, shlex, errno

HOME = Path(HOMEPATH)
tmp = Path(TEMPPATH)
vnv = Path(VENVPATH)

url = 'https://huggingface.co/pantat88/back_up/resolve/main/venv-torch241-cu121.tar.lz4'
fn = Path(url).name

def she_bang():
    vnv_bin = vnv / 'bin'
    old_shebang = b'#!/home/studio-lab-user/tmp/venv/bin/python3\n'
    new_shebang = f"#!{vnv}/bin/python3\n"
    
    for script in vnv_bin.glob('*'):
        if script.is_file():
            try:
                with open(script, 'r+b') as file:
                    lines = file.readlines()
                    if lines and lines[0] == old_shebang:
                        lines[0] = new_shebang.encode('utf-8')
                        file.seek(0)
                        file.writelines(lines)
                        file.truncate()

            except OSError as e:
                if e.errno == 26:
                    pass

def venv_install():
    if vnv.exists():
        get_ipython().system(f'rm -rf {vnv}/* {vnv}')

    os.chdir(BASEPATH)
    say('<br>【{red} Installing VENV{d} 】{red}')
    download(url)

    get_ipython().system(f'pv {fn} | lz4 -d | tar xf -')
    Path(fn).unlink()

    get_ipython().system(f'rm -rf {vnv}/bin/pip* {vnv}/bin/python*')

    n = [
        f'python3 -m venv {vnv}',
        f'{vnv}/bin/python3 -m pip install -U --force-reinstall pip',
        f'{vnv}/bin/python3 -m pip install ipykernel'
    ]

    for p in n:
        subprocess.run(shlex.split(p), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

tempe()
venv_install()
she_bang()
os.chdir(HOME)
