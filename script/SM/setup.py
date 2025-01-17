R = "\033[31m"
P = "\033[38;5;135m"
RST = "\033[0m"
ERR = f"{P}[{RST}{R}ERROR{RST}{P}]{RST}"

import sys, subprocess
python_version = subprocess.run(['python', '--version'], capture_output=True, text=True).stdout.split()[1]
if tuple(map(int, python_version.split('.'))) < (3, 10, 6):
    print(f"{ERR}: Python version 3.10.6 or higher required, and you are using Python {python_version}")
    sys.exit()

from IPython.display import display, HTML, clear_output, Image
from IPython import get_ipython
from ipywidgets import widgets
from pathlib import Path
import shutil
import json
import time
import os

from nenen88 import pull, say, download, clone, tempe

SyS = get_ipython().system
CD = os.chdir

HOME = Path.home()
CD(HOME)
SRC = HOME / '.gutris1'
CSS = SRC / 'setup.css'
IMG = SRC / 'loading.png'
MRK = SRC / 'marking.py'
MARKED = SRC / 'marking.json'
TMP = Path('/tmp')

SRC.mkdir(parents=True, exist_ok=True)

def load_css():
    with open(CSS, "r") as f:
        d = f.read()
    display(HTML(f"<style>{d}</style>"))

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
            ('conda install -qy ffmpeg curl', '\ninstalling ffmpeg...'),
            ('conda install -qy cuda-runtime=12.4.1', 'installing cuda-runtime=12.4.1...'),
            ('conda install -qy cudnn=9.2.1.18', 'installing cudnn=9.2.1.18...'),
            ('conda clean -qy --all', None)
        ]

        for d, m in c:
            if m is not None:
                print(m)
            SyS(f'{d} &> /dev/null')

def marking(p, n, i):
    t = p / n
    v = {
        'ui': i,
        'launch_args': '',
        'zrok_token': '',
        'ngrok_token': '',
        'tunnel': ''
    }

    if not t.exists():
        with open(t, 'w') as f:
            json.dump(v, f, indent=4)

    with open(t, 'r') as f:
        d = json.load(f)

    d.update({
        'ui': i,
        'launch_args': ''
    })

    with open(t, 'w') as f:
        json.dump(d, f, indent=4)

def sym_link(U, M):
    links = {
        'A1111': [
            f"rm -rf {HOME}/tmp {HOME}/.cache/* {M}/Stable-diffusion/tmp_ckpt {M}/Lora/tmp_lora {M}/ControlNet",
            f"mkdir -p {M}/Lora {M}/ESRGAN",
            f"ln -vs {TMP} {HOME}/tmp",
            f"ln -vs {TMP}/ckpt {M}/Stable-diffusion/tmp_ckpt",
            f"ln -vs {TMP}/lora {M}/Lora/tmp_lora",
            f"ln -vs {TMP}/controlnet {M}/ControlNet"
        ],

        'ComfyUI': [
            f"rm -rf {HOME}/tmp {HOME}/.cache/* {M}/controlnet {M}/clip {M}/unet",
            f"rm -rf {M}/checkpoints/tmp_ckpt {M}/loras/tmp_lora",
            f"ln -vs {TMP} {HOME}/tmp",
            f"ln -vs {TMP}/ckpt {M}/checkpoints/tmp_ckpt",
            f"ln -vs {TMP}/lora {M}/loras/tmp_lora",
            f"ln -vs {TMP}/controlnet {M}/controlnet",
            f"ln -vs {TMP}/clip {M}/clip",
            f"ln -vs {TMP}/unet {M}/unet",
            f"ln -vs {M}/checkpoints {M}/checkpoints_symlink"
        ],

        'Forge': [
            f"rm -rf {HOME}/tmp {HOME}/.cache/* {M}/ControlNet {M}/svd {M}/z123 {M}/clip {M}/unet",
            f"rm -rf {M}/Stable-diffusion/tmp_ckpt {M}/Lora/tmp_lora",
            f"mkdir -p {M}/Lora {M}/ESRGAN",
            f"ln -vs {TMP} {HOME}/tmp",
            f"ln -vs {TMP}/ckpt {M}/Stable-diffusion/tmp_ckpt",
            f"ln -vs {TMP}/lora {M}/Lora/tmp_lora",
            f"ln -vs {TMP}/controlnet {M}/ControlNet",
            f"ln -vs {TMP}/z123 {M}/z123",
            f"ln -vs {TMP}/svd {M}/svd",
            f"ln -vs {TMP}/clip {M}/clip",
            f"ln -vs {TMP}/unet {M}/unet"
        ],

        'ReForge': [
            f"rm -rf {HOME}/tmp {HOME}/.cache/* {M}/ControlNet {M}/svd {M}/z123",
            f"rm -rf {M}/Stable-diffusion/tmp_ckpt {M}/Lora/tmp_lora",
            f"mkdir -p {M}/Lora {M}/ESRGAN",
            f"ln -vs {TMP} {HOME}/tmp",
            f"ln -vs {TMP}/ckpt {M}/Stable-diffusion/tmp_ckpt",
            f"ln -vs {TMP}/lora {M}/Lora/tmp_lora",
            f"ln -vs {TMP}/controlnet {M}/ControlNet",
            f"ln -vs {TMP}/z123 {M}/z123",
            f"ln -vs {TMP}/svd {M}/svd"
        ],

        'SwarmUI': [
            f"rm -rf {HOME}/tmp {HOME}/.cache/* {M}/Stable-Diffusion/tmp_ckpt",
            f"rm -rf {M}/Lora/tmp_lora {M}/controlnet {M}/clip {M}/unet",
            f"ln -vs {TMP} {HOME}/tmp",
            f"ln -vs {TMP}/ckpt {M}/Stable-Diffusion/tmp_ckpt",
            f"ln -vs {TMP}/lora {M}/Lora/tmp_lora",
            f"ln -vs {TMP}/controlnet {M}/controlnet",
            f"ln -vs {TMP}/clip {M}/clip",
            f"ln -vs {TMP}/unet {M}/unet"
        ]
    }

    return links.get(U, [])

