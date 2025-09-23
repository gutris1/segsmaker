R = '\033[31m'
P = '\033[38;5;135m'
RST = '\033[0m'
ERR = f'{P}[{RST}{R}ERROR{RST}{P}]{RST}'

import sys, subprocess
python_version = subprocess.run(['python', '--version'], capture_output=True, text=True).stdout.split()[1]
if tuple(map(int, python_version.split('.'))) < (3, 10, 6):
    print(f'{ERR}: Python version 3.10.6 or higher required, and you are using Python {python_version}')
    sys.exit()

from IPython.display import display, HTML, clear_output, Image
from IPython import get_ipython
from ipywidgets import widgets
from pathlib import Path
import shutil
import shlex
import json
import os

from nenen88 import pull, say, download, clone, tempe

REPO = {
    'A1111': 'https://github.com/AUTOMATIC1111/stable-diffusion-webui A1111',
    'Forge': 'https://github.com/lllyasviel/stable-diffusion-webui-forge Forge',
    'ReForge': '-b main-old https://github.com/Panchovix/stable-diffusion-webui-reForge ReForge',
    'Forge-Classic': 'https://github.com/Haoming02/sd-webui-forge-classic Forge-Classic',
    'ComfyUI': 'https://github.com/comfyanonymous/ComfyUI',
    'SwarmUI': 'https://github.com/mcmonkeyprojects/SwarmUI'
}

SyS = get_ipython().system
CD = os.chdir

HOME = Path.home()
SRC = HOME / '.gutris1'
CSS = SRC / 'setup.css'
IMG = SRC / 'loading.png'
MRK = SRC / 'marking.py'
MARKED = SRC / 'marking.json'
TMP = Path('/tmp')

SRC.mkdir(parents=True, exist_ok=True)
iRON = os.environ

def SM_Script(WEBUI):
    return [
        f'https://github.com/gutris1/segsmaker/raw/main/script/SM/venv.py {WEBUI}',
        f'https://github.com/gutris1/segsmaker/raw/main/script/SM/Launcher.py {WEBUI}',
        f'https://github.com/gutris1/segsmaker/raw/main/script/SM/segsmaker.py {WEBUI}'
    ]

def CN_Script(WEBUI):
    return f'https://github.com/gutris1/segsmaker/raw/main/script/controlnet.py {WEBUI}/asd'

def Load_CSS():
    display(HTML(f'<style>{CSS.read_text()}</style>'))

def tmp_cleaning(v):
    for i in TMP.iterdir():
        if i.is_dir() and i != v:
            shutil.rmtree(i)
        elif i.is_file() and i != v:
            i.unlink()

