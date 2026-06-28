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

    scripts = SM_Script(W)
    scripts.extend(CN_Script(W))

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

    l = scripts + upscalers
    for i in l: download(i)

    if U not in ['SwarmUI', 'ComfyUI']:
        e = 'jpg' if U in ['Forge-Classic', 'Forge-Neo'] else 'png'
        SyS(f'rm -f {W}/html/card-no-preview.{e}')

        for ass in [
            f'https://huggingface.co/gutris1/webui/resolve/main/misc/card-no-preview.png {W}/html card-no-preview.{e}',
            f'https://github.com/gutris1/segsmaker/raw/main/config/NoCrypt_miku.json {W}/tmp/gradio_themes',
            f'https://github.com/gutris1/segsmaker/raw/main/config/user.css {W} user.css'
        ]: download(ass)

        if U not in ['Forge', 'Forge-Neo']: download(f'https://github.com/gutris1/segsmaker/raw/main/config/config.json {W} config.json')

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
    multi_panel.layout.display = 'none'

    current_ui = json.load(MARKED.open()).get('ui') if MARKED.exists() else None
    WEBUI = HOME / ui if ui else None

    if WEBUI and WEBUI.exists():
        git_dir = WEBUI / '.git'

        if git_dir.exists():
            CD(WEBUI)

            with output:
                branch = UID.get(ui, {}).get('b')
                if branch: SyS(f'git pull origin {branch}')

                x = SM_Script(WEBUI)
                if ui: x.append(CN_Script(WEBUI))

                print()
                install_tunnel()
                for y in x: download(y)

    else:
        if current_ui and current_ui != ui:
            webui = HOME / current_ui

            with output:
                if webui.exists():
                    print(f'{current_ui} is installed. uninstall it before switching to {ui}.')
                    return

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

def SM_Script(WEBUI):
    return [
        f'https://github.com/gutris1/segsmaker/raw/main/script/SM/venv.py {WEBUI}',
        f'https://github.com/gutris1/segsmaker/raw/main/script/SM/segsmaker.py {WEBUI}'
    ]

def CN_Script(WEBUI):
    return [
        f'https://github.com/gutris1/segsmaker/raw/main/script/controlnet.py {WEBUI}/asd',
        f'https://github.com/gutris1/segsmaker/raw/main/script/cn15.py {WEBUI}/asd',
        f'https://github.com/gutris1/segsmaker/raw/main/script/cnxl.py {WEBUI}/asd'
    ]

def segsmaker_setup():
    JS = """
    (() => {
      setTimeout(() => {
        document.querySelectorAll('.multi-panel, .hbox1, .hbox2').forEach(el => el.classList.add('loaded'));
      }, 1200);
    
      setTimeout(() => {
        document.querySelectorAll('.multi-panel').forEach(el => {
          let p = el.parentElement;
          for (let i = 0; i < 3 && p; i++, p = p.parentElement) {
            p.classList.add('setup-loaded');
          }
        });
      }, 1000);
    })();
    """

    for cmd in [
        f'curl -sLo {CSS} https://github.com/gutris1/segsmaker/raw/main/script/SM/segsmaker.css',
        f'curl -sLo {IMG} https://github.com/gutris1/segsmaker/raw/main/script/loading.png',
        f'curl -sLo {SRC}/bg.jpg https://i.imgur.com/5Mkdrpw.jpeg,'
        f'curl -sLo {MRK} https://github.com/gutris1/segsmaker/raw/main/script/marking.py'
    ]: SyS(cmd)

    load_css()
    display(HTML(f'<script>{JS}</script>'))
    display(multi_panel, output, loading)

