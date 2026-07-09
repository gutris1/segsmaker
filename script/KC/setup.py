from IPython.display import clear_output
from IPython import get_ipython
from pathlib import Path
import subprocess
import argparse
import shlex
import json
import sys
import os
import re

CD = os.chdir
iRON = os.environ
SyS = get_ipython().system

KAGGLE = 'KAGGLE_DATA_PROXY_TOKEN' in iRON

def _args():
    RESET = '\033[0m'
    RED = '\033[31m'
    PURPLE = '\033[38;5;135m'
    ERR = f'{PURPLE}[{RESET}{RED}ERROR{RESET}{PURPLE}]{RESET}'

    L = ['A1111', 'Forge', 'ReForge', 'ReForge-old', 'Forge-Classic', 'Forge-Neo', 'ComfyUI', 'SwarmUI']

    parser = argparse.ArgumentParser(description='WebUI Installer Script for Kaggle and Google Colab')
    parser.add_argument('--webui', required=True, help='available webui: A1111, Forge, ReForge, ReForge-old, Forge-Classic, Forge-Neo, ComfyUI, SwarmUI')
    parser.add_argument('--civitai_key', required=True, help='your CivitAI API key')
    parser.add_argument('--hf_read_token', default=None, help='your Huggingface READ Token (optional)')

    args, unknown = parser.parse_known_args()

    arg1 = args.webui.lower()
    arg2 = args.civitai_key.strip()
    arg3 = args.hf_read_token.strip() if args.hf_read_token else ''

    if not any(arg1 == option.lower() for option in L):
        print(f'{ERR}: invalid webui option: "{args.webui}"\nAvailable webui options: {", ".join(L)}')
        return None, None, None

    if not arg2:
        print(f'{ERR}: CivitAI API key is missing.')
        return None, None, None
    if re.search(r'\s+', arg2):
        print(f'{ERR}: CivitAI API key contains spaces "{arg2}" - not allowed.')
        return None, None, None
    if len(arg2) < 32:
        print(f'{ERR}: CivitAI API key must be at least 32 characters long.')
        return None, None, None

    if not arg3: arg3 = ''
    if re.search(r'\s+', arg3): arg3 = ''

    ui = next(option for option in L if arg1 == option.lower())
    return ui, arg2, arg3

def _python():
    py = UID[ui]['py']

    say(f"<b>【{{red}} {ui.replace('-', ' ')} — Python {py['v']}{{d}} 】{{red}}</b>")
    CD('/')

    SyS('sudo apt-get -qq -y install aria2 pv lz4 > /dev/null 2>&1')

    for url in (py['url'] if isinstance(py['url'], list) else [py['url']]):
        fn = Path(url).name
        download(url)
        SyS(f'pv "{fn}" | lz4 -d | tar -C /tmp -xf -')
        Path(fn).unlink(missing_ok=True)

    BIN = str(PY / 'bin')
    PKG = str(next((PY / 'lib').glob('python*/site-packages')))

    sys.path.insert(0, PKG)

    if BIN not in iRON.get('PATH', ''): iRON['PATH'] = BIN + ':' + iRON.get('PATH', '')
    if PKG not in iRON.get('PYTHONPATH', ''): iRON['PYTHONPATH'] = PKG + ':' + iRON.get('PYTHONPATH', '')

    if KAGGLE:
        for cmd in (
            'pip install ipywidgets jupyterlab_widgets --upgrade',
            'rm -f /usr/lib/python3.10/sitecustomize.py',
        ): SyS(f'{cmd} > /dev/null 2>&1')

    clear_output(wait=True)

def _marking():
    v = {'ui': ui}

    if not MARK.exists(): MARK.write_text(json.dumps(v, indent=4))

    d = json.loads(MARK.read_text())
    d.update(v)
    MARK.write_text(json.dumps(d, indent=4))

def _inject():
    p = Path(nenen)
    v = p.read_text()
    v = v.replace("TOKET = ''", f"TOKET = '{civitai_key}'")
    v = v.replace("TOBRUT = ''", f"TOBRUT = '{hf_read_token}'")
    p.write_text(v)

