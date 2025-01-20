from IPython import get_ipython
from pathlib import Path
from nenen88 import tempe, say, download
from KANDANG import HOMEPATH, VENVPATH, BASEPATH, ENVNAME
import json
import os

HOME = Path(HOMEPATH)
VENV = Path(VENVPATH)

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
    o = b'#!/content/venv/bin/python3\n'
    n = b'#!/kaggle/venv/bin/python3\n'

    for s in (VENV / 'bin').glob('*'):
        if s.is_file():
            try:
                with open(s, 'r+b') as f:
                    l = f.readlines()
                    if l and l[0] == o:
                        l[0] = n
                        f.seek(0)
                        f.writelines(l)
                        f.truncate()

            except OSError as e:
                if e.errno == 26:
                    pass

def venv_install():
    MD = HOME / 'gutris1/marking.json'
    config = json.load(MD.open('r'))
    ui = config.get('ui')

    venv_check(ui)

    url = 'https://huggingface.co/pantat88/back_up/resolve/main/venv-torch251-cu121.tar.lz4'
    fn = Path(url).name

    say('<br>【{red} Installing VENV{d} 】{red}')
    CD(BASEPATH)
    download(url)

    SyS(f'pv {fn} | lz4 -d | tar xf -')
    Path(fn).unlink()

    req = []

    if ENVNAME == 'Kaggle':
        req.extend([
            f'rm -f {VENV}/bin/pip* {VENV}/bin/python*',
            f'python3 -m venv {VENV}'
        ])

    req+=[f'{pip} install -U --force-reinstall pip']

    if ui == 'Forge':
        req+=[f'{pip} uninstall -y transformers']

    [SyS(f'{cmd}>/dev/null 2>&1') for cmd in req]


pip = str(VENV / 'bin/python3 -m pip')
SyS = get_ipython().system
CD = os.chdir

tempe()
venv_install()
if ENVNAME == 'Kaggle': she_bang()
CD(HOME)