UID = {
    'A1111': {
        'r': 'https://github.com/gutris1/A1111',
        'b': 'master',
        'sym': lambda M: [
            f"rm -rf {M / 'Stable-diffusion/tmp_ckpt'} {M / 'Lora/tmp_lora'} {M / 'ControlNet'}"
        ],
        'links': lambda M: [
            (TMP, HOME / 'tmp'),
            (TMP / 'ckpt', M / 'Stable-diffusion/tmp_ckpt'),
            (TMP / 'lora', M / 'Lora/tmp_lora'),
            (TMP / 'controlnet', M / 'ControlNet')
        ],
    },

    'Forge': {
        'r': 'https://github.com/lllyasviel/stable-diffusion-webui-forge Forge',
        'b': 'main',
        'sym': lambda M: [
            f"rm -rf {M / 'Stable-diffusion/tmp_ckpt'} {M / 'Lora/tmp_lora'} {M / 'ControlNet'}",
            f"rm -rf {M / 'svd'} {M / 'z123'} {M / 'clip'} {M / 'clip_vision'} {M / 'diffusers'}",
            f"rm -rf {M / 'diffusion_models'} {M / 'text_encoder'} {M / 'unet'}"
        ],
        'links': lambda M: [
            (TMP, HOME / 'tmp'),
            (TMP / 'ckpt', M / 'Stable-diffusion/tmp_ckpt'),
            (TMP / 'lora', M / 'Lora/tmp_lora'),
            (TMP / 'controlnet', M / 'ControlNet'),
            (TMP / 'z123', M / 'z123'),
            (TMP / 'svd', M / 'svd'),
            (TMP / 'clip', M / 'clip'),
            (TMP / 'clip_vision', M / 'clip_vision'),
            (TMP / 'diffusers', M / 'diffusers'),
            (TMP / 'diffusion_models', M / 'diffusion_models'),
            (TMP / 'text_encoders', M / 'text_encoder'),
            (TMP / 'unet', M / 'unet')
        ],
    },

    'ReForge': {
        'r': 'https://github.com/Panchovix/stable-diffusion-webui-reForge ReForge',
        'b': 'main',
        'sym': lambda M: [
            f"rm -rf {M / 'Stable-diffusion/tmp_ckpt'} {M / 'Lora/tmp_lora'} {M / 'ControlNet'}",
            f"rm -rf {M / 'svd'} {M / 'z123'}"
        ],
        'links': lambda M: [
            (TMP, HOME / 'tmp'),
            (TMP / 'ckpt', M / 'Stable-diffusion/tmp_ckpt'),
            (TMP / 'lora', M / 'Lora/tmp_lora'),
            (TMP / 'controlnet', M / 'ControlNet'),
            (TMP / 'z123', M / 'z123'),
            (TMP / 'svd', M / 'svd')
        ],
    },

    'ReForge-old': {
        'r': '-b main-old https://github.com/Panchovix/stable-diffusion-webui-reForge ReForge-old',
        'b': 'main-old',
    },

    'Forge-Classic': {
        'r': '-b classic https://github.com/Haoming02/sd-webui-forge-classic Forge-Classic',
        'b': 'classic',
        'sym': lambda M: [
            f"rm -rf {M / 'Stable-diffusion/tmp_ckpt'} {M / 'Lora/tmp_lora'} {M / 'ControlNet'}"
        ],
        'links': lambda M: [
            (TMP, HOME / 'tmp'),
            (TMP / 'ckpt', M / 'Stable-diffusion/tmp_ckpt'),
            (TMP / 'lora', M / 'Lora/tmp_lora'),
            (TMP / 'controlnet', M / 'ControlNet')
        ],
    },

    'Forge-Neo': {
        'r': '-b neo https://github.com/Haoming02/sd-webui-forge-classic Forge-Neo',
        'b': 'neo',
    },

    'ComfyUI': {
        'r': 'https://github.com/comfyanonymous/ComfyUI',
        'b': 'master',
        'sym': lambda M: [
            f"rm -rf {M / 'checkpoints/tmp_ckpt'} {M / 'loras/tmp_lora'} {M / 'controlnet'}",
            f"rm -rf {M / 'clip'} {M / 'clip_vision'} {M / 'diffusers'} {M / 'diffusion_models'}",
            f"rm -rf {M / 'text_encoders'} {M / 'unet'}"
        ],
        'links': lambda M: [
            (M / 'checkpoints', M / 'checkpoints_symlink'),
            (TMP, HOME / 'tmp'),
            (TMP / 'ckpt', M / 'checkpoints/tmp_ckpt'),
            (TMP / 'lora', M / 'loras/tmp_lora'),
            (TMP / 'controlnet', M / 'controlnet'),
            (TMP / 'clip', M / 'clip'),
            (TMP / 'clip_vision', M / 'clip_vision'),
            (TMP / 'diffusers', M / 'diffusers'),
            (TMP / 'diffusion_models', M / 'diffusion_models'),
            (TMP / 'text_encoders', M / 'text_encoders'),
            (TMP / 'unet', M / 'unet')
        ],
    },

    'SwarmUI': {
        'r': 'https://github.com/mcmonkeyprojects/SwarmUI',
        'b': 'master',
       'sym': lambda M: [
            f"rm -rf {M / 'Stable-Diffusion/tmp_ckpt'} {M / 'Lora/tmp_lora'} {M / 'controlnet'}",
            f"rm -rf {M / 'clip'} {M / 'unet'}"
        ],
        'links': lambda M: [
            (TMP, HOME / 'tmp'),
            (TMP / 'ckpt', M / 'Stable-Diffusion/tmp_ckpt'),
            (TMP / 'lora', M / 'Lora/tmp_lora'),
            (TMP / 'controlnet', M / 'controlnet'),
            (TMP / 'clip', M / 'clip'),
            (TMP / 'unet', M / 'unet')
        ],
    },
}

output = widgets.Output()
loading = widgets.Output()

row1 = ['A1111', 'Forge', 'ReForge', 'ReForge-old']
buttons1 = [widgets.Button(description='') for btn in row1]
for button, btn in zip(buttons1, row1):
    button.add_class(btn.lower())
    button.add_class('segs-setup-buttons')
    button.on_click(lambda x, btn=btn: webui_setup(btn))

row2 = ['Forge-Neo', 'Forge-Classic', 'ComfyUI', 'SwarmUI']
buttons2 = [widgets.Button(description='') for btn in row2]
for button, btn in zip(buttons2, row2):
    button.add_class(btn.lower())
    button.add_class('segs-setup-buttons')
    button.on_click(lambda x, btn=btn: webui_setup(btn))

hbox1 = widgets.Box(buttons1, layout=widgets.Layout(width='100%', height='255px'))
hbox2 = widgets.Box(buttons2, layout=widgets.Layout(width='100%', height='255px'))
multi_panel = widgets.VBox([hbox1, hbox2])
multi_panel.add_class('multi-panel')
hbox1.add_class('hbox1')
hbox2.add_class('hbox2')

CD(HOME)
segsmaker_setup()