def webui_req(U, W, M):
    vnv = TMP / 'venv'
    tmp_cleaning(vnv)
    CD(W)

    if U in ['A1111', 'Forge', 'ComfyUI', 'ReForge']:
        pull(f"https://github.com/gutris1/segsmaker {U.lower()} {W}")
    elif U == 'SwarmUI':
        M.mkdir(parents=True, exist_ok=True)
        for sub in ['Stable-Diffusion', 'Lora', 'Embeddings', 'VAE', 'upscale_models']:
            (M / sub).mkdir(parents=True, exist_ok=True)

        download(f"https://dot.net/v1/dotnet-install.sh {W}")
        dotnet = W / 'dotnet-install.sh'
        dotnet.chmod(0o755)
        SyS("bash ./dotnet-install.sh --channel 8.0")

    req = sym_link(U, M)
    for ln in req:
        SyS(f'{ln} &> /dev/null')

    scripts = [
        f"https://github.com/gutris1/segsmaker/raw/main/script/SM/controlnet.py {W}/asd",
        f"https://github.com/gutris1/segsmaker/raw/main/script/SM/venv.py {W}",
        f"https://github.com/gutris1/segsmaker/raw/main/script/SM/Launcher.py {W}",
        f"https://github.com/gutris1/segsmaker/raw/main/script/SM/segsmaker.py {W}"
    ]

    u = M / 'upscale_models' if U in ['ComfyUI', 'SwarmUI'] else M / 'ESRGAN'
    upscalers = [
        f"https://huggingface.co/pantat88/ui/resolve/main/4x-UltraSharp.pth {u}",
        f"https://huggingface.co/pantat88/ui/resolve/main/4x-AnimeSharp.pth {u}",
        f"https://huggingface.co/pantat88/ui/resolve/main/4x_NMKD-Superscale-SP_178000_G.pth {u}",
        f"https://huggingface.co/uwg/upscaler/resolve/main/ESRGAN/8x_NMKD-Superscale_150000_G.pth {u}",
        f"https://huggingface.co/pantat88/ui/resolve/main/4x_RealisticRescaler_100000_G.pth {u}",
        f"https://huggingface.co/pantat88/ui/resolve/main/8x_RealESRGAN.pth {u}",
        f"https://huggingface.co/pantat88/ui/resolve/main/4x_foolhardy_Remacri.pth {u}"
    ]

    line = scripts + upscalers
    for item in line:
        download(item)

    if U not in ['SwarmUI', 'ComfyUI']:
        SyS(f'rm -f {W}/html/card-no-preview.png')
        download(f'https://huggingface.co/pantat88/ui/resolve/main/card-no-preview.png {W}/html')