def _tunnels():
    SyS(f'wget -qO {USR}/cl https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64')
    SyS(f'chmod +x {USR}/cl')

    bins = {
        'zrok': {
            'bin': USR / 'zrok2',
            'url': 'https://github.com/openziti/zrok/releases/download/v2.0.4/zrok_2.0.4_linux_amd64.tar.gz'
        },
        'ngrok': {
            'bin': USR / 'ngrok',
            'url': 'https://bin.ngrok.com/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz'
        }
    }

    for n, b in bins.items():
        if b['bin'].exists(): b['bin'].unlink()

        url = b['url']
        name = Path(url).name

        SyS(f'wget -qO {name} {url}')
        SyS(f'tar -xzf {name} -C {USR}')
        SyS(f'rm -f {name}')

def _symlinks(M):
    UID['ReForge-old']['sym'] = UID['ReForge']['sym']
    UID['ReForge-old']['links'] = UID['ReForge']['links']

    UID['Forge-Neo']['sym'] = UID['Forge-Classic']['sym']
    UID['Forge-Neo']['links'] = UID['Forge-Classic']['links']

    if ui not in ('ComfyUI', 'SwarmUI'):
        [(M / f).mkdir(parents=True, exist_ok=True) for f in ['Lora', 'ESRGAN']]

    t = HOME / 'tmp'
    SyS(f"rm -rf '{t}' && ln -s /tmp '{t}'")

    d = UID[ui]

    for c in d['sym'](M): SyS(c)
    for p, f in d['links'](M): SyS(f'ln -s {p} {f}')

def _reqs(W, M):
    CD(W)

    if ui != 'SwarmUI': pull(f'https://github.com/gutris1/segsmaker {ui.lower()} {W}')

    else:
        M.mkdir(parents=True, exist_ok=True)

        for f in [
            'Stable-Diffusion',
            'Lora',
            'Embeddings',
            'VAE',
            'upscale_models',
            'text_encoders'
        ]: (M / f).mkdir(parents=True, exist_ok=True)

        for a in ['update', 'install -y dotnet-sdk-8.0']: SyS(f'sudo apt-get -qq {a} > /dev/null 2>&1')

    _symlinks(M)
    _tunnels()

    scripts = [
        f'{G}/script/controlnet.py {W}/asd',
        f'{G}/script/cn15.py {W}/asd',
        f'{G}/script/cnxl.py {W}/asd',
        f'{G}/script/KC/segsmaker.py {W}'
    ]

    u = M / 'upscale_models' if ui in ['ComfyUI', 'SwarmUI'] else M / 'ESRGAN'

    upscalers = [
        f'https://huggingface.co/gutris1/webui/resolve/main/misc/4x-UltraSharp.pth {u}',
        f'https://huggingface.co/gutris1/webui/resolve/main/misc/4x-AnimeSharp.pth {u}',
        f'https://huggingface.co/gutris1/webui/resolve/main/misc/4x_NMKD-Superscale-SP_178000_G.pth {u}',
        f'https://huggingface.co/uwg/upscaler/resolve/main/ESRGAN/8x_NMKD-Superscale_150000_G.pth {u}',
        f'https://huggingface.co/gutris1/webui/resolve/main/misc/4x_RealisticRescaler_100000_G.pth {u}',
        f'https://huggingface.co/gutris1/webui/resolve/main/misc/8x_RealESRGAN.pth {u}',
        f'https://huggingface.co/gutris1/webui/resolve/main/misc/4x_foolhardy_Remacri.pth {u}',
        f'https://huggingface.co/subby2006/NMKD-YandereNeoXL/resolve/main/4x_NMKD-YandereNeoXL_200k.pth {u}',
        f'https://huggingface.co/subby2006/NMKD-UltraYandere/resolve/main/4x_NMKD-UltraYandere_300k.pth {u}'
    ]

    line = scripts + upscalers
    for item in line: download(item)

    if ui not in ['SwarmUI', 'ComfyUI']:
        e = 'jpg' if ui in ['Forge-Classic', 'Forge-Neo'] else 'png'
        SyS(f'rm -f {W}/html/card-no-preview.{e}')

        for i in [
            f'https://huggingface.co/gutris1/webui/resolve/main/misc/card-no-preview.png {W}/html card-no-preview.{e}',
            f'{G}/config/NoCrypt_miku.json {W}/tmp/gradio_themes',
            f'{G}/config/user.css {W} user.css'
        ]: download(i)

        if ui not in ['Forge', 'Forge-Neo']: download(f'{G}/config/config.json {W} config.json')

