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

R = '\033[31m'
P = '\033[38;5;135m'
RST = '\033[0m'
ERR = f'{P}[{RST}{R}ERROR{RST}{P}]{RST}'

python_version = subprocess.run(['python', '--version'], capture_output=True, text=True).stdout.split()[1]
if tuple(map(int, python_version.split('.'))) < (3, 10, 6):
    print(f'{ERR}: Python version 3.10.6 or higher required, and you are using Python {python_version}')
    sys.exit()

from nenen88 import pull, say, download, clone, tempe

SyS = get_ipython().system
iRON = os.environ
CD = os.chdir

HOME = Path.home()
SRC = HOME / '.gutris1'
CSS = SRC / 'segsmaker.css'
IMG = SRC / 'loading.png'
MRK = SRC / 'marking.py'
MARKED = SRC / 'marking.json'
TMP = Path('/tmp')

uid = HOME / '.ipython/profile_default/startup/ssl_uid.py'

SRC.mkdir(parents=True, exist_ok=True)

def load_css():
    display(HTML(f'<style>{CSS.read_text()}</style>'))

def tmp_cleaning(v):
    for i in TMP.iterdir():
        if i.is_dir() and i != v:
            shutil.rmtree(i)
        elif i.is_file() and i != v:
            i.unlink()

def marking(p, n, i):
    j = p / n

    if not j.exists():
        j.write_text(json.dumps({
            'ui': i,
            'launch_args': '',
            'zrok_token': '',
            'ngrok_token': '',
            'tunnel': ''
        }, indent=4))

    d = json.loads(j.read_text())
    d.update({
      'ui': i,
      'launch_args': ''
    })

    j.write_text(json.dumps(d, indent=4))

def install_tunnel():
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

def sym_link(U, M):
    UID['ReForge-old']['sym'] = UID['ReForge']['sym']
    UID['ReForge-old']['links'] = UID['ReForge']['links']

    UID['Forge-Neo']['sym'] = UID['Forge-Classic']['sym']
    UID['Forge-Neo']['links'] = UID['Forge-Classic']['links']

    cfg = UID[U]

    SyS(f"rm -rf {HOME / 'tmp'} {HOME / '.cache'}/*")
    for cmd in cfg['sym'](M): SyS(cmd)

    if U not in ('ComfyUI', 'SwarmUI'):
        for d in ('Lora', 'ESRGAN'): (M / d).mkdir(parents=True, exist_ok=True)

    for src, tg in cfg['links'](M): SyS(f'ln -s {src} {tg}')

def webui_req(U, W, M):
    vnv = TMP / 'venv'
    tmp_cleaning(vnv)
    CD(W)

    if U != 'SwarmUI': pull(f'https://github.com/gutris1/segsmaker {U.lower()} {W}')
    else:
        M.mkdir(parents=True, exist_ok=True)
        for sub in ['Stable-Diffusion', 'Lora', 'Embeddings', 'VAE', 'upscale_models']:
            (M / sub).mkdir(parents=True, exist_ok=True)

        download(f'https://dot.net/v1/dotnet-install.sh {W}')
        dotnet = W / 'dotnet-install.sh'
        dotnet.chmod(0o755)
        SyS('bash ./dotnet-install.sh --channel 8.0')

    sym_link(U, M)

    u = M / 'upscale_models' if U in ['ComfyUI', 'SwarmUI'] else M / 'ESRGAN'
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

    for i in sm_script(W) + upscalers: download(i)

    if U not in ['SwarmUI', 'ComfyUI']:
        e = 'jpg' if U in ['Forge-Classic', 'Forge-Neo'] else 'png'
        SyS(f'rm -f {W}/html/card-no-preview.{e}')

        for m in [
            f'https://huggingface.co/gutris1/webui/resolve/main/misc/card-no-preview.png {W}/html card-no-preview.{e}',
            f'{G}/config/NoCrypt_miku.json {W}/tmp/gradio_themes',
            f'{G}/config/user.css {W} user.css'
        ]: download(m)

        if U not in ['Forge', 'Forge-Neo']: download(f'{G}/config/config.json {W} config.json')