def WebUIExtensions(U, W, M):
    EXT = W / "custom_nodes" if U == 'ComfyUI' else W / "extensions"
    CD(EXT)

    if U == 'ComfyUI':
        say("<br><b>【{red} Installing Custom Nodes{d} 】{red}</b>")
        clone(str(W / "asd/custom_nodes.txt"))
        print()

        for faces in [
            f"https://github.com/sczhou/CodeFormer/releases/download/v0.1.0/codeformer.pth {M}/facerestore_models",
            f"https://github.com/TencentARC/GFPGAN/releases/download/v1.3.4/GFPGANv1.4.pth {M}/facerestore_models"
        ]:
            download(faces)

    else:
        say("<br><b>【{red} Installing Extensions{d} 】{red}</b>")
        clone(str(W / "asd/extension.txt"))

def installing_webui(U, S, W, M, E, V):
    webui_req(U, W, M)

    if S == "button-15":
        embzip =  W / 'embeddings.zip'
        extras = [
            f"https://huggingface.co/pantat88/ui/resolve/main/embeddings.zip {W}",
            f"https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.safetensors {V}"
        ]

    elif S == "button-xl":
        embzip = W / 'embeddingsXL.zip'
        extras = [
            f"https://huggingface.co/pantat88/ui/resolve/main/embeddingsXL.zip {W}",
            f"https://huggingface.co/madebyollin/sdxl-vae-fp16-fix/resolve/main/sdxl.vae.safetensors {V} sdxl_vae.safetensors"
        ]

    for item in extras:
        download(item)

    SyS(f"unzip -qo {embzip} -d {E} && rm {embzip}")

    if U != 'SwarmUI':
        WebUIExtensions(U, W, M)

def webui_install(ui, which_sd):
    with loading:
        display(Image(filename=str(IMG)))

    with output:
        alist = {
            'A1111': 'https://github.com/AUTOMATIC1111/stable-diffusion-webui A1111',
            'Forge': 'https://github.com/lllyasviel/stable-diffusion-webui-forge Forge',
            'ComfyUI': 'https://github.com/comfyanonymous/ComfyUI',
            'ReForge': 'https://github.com/Panchovix/stable-diffusion-webui-reForge ReForge',
            'SwarmUI': 'https://github.com/mcmonkeyprojects/SwarmUI'
        }
        
        if ui in alist:
            WEBUI = HOME / ui
            repo = alist[ui]

        MODELS = WEBUI / 'Models' if ui == 'SwarmUI' else WEBUI / 'models'
        EMB = MODELS / 'Embeddings' if ui == 'SwarmUI' else (MODELS / 'embeddings' if ui == 'ComfyUI' else WEBUI / 'embeddings')
        VAE = MODELS / 'vae' if ui == 'ComfyUI' else MODELS / 'VAE'

        say(f"<b>【{{red}} Installing {WEBUI.name}{{d}} 】{{red}}</b>")
        clone(repo)
        time.sleep(1)

        marking(SRC, MARKED, ui)
        installing_webui(ui, which_sd, WEBUI, MODELS, EMB, VAE)
        tempe()

        with loading:
            loading.clear_output(wait=True)
            get_ipython().run_line_magic('run', str(MRK))
            get_ipython().run_line_magic('run', str(WEBUI / 'venv.py'))

            CD(HOME)
            loading.clear_output(wait=True)
            say("<b>【{red} Done{d} 】{red}</b>")

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

        say(f"<b>【{{red}} Installing {WEBUI.name}{{d}} 】{{red}}</b>")
        clone(repo)
        time.sleep(1)

        marking(SRC, MARKED, ui)
        tmp_cleaning(vnv)

        if ui == 'FaceFusion':
            check_ffmpeg()
            req = [
                f"rm -rf {HOME}/tmp {HOME}/.cache/*", f"ln -vs /tmp {HOME}/tmp"
            ]
        else:
            req = [
                f"rm -rf {HOME}/tmp {HOME}/.cache/*", f"mkdir -p {WEBUI}/dataset",
                f"mkdir -p {WEBUI}/VAE", f"ln -vs /tmp {HOME}/tmp"
            ]

        for lines in req:
            SyS(f'{lines} &> /dev/null')

        scripts = [
            f"https://github.com/gutris1/segsmaker/raw/main/script/SM/venv.py {WEBUI}",
            f"https://github.com/gutris1/segsmaker/raw/main/script/SM/Launcher.py {WEBUI}",
            f"https://github.com/gutris1/segsmaker/raw/main/script/SM/segsmaker.py {WEBUI}"
        ]

        for items in scripts:
            download(items)

        tempe()

        with loading:
            loading.clear_output(wait=True)
            get_ipython().run_line_magic('run', str(MRK))
            get_ipython().run_line_magic('run', str(WEBUI / 'venv.py'))

            CD(HOME)
            loading.clear_output(wait=True)
            say("<b>【{red} Done{d} 】{red}</b>")

