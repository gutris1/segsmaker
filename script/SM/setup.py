from IPython.display import display, HTML, clear_output, Image
from IPython import get_ipython
from ipywidgets import widgets
from pathlib import Path
import subprocess
import shutil
import shlex
import json
import sys
import os
import re

CD = os.chdir
iRON = os.environ
SyS = get_ipython().system

def _check():
    R = '\033[31m'
    P = '\033[38;5;135m'
    RST = '\033[0m'
    ERR = f'{P}[{RST}{R}ERROR{RST}{P}]{RST}'

    v = subprocess.run(['python', '--version'], capture_output=True, text=True).stdout.split()[1]
    if tuple(map(int, v.split('.'))) < (3, 10, 6):
        print(f'{ERR}: Python version 3.10.6 or higher required, and you are using Python {v}')
        sys.exit()

def _cleaning():
    v = UID[ui]['py']['p']

    for i in TMP.iterdir():
        if i.is_dir() and i != v:
            shutil.rmtree(i)
        elif i.is_file():
            i.unlink()

def _marking():
    j = SRC / MARK

    if not j.exists():
        j.write_text(json.dumps({
            'ui': ui,
            'launch_args': '',
            'zrok_token': '',
            'ngrok_token': '',
            'tunnel': ''
        }, indent=4))

    d = json.loads(j.read_text())
    d.update({
      'ui': ui,
      'launch_args': ''
    })

    j.write_text(json.dumps(d, indent=4))

def _tunnels():
    tunnel = {
        'zrok2': {
            'bin': HOME / '.zrok2/zrok2',
            'version': HOME / '.zrok2/v2.0.4',
            'url': 'https://github.com/openziti/zrok/releases/download/v2.0.4/zrok_2.0.4_linux_amd64.tar.gz'
        },
        'ngrok': {
            'bin': HOME / '.ngrok/ngrok',
            'url': 'https://bin.ngrok.com/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz'
        }
    }

    for b in tunnel.values():
        binPath = b['bin']
        p = binPath.parent

        if b.get('version', binPath).exists(): continue

        p.mkdir(parents=True, exist_ok=True)
        if binPath.exists(): binPath.unlink()

        n = Path(b['url']).name

        for cmd in [
            f'curl -sLo {p}/{n} {b["url"]}',
            f'tar -xzf {p}/{n} -C {p}',
            f'rm -f {p}/{n}'
        ]: SyS(cmd)

        if 'version' in b:
            [f.unlink(missing_ok=True) for f in p.glob('v*')]
            b['version'].touch()

        if str(p) not in iRON.get('PATH', ''): iRON['PATH'] += ':' + str(p)
        if binPath.exists(): binPath.chmod(0o755)

def _symlinks(M):
    UID['ReForge-old']['sym'] = UID['ReForge']['sym']
    UID['ReForge-old']['links'] = UID['ReForge']['links']

    UID['Forge-Neo']['sym'] = UID['Forge-Classic']['sym']
    UID['Forge-Neo']['links'] = UID['Forge-Classic']['links']

    if ui not in ('ComfyUI', 'SwarmUI'):
        [(M / f).mkdir(parents=True, exist_ok=True) for f in ['Lora', 'ESRGAN']]

    d = UID[ui]

    for c in d['sym'](M): SyS(c)
    for p, t in d['links'](M): SyS(f'ln -s {p} {t}')

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

        download(f'https://dot.net/v1/dotnet-install.sh {W}')
        dotnet = W / 'dotnet-install.sh'
        dotnet.chmod(0o755)
        SyS('bash ./dotnet-install.sh --channel 8.0')
        print()

    _symlinks(M)

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

    for i in _scripts(W) + upscalers: download(i)

    if ui not in ['SwarmUI', 'ComfyUI']:
        e = 'jpg' if ui in ['Forge-Classic', 'Forge-Neo'] else 'png'
        SyS(f'rm -f {W}/html/card-no-preview.{e}')

        for b in [
            f'https://huggingface.co/gutris1/webui/resolve/main/misc/card-no-preview.png {W}/html card-no-preview.{e}',
            f'{G}/config/NoCrypt_miku.json {W}/tmp/gradio_themes',
            f'{G}/config/user.css {W} user.css'
        ]: download(b)

        if ui not in ['Forge', 'Forge-Neo']: download(f'{G}/config/config.json {W} config.json')

