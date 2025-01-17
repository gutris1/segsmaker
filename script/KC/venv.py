from IPython import get_ipython
from pathlib import Path
from nenen88 import tempe, say, download
from KANDANG import HOMEPATH, VENVPATH, BASEPATH
import json
import os

HOME = Path(HOMEPATH)
VENV = Path(VENVPATH)

SyS = get_ipython().system
CD = os.chdir

def venv_check(ui):
    fp = Path(BASEPATH) / "vnv.json"
    dt = {"venv": ui}

    if fp.exists():
        with fp.open("r") as f:
            v = json.load(f)

        if v.get("venv") != ui:
            if VENV.exists():
                SyS(f'rm -rf {VENV}/* {VENV}')

            v["venv"] = ui
            dt = v

    with fp.open("w") as f:
        json.dump(dt, f, indent=4)

def she_bang():
    old = b'#!/home/studio-lab-user/tmp/venv/bin/python3\n'
    new = f"#!{VENV}/bin/python3\n"

    for script in (VENV / 'bin').glob('*'):
        if script.is_file():
            try:
                with open(script, 'r+b') as file:
                    lines = file.readlines()
                    if lines and lines[0] == old:
                        lines[0] = new.encode('utf-8')
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

    SyS(f'rm -rf {VENV}/bin/pip* {VENV}/bin/python*')

    req = [
        f'python3 -m venv {VENV}',
        f'{VENV}/bin/python3 -m pip install -U --force-reinstall pip',
        f'{VENV}/bin/python3 -m pip install ipykernel',
        f'{VENV}/bin/python3 -m pip uninstall -y ngrok pyngrok'
    ]

    if ui in ['Forge', 'ComfyUI', 'SwarmUI']:
        req.append(f'{VENV}/bin/python3 -m pip uninstall -y transformers')

    for cmd in req:
        SyS(f'{cmd} &> /dev/null')

tempe()
venv_install()
she_bang()
CD(HOME)