def oppai(btn, sd=None):
    global ui, hbox
    ui = btn
    multi_panel.layout.display = 'none'

    config = json.load(MARKED.open('r')) if MARKED.exists() else {}
    cui = config.get('ui')
    WEBUI = HOME / ui if ui else None

    if WEBUI and WEBUI.exists():
        git_dir = WEBUI / '.git'
        if git_dir.exists():
            CD(WEBUI)
            with output:
                if ui in ['A1111', 'ComfyUI', 'SwarmUI', 'FaceFusion']:
                    SyS("git pull origin master")

                elif ui in ['Forge', 'ReForge', 'SDTrainer']:
                    SyS("git pull origin main")

                x = [
                    f"https://github.com/gutris1/segsmaker/raw/main/script/SM/venv.py {WEBUI}",
                    f"https://github.com/gutris1/segsmaker/raw/main/script/SM/Launcher.py {WEBUI}",
                    f"https://github.com/gutris1/segsmaker/raw/main/script/SM/segsmaker.py {WEBUI}"
                ]

                if ui not in ['SDTrainer', 'FaceFusion']:
                    x.append(f"https://github.com/gutris1/segsmaker/raw/main/script/SM/controlnet.py {WEBUI}/asd")

                print()
                for y in x:
                    download(y)

    else:
        if cui and cui != ui:
            ass = HOME / cui
            with output:
                if ass.exists():
                    print(f"{cui} is installed. uninstall it before switching to {ui}.")
                    return

        if ui in ['FaceFusion', 'SDTrainer']:
            facetrainer(ui)
        else:
            if sd:
                hbox.layout.display = 'none'
                webui_install(ui, sd)
            else:
                hbox.layout.display = 'flex'

def select_webui(btn):
    oppai(btn)

def select_sd(sd):
    oppai(ui, sd)

output = widgets.Output()
loading = widgets.Output()

row1 = ['A1111', 'Forge', 'ComfyUI', 'ReForge']
buttons1 = [widgets.Button(description='') for btn in row1]
for button, btn in zip(buttons1, row1):
    button.add_class(btn.lower())
    button.on_click(lambda x, btn=btn: select_webui(btn))

row2 = ['SwarmUI', 'FaceFusion', 'SDTrainer']
buttons2 = [widgets.Button(description='') for btn in row2]
for button, btn in zip(buttons2, row2):
    button.add_class(btn.lower())
    button.on_click(lambda x, btn=btn: select_webui(btn))

hbox1 = widgets.HBox(buttons1, layout=widgets.Layout(width='630px', height='250px'))
hbox2 = widgets.HBox(buttons2, layout=widgets.Layout(width='630px', height='250px'))
multi_panel = widgets.VBox([hbox1, hbox2], layout=widgets.Layout(width='600px', height='500px'))
multi_panel.add_class('multi-panel')

which_sd = ['button-15', 'button-back', 'button-xl']
buttons3 = [widgets.Button(description='') for btn in which_sd]
for button, btn in zip(buttons3, which_sd):
    button.add_class(btn.lower())
    if btn == 'button-back':
        button.on_click(lambda x: go_back(btn))
    else:
        button.on_click(lambda x, btn=btn: select_sd(btn))

hbox = widgets.HBox(buttons3, layout=widgets.Layout(width='450px', height='250px'))
hbox.add_class("multi-panel")
hbox.layout.display = 'none'

def go_back(b):
    hbox.layout.display = 'none'
    clear_output()
    multi_panel.layout.display = 'block'
    
    config = json.load(MARKED.open('r')) if MARKED.exists() else {}
    config['ui'] = None
    json.dump(config, MARKED.open('w'))

def multi_widgets():
    x = [
        f"curl -sLo {CSS} https://github.com/gutris1/segsmaker/raw/main/script/SM/setup.css",
        f"curl -sLo {IMG} https://github.com/gutris1/segsmaker/raw/main/script/SM/loading.png",
        f"curl -sLo {MRK} https://github.com/gutris1/segsmaker/raw/main/script/SM/marking.py"
    ]
    for y in x:
        SyS(y)

    load_css()
    display(multi_panel, hbox, output, loading)

multi_widgets()
