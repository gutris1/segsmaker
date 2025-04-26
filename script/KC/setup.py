from IPython.display import display, Image, HTML, clear_output
from IPython import get_ipython
from ipywidgets import widgets
from pathlib import Path
import subprocess
import argparse
import shlex
import json
import sys
import os
import re

SyS = get_ipython().system
CD = os.chdir
iRON = os.environ

output = widgets.Output()
loading = widgets.Output()

ENVNAME, ENVBASE, ENVHOME = None, None, None
env_list = {
    'Colab': ('/content', '/content', 'COLAB_JUPYTER_TOKEN'),
    'Kaggle': ('/kaggle', '/kaggle/working', 'KAGGLE_DATA_PROXY_TOKEN')
}
for envname, (envbase, envhome, envvar) in env_list.items():
    if envvar in iRON:
        ENVNAME = envname
        ENVBASE = envbase
        ENVHOME = envhome
        break

if not ENVNAME:
    print('You are not in Kaggle or Google Colab.\nExiting.')
    sys.exit()

RST = '\033[0m'
R = '\033[31m'
P = '\033[38;5;135m'
ORANGE = '\033[38;5;208m'
AR = f'{ORANGE}▶{RST}'
ERR = f'{P}[{RST}{R}ERROR{RST}{P}]{RST}'
IMG = 'https://github.com/gutris1/segsmaker/raw/main/script/loading.png'

HOME = Path(ENVHOME)
BASEPATH = Path(ENVBASE)
TMP = BASEPATH / 'temp'

PY = Path('/GUTRIS1')
SRC = HOME / 'gutris1'
MRK = SRC / 'marking.py'
KEY = SRC / 'api-key.json'
MARKED = SRC / 'marking.json'

USR = Path('/usr/bin')
STR = Path.home() / '.ipython/profile_default/startup'
nenen = STR / 'nenen88.py'
KANDANG = STR / 'KANDANG.py'

TMP.mkdir(parents=True, exist_ok=True)
SRC.mkdir(parents=True, exist_ok=True)

WEBUI_LIST = ['A1111', 'Forge', 'ComfyUI', 'ReForge', 'SwarmUI']

def prevent_silly():
    parser = argparse.ArgumentParser(description='WebUI Installer Script for Kaggle and Google Colab')
    parser.add_argument('--webui', required=True, help='available webui: A1111, Forge, ComfyUI, ReForge, SwarmUI')
    parser.add_argument('--civitai_key', required=True, help='your CivitAI API key')
    parser.add_argument('--hf_read_token', default=None, help='your Huggingface READ Token (optional)')
    parser.add_argument('--bgm', default='dQw4w9WgXcQ', help='play youtube video on jupyter cell')

    args, unknown = parser.parse_known_args()

    arg1 = args.webui.lower()
    arg2 = args.civitai_key.strip()
    arg3 = args.hf_read_token.strip() if args.hf_read_token else ''
    arg4 = args.bgm.strip() if args.bgm else ''

    if not any(arg1 == option.lower() for option in WEBUI_LIST):
        print(f'{ERR}: invalid webui option: "{args.webui}"')
        print(f'Available webui options: {", ".join(WEBUI_LIST)}')
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

    rr = 'dQw4w9WgXcQ'
    if not arg4: arg4 = rr
    if re.search(r'\s+', arg4): arg4 = rr

    Muzik = f"""
    <iframe width="640" height="360"
      src="https://www.youtube.com/embed/{arg4}?autoplay=1"
      frameborder="0"
      referrerpolicy="strict-origin-when-cross-origin"
      allowfullscreen>
    </iframe>
    """

    webui_webui = next(option for option in WEBUI_LIST if arg1 == option.lower())
    return webui_webui, arg2, arg3, Muzik

