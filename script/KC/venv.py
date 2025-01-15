from IPython import get_ipython
from pathlib import Path
from nenen88 import tempe, say, download
from KANDANG import HOMEPATH, VENVPATH, BASEPATH
import subprocess
import shlex
import errno
import json
import os

HOME = Path(HOMEPATH)
VNV = Path(VENVPATH)

SyS = get_ipython().system
CD = os.chdir

def venv_check(ui):
    fp = Path(BASEPATH) / "vnv.json"
    dt = {"venv": ui}

    if fp.exists():
        with fp.open("r") as f:
            v = json.load(f)

        if v.get("venv") != ui:
            if VNV.exists():
                SyS(f'rm -rf {VNV}/* {VNV}')

            v["venv"] = ui
            dt = v

    with fp.open("w") as f:
        json.dump(dt, f, indent=4)

def she_bang():
    vnv_bin = VNV / 'bin'
    old_shebang = b'#!/home/studio-lab-user/tmp/venv/bin/python3\n'
    new_shebang = f"#!{VNV}/bin/python3\n"

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
    MD = HOME / 'gutris1/marking.json'
    config = json.load(MD.open('r'))
    ui = config.get('ui')

    venv_check(ui)

    url = 'https://huggingface.co/pantat88/back_up/resolve/main/venv-torch241-cu121.tar.lz4'
    fn = Path(url).name

    say('<br>【{red} Installing VENV{d} 】{red}')
    CD(BASEPATH)
    download(url)

    SyS(f'pv {fn} | lz4 -d | tar xf -')
    Path(fn).unlink()

    SyS(f'rm -rf {VNV}/bin/pip* {VNV}/bin/python*')

    n = [
        f'python3 -m venv {VNV}',
        f'{VNV}/bin/python3 -m pip install -U --force-reinstall pip',
        f'{VNV}/bin/python3 -m pip install ipykernel',
        f'{VNV}/bin/python3 -m pip uninstall -y ngrok pyngrok'
    ]

    if ui == 'Forge':
        n.append(f'{VNV}/bin/python3 -m pip uninstall -y transformers')

    for p in n:
        subprocess.run(shlex.split(p), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

tempe()
venv_install()
she_bang()
CD(HOME)