def check_ffmpeg():
    i = get_ipython().getoutput('conda list ffmpeg')
    if not any('ffmpeg' in l for l in i):
        c = [
            ('mamba install -y ffmpeg curl', '\ninstalling ffmpeg...'),
            ('mamba install -y cuda-runtime=12.4.1', 'installing cuda-runtime=12.4.1...'),
            ('mamba install -y cudnn=9.2.1.18', 'installing cudnn=9.2.1.18...'),
            ('conda clean -y --all', None)
        ]

        for d, m in c:
            if m is not None:
                print(m)
            subprocess.run(shlex.split(d), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def marking(p, n, i):
    t = p / n
    if not t.exists():
        t.write_text(json.dumps({
            'ui': i,
            'launch_args': '',
            'zrok_token': '',
            'ngrok_token': '',
            'tunnel': ''
        }, indent=4))
    d = json.loads(t.read_text())
    d.update({'ui': i, 'launch_args': ''})
    t.write_text(json.dumps(d, indent=4))

def install_tunnel():
    bins = {
        'zrok': {
            'bin': HOME / '.zrok/bin/zrok',
            'url': 'https://github.com/openziti/zrok/releases/download/v1.0.6/zrok_1.0.6_linux_amd64.tar.gz'
        },
        'ngrok': {
            'bin': HOME / '.ngrok/bin/ngrok',
            'url': 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz'
        }
    }

    for n, b in bins.items():
        binPath = b['bin']
        if binPath.exists(): binPath.unlink()

        url = b['url']
        name = Path(url).name
        binDir = binPath.parent

        binDir.mkdir(parents=True, exist_ok=True)

        SyS(f'curl -sLo {binDir}/{name} {url}')
        SyS(f'tar -xzf {binDir}/{name} -C {binDir} --wildcards *{n}')
        SyS(f'rm -f {binDir}/{name}')

        if str(binDir) not in iRON.get('PATH', ''): iRON['PATH'] += ':' + str(binDir)
        binPath.chmod(0o755)

def sym_link(U, M):
    configs = {
        'A1111': {
            'sym': [
                f"rm -rf {M / 'Stable-diffusion/tmp_ckpt'} {M / 'Lora/tmp_lora'} {M / 'ControlNet'}"
            ],
            'links': [
                (TMP, HOME / 'tmp'),
                (TMP / 'ckpt', M / 'Stable-diffusion/tmp_ckpt'),
                (TMP / 'lora', M / 'Lora/tmp_lora'),
                (TMP / 'controlnet', M / 'ControlNet')
            ]
        },

        'Forge': {
            'sym': [
                f"rm -rf {M / 'Stable-diffusion/tmp_ckpt'} {M / 'Lora/tmp_lora'} {M / 'ControlNet'}",
                f"rm -rf {M / 'svd'} {M / 'z123'} {M / 'clip'} {M / 'clip_vision'} {M / 'diffusers'}",
                f"rm -rf {M / 'diffusion_models'} {M / 'text_encoder'} {M / 'unet'}"
            ],
            'links': [
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
            ]
        },

        'ReForge': {
            'sym': [
                f"rm -rf {M / 'Stable-diffusion/tmp_ckpt'} {M / 'Lora/tmp_lora'} {M / 'ControlNet'}",
                f"rm -rf {M / 'svd'} {M / 'z123'}"
            ],
            'links': [
                (TMP, HOME / 'tmp'),
                (TMP / 'ckpt', M / 'Stable-diffusion/tmp_ckpt'),
                (TMP / 'lora', M / 'Lora/tmp_lora'),
                (TMP / 'controlnet', M / 'ControlNet'),
                (TMP / 'z123', M / 'z123'),
                (TMP / 'svd', M / 'svd')
            ]
        },

        'Forge-Classic': {
            'sym': [
                f"rm -rf {M / 'Stable-diffusion/tmp_ckpt'} {M / 'Lora/tmp_lora'} {M / 'ControlNet'}"
            ],
            'links': [
                (TMP, HOME / 'tmp'),
                (TMP / 'ckpt', M / 'Stable-diffusion/tmp_ckpt'),
                (TMP / 'lora', M / 'Lora/tmp_lora'),
                (TMP / 'controlnet', M / 'ControlNet')
            ]
        },

        'ComfyUI': {
            'sym': [
                f"rm -rf {M / 'checkpoints/tmp_ckpt'} {M / 'loras/tmp_lora'} {M / 'controlnet'}",
                f"rm -rf {M / 'clip'} {M / 'clip_vision'} {M / 'diffusers'} {M / 'diffusion_models'}",
                f"rm -rf {M / 'text_encoders'} {M / 'unet'}"
            ],
            'links': [
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
            ]
        },

        'SwarmUI': {
            'sym': [
                f"rm -rf {M / 'Stable-Diffusion/tmp_ckpt'} {M / 'Lora/tmp_lora'} {M / 'controlnet'}",
                f"rm -rf {M / 'clip'} {M / 'unet'}"
            ],
            'links': [
                (TMP, HOME / 'tmp'),
                (TMP / 'ckpt', M / 'Stable-Diffusion/tmp_ckpt'),
                (TMP / 'lora', M / 'Lora/tmp_lora'),
                (TMP / 'controlnet', M / 'controlnet'),
                (TMP / 'clip', M / 'clip'),
                (TMP / 'unet', M / 'unet')
            ]
        }
    }

    cfg = configs.get(U)
    SyS(f"rm -rf {HOME / 'tmp'} {HOME / '.cache'}/*")
    [SyS(f'{cmd}') for cmd in cfg['sym']]
    if U not in ['ComfyUI', 'SwarmUI']: [(M / d).mkdir(parents=True, exist_ok=True) for d in ['Lora', 'ESRGAN']]
    [SyS(f'ln -s {src} {tg}') for src, tg in cfg['links']]

def webui_req(U, W, M):
    vnv = TMP / 'venv'
    tmp_cleaning(vnv)
    CD(W)

    if U != 'SwarmUI':
        pull(f'https://github.com/gutris1/segsmaker {U.lower()} {W}')
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
    scripts.append(CN_Script(W))

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
        e = 'jpg' if U == 'Forge-Classic' else 'png'
        SyS(f'rm -f {W}/html/card-no-preview.{e}')

        for ass in [
            f'https://huggingface.co/gutris1/webui/resolve/main/misc/card-no-preview.png {W}/html card-no-preview.{e}',
            f'https://github.com/gutris1/segsmaker/raw/main/config/NoCrypt_miku.json {W}/tmp/gradio_themes',
            f'https://github.com/gutris1/segsmaker/raw/main/config/user.css {W} user.css'
        ]: download(ass)

        if U != 'Forge': download(f'https://github.com/gutris1/segsmaker/raw/main/config/config.json {W} config.json')

def WebUIExtensions(U, W, M):
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

def installing_webui(U, W):
    M = W / 'Models' if U == 'SwarmUI' else W / 'models'
    E = M / 'Embeddings' if U == 'SwarmUI' else (M / 'embeddings' if U in ['Forge-Classic', 'ComfyUI'] else W / 'embeddings')
    V = M / 'vae' if U == 'ComfyUI' else M / 'VAE'

    webui_req(U, W, M)
    install_tunnel()

    extras = [
        f'https://huggingface.co/gutris1/webui/resolve/main/misc/embeddingsXL.zip {W}',
        f'https://huggingface.co/madebyollin/sdxl-vae-fp16-fix/resolve/main/sdxl.vae.safetensors {V} sdxl_vae.safetensors'
    ]

    for i in extras: download(i)
    SyS(f"unzip -qo {W / 'embeddingsXL.zip'} -d {E} && rm {W / 'embeddingsXL.zip'}")

    if U != 'SwarmUI': WebUIExtensions(U, W, M)

def webui_install(ui):
    with loading:
        display(Image(filename=str(IMG)))

    with output:
        if ui in REPO:
            WEBUI = HOME / ui
            repo = REPO[ui]

        say(f"<b>【{{red}} Installing {ui.replace('-', '')}{{d}} 】{{red}}</b>")
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

def facetrainer(ui):
    with loading:
        display(Image(filename=str(IMG)))

    SDTFusion = {
        'FaceFusion': ('--depth 1 https://github.com/LaoJiuYes/facefusion-lockless FaceFusion', TMP / 'venv-fusion'),
        'SDTrainer': ('--recurse-submodules https://github.com/Akegarasu/lora-scripts SDTrainer', TMP / 'venv-sd-trainer'),
    }

    with output:
        if ui in SDTFusion:
            WEBUI = HOME / ui
            repo, vnv = SDTFusion[ui]

        say(f"<b>【{{red}} Installing {ui.replace('-', '')}{{d}} 】{{red}}</b>")
        clone(repo)

        marking(SRC, MARKED, ui)
        tmp_cleaning(vnv)

        if ui == 'FaceFusion':
            check_ffmpeg()
            req = [f'rm -rf {HOME}/tmp {HOME}/.cache/*', f'ln -vs /tmp {HOME}/tmp']
        else:
            req = [
                f'rm -rf {HOME}/tmp {HOME}/.cache/*', f'mkdir -p {WEBUI}/dataset',
                f'mkdir -p {WEBUI}/VAE', f'ln -vs /tmp {HOME}/tmp'
            ]

        for lines in req: SyS(f'{lines} > /dev/null 2>&1')
        for items in SM_Script(WEBUI): download(items)
        tempe()

        with loading:
            loading.clear_output(wait=True)
            get_ipython().run_line_magic('run', str(MRK))
            get_ipython().run_line_magic('run', str(WEBUI / 'venv.py'))

            loading.clear_output(wait=True)
            say('<b>【{red} Done{d} 】{red}</b>')
            CD(HOME)

def oppai(ui):
    multi_panel.layout.display = 'none'

    config = json.load(MARKED.open('r')) if MARKED.exists() else {}
    current_ui = config.get('ui')
    WEBUI = HOME / ui if ui else None

    if WEBUI and WEBUI.exists():
        git_dir = WEBUI / '.git'
        if git_dir.exists():
            CD(WEBUI)
            with output:
                if ui in ['A1111', 'ComfyUI', 'SwarmUI', 'FaceFusion']:
                    SyS('git pull origin master')

                elif ui in ['Forge', 'ReForge', 'SDTrainer']:
                    SyS('git pull origin main')

                else:
                    SyS('git pull origin classic')

                x = SM_Script(WEBUI)

                if ui and ui not in ['SDTrainer', 'FaceFusion']:
                    x.append(CN_Script(WEBUI))

                print()
                for y in x: download(y)

    else:
        if current_ui and current_ui != ui:
            webui = HOME / current_ui
            with output:
                if webui.exists():
                    print(f'{current_ui} is installed. uninstall it before switching to {ui}.')
                    return

        if ui in ['FaceFusion', 'SDTrainer']:
            facetrainer(ui)
        else:
            webui_install(ui)

output = widgets.Output()
loading = widgets.Output()

row1 = ['A1111', 'Forge', 'ReForge', 'Forge-Classic']
buttons1 = [widgets.Button(description='') for btn in row1]
for button, btn in zip(buttons1, row1):
    button.add_class(btn.lower())
    button.add_class('segs-setup-buttons')
    button.on_click(lambda x, btn=btn: oppai(btn))

row2 = ['ComfyUI', 'SwarmUI', 'FaceFusion', 'SDTrainer']
buttons2 = [widgets.Button(description='') for btn in row2]
for button, btn in zip(buttons2, row2):
    button.add_class(btn.lower())
    button.add_class('segs-setup-buttons')
    button.on_click(lambda x, btn=btn: oppai(btn))

hbox1 = widgets.HBox(buttons1, layout=widgets.Layout(width='100%', height='255px'))
hbox2 = widgets.HBox(buttons2, layout=widgets.Layout(width='100%', height='255px'))
multi_panel = widgets.VBox([hbox1, hbox2], layout=widgets.Layout(width='100%', height='520px'))
multi_panel.add_class('multi-panel')
hbox1.add_class('hbox1')
hbox2.add_class('hbox2')

def Segsmaker_Setup_Widgets():
    for cmd in [
        f'curl -sLo {CSS} https://github.com/gutris1/segsmaker/raw/main/script/SM/setup.css',
        f'curl -sLo {IMG} https://github.com/gutris1/segsmaker/raw/main/script/loading.png',
        f'curl -sLo {MRK} https://github.com/gutris1/segsmaker/raw/main/script/marking.py'
    ]: SyS(cmd)

    Load_CSS()
    display(multi_panel, output, loading)

CD(HOME)
Segsmaker_Setup_Widgets()