def PythonPortable():
    BIN = str(PY / 'bin')
    PKG = str(PY / 'lib/python3.10/site-packages')

    if webui in ['ComfyUI', 'SwarmUI']:
        url = 'https://huggingface.co/gutris1/webui/resolve/main/env/ComfyUI-python310-torch251-cu121.tar.lz4'
    else:
        url = 'https://huggingface.co/gutris1/webui/resolve/main/env/python310-torch251-cu121.tar.lz4'

    fn = Path(url).name

    CD('/')
    print(f'\n{AR} installing Python Portable 3.10.15')
    SyS('sudo apt-get -qq -y install aria2 pv lz4 >/dev/null 2>&1')
    aria = f'aria2c --console-log-level=error --stderr=true -c -x16 -s16 -k1M -j5 {url} -o {fn}'
    pv = f'pv {fn} | lz4 -d | tar -xf -'

    p = subprocess.Popen(shlex.split(aria), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    p.wait()

    SyS(pv)
    Path(f'/{fn}').unlink()

    sys.path.insert(0, PKG)
    if BIN not in iRON['PATH']: iRON['PATH'] = BIN + ':' + iRON['PATH']
    if PKG not in iRON['PYTHONPATH']: iRON['PYTHONPATH'] = PKG + ':' + iRON['PYTHONPATH']

    if ENVNAME == 'Kaggle':
        for cmd in [
            'pip install ipywidgets jupyterlab_widgets --upgrade',
            'rm -f /usr/lib/python3.10/sitecustomize.py'
        ]: SyS(f'{cmd} >/dev/null 2>&1')

def install_tunnel():
    SyS(f'wget -qO {USR}/cl https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64')
    SyS(f'chmod +x {USR}/cl')

    path = PY / 'lib/python3.10/site-packages/gradio_tunneling/main.py'
    SyS(f'pip install -q gradio-tunneling && wget -qO {path} https://github.com/gutris1/segsmaker/raw/main/script/gradio-tunnel.py')

    bins = {
        'zrok': {
            'bin': USR / 'zrok',
            'url': 'https://github.com/openziti/zrok/releases/download/v1.0.2/zrok_1.0.2_linux_amd64.tar.gz'
        },
        'ngrok': {
            'bin': USR / 'ngrok',
            'url': 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz'
        }
    }

    for n, b in bins.items():
        if b['bin'].exists():
            continue

        url = b['url']
        name = Path(url).name

        SyS(f'wget -qO {name} {url}')
        SyS(f'tar -xzf {name} -C {USR}')
        SyS(f'rm -f {name}')

def saving():
    j = {
        'ENVNAME': ENVNAME,
        'HOMEPATH': HOME,
        'TEMPPATH': TMP,
        'BASEPATH': BASEPATH
    }

    text = '\n'.join(f"{k} = '{v}'" for k, v in j.items())
    Path(KANDANG).write_text(text)

def marking(p, n, u):
    t = p / n
    v = {'ui': u, 'launch_args': '', 'tunnel': ''}

    if not t.exists(): t.write_text(json.dumps(v, indent=4))

    d = json.loads(t.read_text())
    d.update(v)
    t.write_text(json.dumps(d, indent=4))

def key_inject(C, H):
    p = Path(nenen)
    v = p.read_text()
    v = v.replace("TOKET = ''", f"TOKET = '{C}'")
    v = v.replace("TOBRUT = ''", f"TOBRUT = '{H}'")
    p.write_text(v)

def sym_link(U, M):
    configs = {
        'A1111': {
            'sym': [
                f"rm -rf {M / 'Stable-diffusion/tmp_ckpt'} {M / 'Lora/tmp_lora'} {M / 'ControlNet'} {TMP}/*"
            ],
            'links': [
                (TMP / 'ckpt', M / 'Stable-diffusion/tmp_ckpt'),
                (TMP / 'lora', M / 'Lora/tmp_lora'),
                (TMP / 'controlnet', M / 'ControlNet')
            ]
        },

        'ReForge': {
            'sym': [
                f"rm -rf {M / 'Stable-diffusion/tmp_ckpt'} {M / 'Lora/tmp_lora'} {M / 'ControlNet'}",
                f"rm -rf {M / 'svd'} {M / 'z123'} {TMP}/*"
            ],
            'links': [
                (TMP / 'ckpt', M / 'Stable-diffusion/tmp_ckpt'),
                (TMP / 'lora', M / 'Lora/tmp_lora'),
                (TMP / 'controlnet', M / 'ControlNet'),
                (TMP / 'z123', M / 'z123'),
                (TMP / 'svd', M / 'svd')
            ]
        },

        'Forge': {
            'sym': [
                f"rm -rf {M / 'Stable-diffusion/tmp_ckpt'} {M / 'Lora/tmp_lora'} {M / 'ControlNet'}",
                f"rm -rf {M / 'svd'} {M / 'z123'} {M / 'clip'} {M / 'clip_vision'} {M / 'diffusers'}",
                f"rm -rf {M / 'diffusion_models'} {M / 'text_encoder'} {M / 'unet'} {TMP}/*"
            ],
            'links': [
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
            ]
        },

        'ComfyUI': {
            'sym': [
                f"rm -rf {M / 'checkpoints/tmp_ckpt'} {M / 'loras/tmp_lora'} {M / 'controlnet'}",
                f"rm -rf {M / 'clip'} {M / 'clip_vision'} {M / 'diffusers'} {M / 'diffusion_models'}",
                f"rm -rf {M / 'text_encoders'} {M / 'unet'} {TMP}/*"
            ],
            'links': [
                (TMP / 'ckpt', M / 'checkpoints/tmp_ckpt'),
                (TMP / 'lora', M / 'loras/tmp_lora'),
                (TMP / 'controlnet', M / 'controlnet'),
                (TMP / 'clip', M / 'clip'),
                (TMP / 'clip_vision', M / 'clip_vision'),
                (TMP / 'diffusers', M / 'diffusers'),
                (TMP / 'diffusion_models', M / 'diffusion_models'),
                (TMP / 'text_encoders', M / 'text_encoders'),
                (TMP / 'unet', M / 'unet')
            ]
        },

        'SwarmUI': {
            'sym': [
                f"rm -rf {M / 'Stable-Diffusion/tmp_ckpt'} {M / 'Lora/tmp_lora'} {M / 'controlnet'}",
                f"rm -rf {M / 'clip'} {M / 'unet'} {TMP}/*"
            ],
            'links': [
                (TMP / 'ckpt', M / 'Stable-Diffusion/tmp_ckpt'),
                (TMP / 'lora', M / 'Lora/tmp_lora'),
                (TMP / 'controlnet', M / 'controlnet'),
                (TMP / 'clip', M / 'clip'),
                (TMP / 'unet', M / 'unet')
            ]
        }
    }

    cfg = configs.get(U)
    [SyS(f'{cmd}') for cmd in cfg['sym']]
    if U in ['A1111', 'Forge', 'ReForge']: [(M / d).mkdir(parents=True, exist_ok=True) for d in ['Lora', 'ESRGAN']]
    [SyS(f'ln -s {src} {tg}') for src, tg in cfg['links']]

def webui_req(U, W, M):
    CD(W)

    if U in ['A1111', 'Forge', 'ComfyUI', 'ReForge']:
        pull(f'https://github.com/gutris1/segsmaker {U.lower()} {W}')

    elif U == 'SwarmUI':
        M.mkdir(parents=True, exist_ok=True)
        for sub in ['Stable-Diffusion', 'Lora', 'Embeddings', 'VAE', 'upscale_models']:
            (M / sub).mkdir(parents=True, exist_ok=True)

        download(f'https://dot.net/v1/dotnet-install.sh {W}')
        dotnet = W / 'dotnet-install.sh'
        dotnet.chmod(0o755)
        SyS('bash ./dotnet-install.sh --channel 8.0')

    sym_link(U, M)
    install_tunnel()

    scripts = [
        f'https://github.com/gutris1/segsmaker/raw/main/script/controlnet.py {W}/asd',
        f'https://github.com/gutris1/segsmaker/raw/main/script/KC/segsmaker.py {W}'
    ]

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

    line = scripts + upscalers
    for item in line: download(item)

    if U not in ['SwarmUI', 'ComfyUI']:
        SyS(f'rm -f {W}/html/card-no-preview.png')
        download(f'https://huggingface.co/gutris1/webui/resolve/main/misc/card-no-preview.png {W}/html')

def webui_extension(U, W, M):
    EXT = W / 'custom_nodes' if U == 'ComfyUI' else W / 'extensions'
    CD(EXT)

    if U == 'ComfyUI':
        say('<br><b>【{red} Installing Custom Nodes{d} 】{red}</b>')
        clone(str(W / 'asd/custom_nodes.txt'))
        print()

        for faces in [
            f'https://github.com/sczhou/CodeFormer/releases/download/v0.1.0/codeformer.pth {M}/facerestore_models',
            f'https://github.com/TencentARC/GFPGAN/releases/download/v1.3.4/GFPGANv1.4.pth {M}/facerestore_models'
        ]: download(faces)

    else:
        say('<br><b>【{red} Installing Extensions{d} 】{red}</b>')
        clone(str(W / 'asd/extension.txt'))

        clone(
            'https://github.com/gutris1/sd-civitai-browser-plus-plus'
            if ENVNAME == 'Kaggle'
            else 'https://github.com/BlafKing/sd-civitai-browser-plus'
        )

def webui_installation(U, W, M, E, V):
    webui_req(U, W, M)

    extras = [
        f'https://huggingface.co/gutris1/webui/resolve/main/misc/embeddings.zip {W}',
        f'https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.safetensors {V}',
        f'https://huggingface.co/gutris1/webui/resolve/main/misc/embeddingsXL.zip {W}',
        f'https://huggingface.co/madebyollin/sdxl-vae-fp16-fix/resolve/main/sdxl.vae.safetensors {V} sdxl_vae.safetensors'
    ]

    for i in extras: download(i)
    SyS(f'unzip -qo {W / "embeddings.zip"} -d {E} && rm {W / "embeddings.zip"}')
    SyS(f'unzip -qo {W / "embeddingsXL.zip"} -d {E} && rm {W / "embeddingsXL.zip"}')

    if U != 'SwarmUI': webui_extension(U, W, M)

def webui_selection(ui):
    with output:
        output.clear_output(wait=True)
        repo_url = {
            'A1111': 'https://github.com/AUTOMATIC1111/stable-diffusion-webui A1111',
            'Forge': 'https://github.com/lllyasviel/stable-diffusion-webui-forge Forge',
            'ComfyUI': 'https://github.com/comfyanonymous/ComfyUI',
            'ReForge': 'https://github.com/Panchovix/stable-diffusion-webui-reForge ReForge',
            'SwarmUI': 'https://github.com/mcmonkeyprojects/SwarmUI'
        }

        if ui in repo_url: (WEBUI, repo) = (HOME / ui, repo_url[ui])

        MODELS = WEBUI / 'Models' if ui == 'SwarmUI' else WEBUI / 'models'
        EMB = MODELS / 'Embeddings' if ui == 'SwarmUI' else (MODELS / 'embeddings' if ui == 'ComfyUI' else WEBUI / 'embeddings')
        VAE = MODELS / 'vae' if ui == 'ComfyUI' else MODELS / 'VAE'

        say(f'<b>【{{red}} Installing {WEBUI.name}{{d}} 】{{red}}</b>')
        clone(repo)

        webui_installation(ui, WEBUI, MODELS, EMB, VAE)

        with loading:
            loading.clear_output(wait=True)
            say('<br><b>【{red} Done{d} 】{red}</b>')
            tempe()
            CD(HOME)

def webui_installer():
    CD(HOME)
    ui = (json.load(MARKED.open('r')) if MARKED.exists() else {}).get('ui')
    WEBUI = HOME / ui if ui else None

    if WEBUI is not None and WEBUI.exists():
        git_dir = WEBUI / '.git'
        if git_dir.exists():
            CD(WEBUI)
            with output:
                output.clear_output(wait=True)
                if ui in ['A1111', 'ComfyUI', 'SwarmUI']:
                    SyS('git pull origin master')
                elif ui in ['Forge', 'ReForge']:
                    SyS('git pull origin main')
                with loading: loading.clear_output()
    else:
        try:
            webui_selection(webui)
        except KeyboardInterrupt:
            with loading: loading.clear_output()
            with output: print('\nCanceled.')
        except Exception as e:
            with loading: loading.clear_output()
            with output: print(f'\n{ERR}: {e}')

def notebook_scripts():
    z = [
        (STR / '00-startup.py', f'wget -qO {STR}/00-startup.py https://github.com/gutris1/segsmaker/raw/main/script/KC/00-startup.py'),
        (nenen, f'wget -qO {nenen} https://github.com/gutris1/segsmaker/raw/main/script/nenen88.py'),
        (STR / 'cupang.py', f'wget -qO {STR}/cupang.py https://github.com/gutris1/segsmaker/raw/main/script/cupang.py'),
        (MRK, f'wget -qO {MRK} https://github.com/gutris1/segsmaker/raw/main/script/marking.py')
    ]

    [SyS(y) for x, y in z if not Path(x).exists()]

    saving()
    key_inject(civitai_key, hf_read_token)
    marking(SRC, MARKED, webui)
    sys.path.append(str(STR))

    for scripts in [nenen, KANDANG, MRK]: get_ipython().run_line_magic('run', str(scripts))

webui, civitai_key, hf_read_token, bgm = prevent_silly()
if civitai_key is None: sys.exit()

display(output, loading)
with loading: display(HTML(bgm)); display(Image(url=IMG))
with output: PY.exists() or PythonPortable()
notebook_scripts()

from nenen88 import clone, say, download, tempe, pull
webui_installer()
