import sys, subprocess

python_version = subprocess.run(['python', '--version'], capture_output=True, text=True).stdout.split()[1]
if tuple(map(int, python_version.split('.'))) < (3, 10, 6):
    print(f"[ERROR]: Python version 3.10.6 or higher required, and you are using Python {python_version}\nExiting.")
    sys.exit()

from IPython.display import display, HTML, clear_output, Image
from ipywidgets import widgets
from pathlib import Path
import time, os, shlex, json, shutil
from IPython import get_ipython
from nenen88 import pull, say, download, clone, tempe


HOME = Path.home()
os.chdir(HOME)
SRC = HOME / '.gutris1'
CSS = SRC / 'setup.css'
IMG = SRC / 'loading.png'
MRK = SRC / 'marking.py'
MARKED = SRC / 'marking.json'
TMP = Path('/tmp')

SRC.mkdir(parents=True, exist_ok=True)

version = "v1.10.1"

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
            subprocess.run(shlex.split(d), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

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
    if U == 'A1111':
        return [
            f"rm -rf {HOME}/tmp {HOME}/.cache/*",
            f"rm -rf {M}/Stable-diffusion/tmp_ckpt",
            f"rm -rf {M}/Lora/tmp_lora {M}/ControlNet",
            f"mkdir -p {M}/Lora {M}/ESRGAN",
            f"ln -vs {TMP} {HOME}/tmp",
            f"ln -vs {TMP}/ckpt {M}/Stable-diffusion/tmp_ckpt",
            f"ln -vs {TMP}/lora {M}/Lora/tmp_lora",
            f"ln -vs {TMP}/controlnet {M}/ControlNet"
        ]

    elif U == 'ComfyUI':
        return [
            f"rm -rf {HOME}/tmp {HOME}/.cache/*",
            f"rm -rf {M}/controlnet {M}/clip",
            f"rm -rf {M}/checkpoints/tmp_ckpt {M}/loras/tmp_lora",
            f"ln -vs {TMP} {HOME}/tmp",
            f"ln -vs {TMP}/ckpt {M}/checkpoints/tmp_ckpt",
            f"ln -vs {TMP}/lora {M}/loras/tmp_lora",
            f"ln -vs {TMP}/controlnet {M}/controlnet",
            f"ln -vs {TMP}/clip {M}/clip",
            f"ln -vs {M}/checkpoints {M}/checkpoints_symlink"
        ]

    elif U in ['Forge', 'ReForge']:
        return [
            f"rm -rf {HOME}/tmp {HOME}/.cache/*",
            f"rm -rf {M}/ControlNet {M}/svd {M}/z123",
            f"rm -rf {M}/Stable-diffusion/tmp_ckpt {M}/Lora/tmp_lora",
            f"mkdir -p {M}/Lora {M}/ESRGAN",
            f"ln -vs {TMP} {HOME}/tmp",
            f"ln -vs {TMP}/ckpt {M}/Stable-diffusion/tmp_ckpt",
            f"ln -vs {TMP}/lora {M}/Lora/tmp_lora",
            f"ln -vs {TMP}/controlnet {M}/ControlNet",
            f"ln -vs {TMP}/z123 {M}/z123",
            f"ln -vs {TMP}/svd {M}/svd"
        ]

    elif U == 'SwarmUI':
        return [
            f"rm -rf {HOME}/tmp {HOME}/.cache/*",
            f"rm -rf {M}/Stable-Diffusion/tmp_ckpt",
            f"rm -rf {M}/Lora/tmp_lora {M}/controlnet {M}/clip",
            f"ln -vs {TMP} {HOME}/tmp",
            f"ln -vs {TMP}/ckpt {M}/Stable-Diffusion/tmp_ckpt",
            f"ln -vs {TMP}/lora {M}/Lora/tmp_lora",
            f"ln -vs {TMP}/controlnet {M}/controlnet",
            f"ln -vs {TMP}/clip {M}/clip"
        ]

def webui_req(U, W, M):
    vnv = TMP / 'venv'
    tmp_cleaning(vnv)
    os.chdir(W)

    if U == 'A1111':
        pull(f"https://github.com/gutris1/segsmaker a1111 {W}")
    elif U == 'Forge':
        pull(f"https://github.com/gutris1/segsmaker forge {W}")
    elif U == 'ComfyUI':
        pull(f"https://github.com/gutris1/segsmaker comfyui {W}")
    elif U == 'ReForge':
        pull(f"https://github.com/gutris1/segsmaker reforge {W}")
    elif U == 'SwarmUI':
        M.mkdir(parents=True, exist_ok=True)

        dirs = ['Stable-Diffusion', 'Lora', 'Embeddings', 'VAE', 'upscale_models']
        for sub in dirs:
            (M / sub).mkdir(parents=True, exist_ok=True)

        download(f"https://dot.net/v1/dotnet-install.sh {W}")

        dotnet = W / 'dotnet-install.sh'
        dotnet.chmod(0o755)
        get_ipython().system("bash ./dotnet-install.sh --channel 8.0")

    req = sym_link(U, M)
    for lines in req:
        subprocess.run(shlex.split(lines), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

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

def Extensions(U, W, M):
    if U == 'ComfyUI':
        say("<br><b>【{red} Installing Custom Nodes{d} 】{red}</b>")
        os.chdir(W / "custom_nodes")
        clone(str(W / "asd/custom_nodes.txt"))
        print()

        custom_nodes_models = [
            f"https://github.com/sczhou/CodeFormer/releases/download/v0.1.0/codeformer.pth {M}/facerestore_models",
            f"https://github.com/TencentARC/GFPGAN/releases/download/v1.3.4/GFPGANv1.4.pth {M}/facerestore_models"
        ]

        for item in custom_nodes_models:
            download(item)

    else:
        say("<br><b>【{red} Installing Extensions{d} 】{red}</b>")
        os.chdir(W / "extensions")
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
            f"https://huggingface.co/stabilityai/sdxl-vae/resolve/main/sdxl_vae.safetensors {V}"
        ]

    for item in extras:
        download(item)

    get_ipython().system(f"unzip -qo {embzip} -d {E} && rm {embzip}")

    if U != 'SwarmUI':
        Extensions(U, W, M)

def webui_install(ui, which_sd):
    with loading:
        display(Image(filename=str(IMG)))

    with output:
        if ui == 'A1111':
            WEBUI = HOME / 'A1111'
            repo = f'git clone --depth 1 -q -b {version} https://github.com/gutris1/A1111'
            say("<b>【{red} Installing A1111{d} 】{red}</b>")

        elif ui == 'Forge':
            WEBUI = HOME / 'Forge'
            repo = 'git clone --depth 1 -q https://github.com/lllyasviel/stable-diffusion-webui-forge Forge'
            say("<b>【{red} Installing Forge{d} 】{red}</b>")

        elif ui == 'ComfyUI':
            WEBUI = HOME / 'ComfyUI'
            repo = 'git clone --depth 1 -q https://github.com/comfyanonymous/ComfyUI'
            say("<b>【{red} Installing ComfyUI{d} 】{red}</b>")

        elif ui == 'ReForge':
            WEBUI = HOME / 'ReForge'
            repo = 'git clone --depth 1 -q https://github.com/Panchovix/stable-diffusion-webui-reForge ReForge'
            say("<b>【{red} Installing ReForge{d} 】{red}</b>")

        elif ui == 'SwarmUI':
            WEBUI = HOME / 'SwarmUI'
            repo = 'git clone --depth 1 -q https://github.com/mcmonkeyprojects/SwarmUI'
            say("<b>【{red} Installing SwarmUI{d} 】{red}</b>")

        MODELS = WEBUI / 'Models' if ui == 'SwarmUI' else WEBUI / 'models'
        EMB = MODELS / 'Embeddings' if ui == 'SwarmUI' else (MODELS / 'embeddings' if ui == 'ComfyUI' else WEBUI / 'embeddings')
        VAE = MODELS / 'vae' if ui == 'ComfyUI' else MODELS / 'VAE'

        get_ipython().system(repo)
        time.sleep(1)

        marking(SRC, MARKED, ui)
        installing_webui(ui, which_sd, WEBUI, MODELS, EMB, VAE)
        tempe()

        with loading:
            loading.clear_output(wait=True)
            get_ipython().run_line_magic('run', str(MRK))
            get_ipython().run_line_magic('run', str(WEBUI / 'venv.py'))

            os.chdir(HOME)
            loading.clear_output(wait=True)
            say("<b>【{red} Done{d} 】{red}</b>")

def facetrainer(ui):
    with loading:
        display(Image(filename=str(IMG)))
    
    with output:
        if ui == 'FaceFusion':
            WEBUI = HOME / 'FaceFusion'
            vnv = TMP / 'venv-fusion'
            repo = 'git clone --depth 1 https://github.com/LaoJiuYes/facefusion-lockless FaceFusion'
            say("<b>【{red} Installing Face Fusion{d} 】{red}</b>")

        elif ui == 'SDTrainer':
            WEBUI = HOME / 'SDTrainer'
            vnv = TMP / 'venv-sd-trainer'
            repo = 'git clone --recurse-submodules https://github.com/Akegarasu/lora-scripts SDTrainer'
            say("<b>【{red} Installing SD Trainer{d} 】{red}</b>")
        
        get_ipython().system(repo)
        time.sleep(1)
        
        marking(SRC, MARKED, ui)
        tmp_cleaning(vnv)

        if ui == 'FaceFusion':
            check_ffmpeg()
            req = [
                f"rm -rf {HOME}/tmp {HOME}/.cache/*",
                f"ln -vs /tmp {HOME}/tmp"
            ]
        else:
            req = [
                f"rm -rf {HOME}/tmp {HOME}/.cache/*",
                f"mkdir -p {WEBUI}/dataset",
                f"mkdir -p {WEBUI}/VAE",
                f"ln -vs /tmp {HOME}/tmp"
            ]
            
        for lines in req:
            subprocess.run(shlex.split(lines), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

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

            os.chdir(HOME)
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
            os.chdir(WEBUI)
            with output:
                commit_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip().decode('utf-8')

                if ui == 'A1111':
                    if commit_hash != version:
                        get_ipython().system(f"git pull origin {version}")

                elif ui in ['ComfyUI', 'SwarmUI', 'FaceFusion']:
                    get_ipython().system("git pull origin master")

                elif ui in ['Forge', 'ReForge', 'SDTrainer']:
                    get_ipython().system("git pull origin main")

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
        get_ipython().system(y)

    load_css()
    display(multi_panel, hbox, output, loading)

multi_widgets()