def _setup():
    WEBUI = HOME / ui

    M = WEBUI / 'Models' if ui == 'SwarmUI' else WEBUI / 'models'
    E = M / 'Embeddings' if ui == 'SwarmUI' else (M / 'embeddings' if ui in ['Forge-Classic', 'Forge-Neo', 'ComfyUI'] else WEBUI / 'embeddings')
    V = M / 'vae' if ui == 'ComfyUI' else M / 'VAE'
    EXT = WEBUI / 'custom_nodes' if ui == 'ComfyUI' else WEBUI / 'extensions'

    CD(HOME)

    if WEBUI.exists() and (WEBUI / '.git').exists():
        CD(WEBUI)
        SyS(f"git pull origin {UID[ui]['branch']}")

    else:
        say(f"<b>【{{red}} {ui.replace('-', ' ')}{{d}} 】{{red}}</b>")
        clone(UID[ui]['repo'])

        _reqs(WEBUI, M)

        for e in [
            f'https://huggingface.co/gutris1/webui/resolve/main/misc/embeddingsXL.zip {WEBUI}',
            f'https://huggingface.co/madebyollin/sdxl-vae-fp16-fix/resolve/main/sdxl.vae.safetensors {V} sdxl_vae.safetensors'
        ]: download(e)

        SyS(f"unzip -qo {WEBUI / 'embeddingsXL.zip'} -d {E} && rm {WEBUI / 'embeddingsXL.zip'}")

        if ui != 'SwarmUI':
            CD(EXT)

            if ui == 'ComfyUI':
                say('<br><b>【{red} ComfyUI — Custom Nodes{d} 】{red}</b>')
                clone(str(WEBUI / 'asd/custom_nodes.txt'))
                print()

                for f in [
                    f'https://github.com/sczhou/CodeFormer/releases/download/v0.1.0/codeformer.pth {M}/facerestore_models',
                    f'https://github.com/TencentARC/GFPGAN/releases/download/v1.3.4/GFPGANv1.4.pth {M}/facerestore_models'
                ]: download(f)

            else:
                say(f"<br><b>【{{red}} {ui.replace('-', ' ')} — Extensions{{d}} 】{{red}}</b>")
                clone(str(WEBUI / 'asd/extension.txt'))

                if KAGGLE: clone('https://github.com/gutris1/sd-image-encryption')

        say('<br><b>【{red} Done{d} 】{red}</b>')
        tempe()
        CD(HOME)

def _scripts():
    for s in [
        f'{startup} {G}/script/KC/00-startup.py',
        f'{cupang} {G}/script/cupang.py',
        f'{uid} {G}/script/_segsmaker_.py',
        f'{nenen} {G}/script/nenen88.py',
        f'{melon} {G}/script/melon00.py',
        f'{MRK} {G}/script/marking.py'
    ]: SyS(f'wget -qO {s}')

    d = {
        'HOME': HOME,
        'SRC': SRC
    }

    t = uid.read_text()

    for k, v in d.items():
        l = f'Path({str(v)!r})' if isinstance(v, Path) else repr(v)
        t = re.sub(rf'^{k}\s*=.*$', f'{k} = {l}', t, flags=re.MULTILINE)

    uid.write_text(t)

    _inject()
    _marking()
    sys.path.append(str(STR))

    for scripts in [nenen, melon, uid, MRK]: get_ipython().run_line_magic('run', str(scripts))

G = 'https://raw.githubusercontent.com/gutris1/segsmaker/main'

USR = Path('/usr/bin')
STR = Path('/root/.ipython/profile_default/startup')
startup = STR / '00-startup.py'
cupang = STR / 'cupang.py'
uid = STR / '_segsmaker_.py'
nenen = STR / 'nenen88.py'
melon = STR / 'melon00.py'

HOME = Path('/kaggle/working' if KAGGLE else '/content')
SRC = HOME / 'gutris1'
MRK = SRC / 'marking.py'
MARK = SRC / 'marking.json'

Path('/tmp').mkdir(parents=True, exist_ok=True)
SRC.mkdir(parents=True, exist_ok=True)

ui, civitai_key, hf_read_token = _args()
_scripts()

from nenen88 import clone, say, download, tempe, pull
from _segsmaker_ import UID

PY = UID[ui]['py']['p']
PY.exists() or _python()

_setup()