def installing_webui(U, W):
    M = W / 'Models' if U == 'SwarmUI' else W / 'models'
    E = M / 'Embeddings' if U == 'SwarmUI' else (M / 'embeddings' if U in ['Forge-Classic', 'Forge-Neo', 'ComfyUI'] else W / 'embeddings')
    V = M / 'vae' if U == 'ComfyUI' else M / 'VAE'

    EXT = W / 'custom_nodes' if U == 'ComfyUI' else W / 'extensions'

    webui_req(U, W, M)
    install_tunnel()

    extras = [
        f'https://huggingface.co/gutris1/webui/resolve/main/misc/embeddingsXL.zip {W}',
        f'https://huggingface.co/madebyollin/sdxl-vae-fp16-fix/resolve/main/sdxl.vae.safetensors {V} sdxl_vae.safetensors'
    ]

    for i in extras: download(i)
    SyS(f"unzip -qo {W / 'embeddingsXL.zip'} -d {E} && rm {W / 'embeddingsXL.zip'}")

    if U != 'SwarmUI':
        CD(EXT)

        if U == 'ComfyUI':
            say('<br><b>【{red} Installing Custom Nodes{d} 】{red}</b>')
            clone(str(W / 'asd/custom_nodes.txt'))
            print()

            for f in [
                f'https://github.com/sczhou/CodeFormer/releases/download/v0.1.0/codeformer.pth {M}/facerestore_models',
                f'https://github.com/TencentARC/GFPGAN/releases/download/v1.3.4/GFPGANv1.4.pth {M}/facerestore_models'
            ]: download(f)

        else:
            say('<br><b>【{red} Installing Extensions{d} 】{red}</b>')
            clone(str(W / 'asd/extension.txt'))

def webui_setup(ui):
    setup_panel.layout.display = 'none'

    current_ui = json.load(MARKED.open()).get('ui') if MARKED.exists() else None
    WEBUI = HOME / ui if ui else None

    if WEBUI and WEBUI.exists():
        if (WEBUI / '.git').exists():
            CD(WEBUI)

            with output:
                branch = UID.get(ui, {}).get('b')
                if branch: SyS(f'git pull origin {branch}')

                install_tunnel()
                print()
                for l in sm_script(WEBUI): download(l)

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
            WEBUI = HOME / ui
            repo = UID[ui]['r']

            say(f"<b>【{{red}} Installing {ui.replace('-', ' ')}{{d}} 】{{red}}</b>")
            clone(repo)

            marking(SRC, MARKED, ui)
            installing_webui(ui, WEBUI)
            tempe()

            with loading:
                loading.clear_output(wait=True)
                get_ipython().run_line_magic('run', str(MRK))
                get_ipython().run_line_magic('run', str(WEBUI / 'venv.py'))

                loading.clear_output(wait=True)
                say('<b>【{red} Done{d} 】{red}</b>')
                CD(HOME)

def sm_script(W):
    return [
        f'{G}/script/SM/venv.py {W}',
        f'{G}/script/SM/segsmaker.py {W}',

        f'{G}/script/controlnet.py {W}/asd',
        f'{G}/script/cn15.py {W}/asd',
        f'{G}/script/cnxl.py {W}/asd'
    ]

def segsmaker_setup():
    JS = """
    (() => {
      setTimeout(() => {
        document.querySelectorAll('.setup-panel, .setup-box1, .setup-box2').forEach(el => el.classList.add('loaded'));
      }, 1200);

      setTimeout(() => {
        document.querySelectorAll('.setup-panel').forEach(el => {
          let p = el.parentElement;
          for (let i = 0; i < 3 && p; i++, p = p.parentElement) {
            p.classList.add('setup-loaded');
          }
        });
      }, 1000);
    })();
    """

    SyS(f'curl -sLo {CSS} {G}/script/SM/segsmaker.css')

    load_css()
    display(HTML(f'<script>{JS}</script>'))
    display(setup_panel, output, loading)

G = 'https://raw.githubusercontent.com/gutris1/segsmaker/main'

output = widgets.Output()
loading = widgets.Output()

def setup_buttons(i, c):
    btn = [widgets.Button(description='') for _ in i]

    for b, n in zip(btn, i):
        b.add_class(n.lower())
        b.add_class('segs-setup-buttons')
        b.on_click(lambda _, n=n: webui_setup(n))

    box = widgets.Box(btn)
    box.add_class(c)
    return box

setup_panel = widgets.VBox([
    setup_buttons(['A1111', 'Forge', 'ReForge', 'ReForge-old'], 'setup-box1'),
    setup_buttons(['Forge-Neo', 'Forge-Classic', 'ComfyUI', 'SwarmUI'], 'setup-box2')
])

setup_panel.add_class('setup-panel')

if not uid.exists(): SyS(f'curl -sLo {uid} {G}/script/SM/ssl_uid.py')
from ssl_uid import UID

CD(HOME)
segsmaker_setup()