def _setup():
    setup_panel.layout.display = 'none'

    current_ui = json.load(MARK.open()).get('ui') if MARK.exists() else None
    WEBUI = HOME / ui

    M = WEBUI / 'Models' if ui == 'SwarmUI' else WEBUI / 'models'
    E = M / 'Embeddings' if ui == 'SwarmUI' else (M / 'embeddings' if ui in ['Forge-Classic', 'Forge-Neo', 'ComfyUI'] else WEBUI / 'embeddings')
    V = M / 'vae' if ui == 'ComfyUI' else M / 'VAE'
    EXT = WEBUI / 'custom_nodes' if ui == 'ComfyUI' else WEBUI / 'extensions'

    CD(HOME)

    if WEBUI.exists() and (WEBUI / '.git').exists():
        with output:
            CD(WEBUI)
            SyS(f"git pull origin {UID[ui]['branch']}")
            print()

            _tunnels()
            for l in _scripts(WEBUI): download(l)

    else:
        if current_ui and current_ui != ui and (HOME / current_ui).exists():
            with output: print(f'{current_ui} is installed. uninstall it before switching to {ui}.')
            return

        for s in [
            f'{SRC}/bg.jpg https://i.imgur.com/5Mkdrpw.jpeg',
            f'{IMG} {G}/script/loading.png',
            f'{MRK} {G}/script/marking.py'
        ]: SyS(f'curl -sLo {s}')

        with loading:
            display(Image(filename=str(IMG)))

        with output:
            say(f"<b>【{{red}} {ui.replace('-', ' ')}{{d}} 】{{red}}</b>")
            clone(UID[ui]['repo'])

            _marking()
            _cleaning()
            _reqs(WEBUI, M)
            _tunnels()

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

            with loading:
                loading.clear_output(wait=True)
                tempe()

                get_ipython().run_line_magic('run', str(MRK))
                get_ipython().run_line_magic('run', str(WEBUI / 'venv.py'))

                loading.clear_output(wait=True)
                say('<br><b>【{red} Done{d} 】{red}</b>')
                CD(HOME)

def _scripts(W):
    return [
        f'{G}/script/SM/venv.py {W}',
        f'{G}/script/SM/segsmaker.py {W}',

        f'{G}/script/controlnet.py {W}/asd',
        f'{G}/script/cn15.py {W}/asd',
        f'{G}/script/cnxl.py {W}/asd'
    ]

def _misc():
    SyS(f'curl -sLo {uid} {G}/script/_segsmaker_.py')
    uid.write_text(re.sub(r'^SRC\s*=.*$', f'SRC = Path({str(SRC)!r})', uid.read_text(), flags=re.MULTILINE))

def _widget():
    JS = """
    (() => {
      setTimeout(() => {
        document.querySelectorAll('.setup-panel, .setup-box1, .setup-box2').forEach(el => el.classList.add('loaded'));
      }, 1200);
    })();
    """

    SyS(f'curl -sLo {CSS} {G}/script/SM/segsmaker.css')

    display(
        HTML(f'<style>{CSS.read_text()}</style><script>{JS}</script>'),
        setup_panel, output, loading
    )

def _buttons(i, c):
    btn = [widgets.Button(description='') for _ in i]

    def onclick(n):
        global ui
        ui = n
        _setup()

    for b, n in zip(btn, i):
        b.add_class(n.lower())
        b.add_class('setup-buttons')
        b.on_click(lambda _, n=n: onclick(n))

    box = widgets.Box(btn)
    box.add_class(c)
    return box

_check()

setup_panel = widgets.VBox([
    _buttons(['A1111', 'Forge', 'ReForge', 'ReForge-old'], 'setup-box1'),
    _buttons(['Forge-Neo', 'Forge-Classic', 'ComfyUI', 'SwarmUI'], 'setup-box2')
])

output = widgets.Output()
loading = widgets.Output()

for w, c in [
    (setup_panel, 'setup-panel'),
    (output, 'ssl-widget-output'),
    (loading, 'ssl-widget-output')
]: w.add_class(c)

G = 'https://raw.githubusercontent.com/gutris1/segsmaker/main'

HOME = Path.home()
TMP = Path('/tmp')

SRC = HOME / '.gutris1'
CSS = SRC / 'segsmaker.css'
IMG = SRC / 'loading.png'
MRK = SRC / 'marking.py'
MARK = SRC / 'marking.json'
uid = HOME / '.ipython/profile_default/startup/_segsmaker_.py'

SRC.mkdir(parents=True, exist_ok=True)

ui = None

if not uid.exists(): _misc()

from nenen88 import pull, say, download, clone, tempe
from _segsmaker_ import UID

_widget()
