from IPython.display import display, Image, clear_output
from IPython import get_ipython
from pathlib import Path
import argparse, sys, json, os, subprocess, shlex, time, re

R = "\033[31m"
P = "\033[38;5;135m"
RST = "\033[0m"
ERR = f"{P}[{RST}{R}ERROR{RST}{P}]{RST}"

IMG = "https://github.com/gutris1/segsmaker/raw/main/script/SM/loading.png"
display(Image(url=IMG))
clear_output(wait=True)

ENVNAME, ENVBASE, ENVHOME = None, None, None
env_list = {
    'Colab': ('/content', '/content', 'COLAB_JUPYTER_TRANSPORT'),
    'Kaggle': ('/kaggle', '/kaggle/working', 'KAGGLE_DATA_PROXY_TOKEN')
}
for envname, (envbase, envhome, envvar) in env_list.items():
    if os.getenv(envvar):
        ENVNAME = envname
        ENVBASE = envbase
        ENVHOME = envhome
        break

if not ENVNAME:
    print("You are not in Kaggle or Google Colab.\nExiting.")
    sys.exit()

HOME = Path(ENVHOME)
BASEPATH = Path(ENVBASE)
TMP = BASEPATH / 'temp'
VNV = BASEPATH / 'venv'

SRC = HOME / 'gutris1'
MRK = SRC / 'marking.py'
KEY = SRC / 'api-key.json'
MARKED = SRC / 'marking.json'

STR = Path('/root/.ipython/profile_default/startup')
nenen = STR / "nenen88.py"
pantat = STR / "pantat88.py"
KANDANG = STR / 'KANDANG.py'

TMP.mkdir(parents=True, exist_ok=True)
SRC.mkdir(parents=True, exist_ok=True)

VALID_WEBUI_OPTIONS = ["A1111", "Forge", "ComfyUI", "ReForge", "SwarmUI"]
VALID_SD_OPTIONS = ["1.5", "xl"]

def prevent_silly():
    parser = argparse.ArgumentParser(description="WebUI Installer Script for Kaggle and Google Colab")
    parser.add_argument('--webui', required=True, help="available webui: A1111, Forge, ComfyUI, ReForge, SwarmUI")
    parser.add_argument('--sd', required=True, help="available sd: 1.5, xl")
    parser.add_argument('--civitai_key', required=True, help="your CivitAI API key")
    parser.add_argument('--hf_read_token', default=None, help="your Huggingface READ Token (optional)")

    args = parser.parse_args()

    arg1 = args.webui.lower()
    arg2 = args.sd.lower()
    arg3 = args.civitai_key.strip()
    arg4 = args.hf_read_token.strip() if args.hf_read_token else ""

    if not any(arg1 == option.lower() for option in VALID_WEBUI_OPTIONS):
        print(f"{ERR}: invalid webui option: '{args.webui}'")
        print(f"Available webui options: {', '.join(VALID_WEBUI_OPTIONS)}")
        return None, None, None

    if not any(arg2 == option.lower() for option in VALID_SD_OPTIONS):
        print(f"{ERR}: invalid sd option: '{args.sd}'")
        print(f"Available sd options: {', '.join(VALID_SD_OPTIONS)}")
        return None, None, None

    if not arg3:
        print(f"{ERR}: CivitAI API key is missing.")
        return None, None, None
    if re.search(r'\s+', arg3):
        print(f"{ERR}: CivitAI API key contains spaces '{arg3}' - not allowed.")
        return None, None, None
    if len(arg3) < 32:
        print(f"{ERR}: CivitAI API key must be at least 32 characters long.")
        return None, None, None

    if not arg4:
        arg4 = ""
    if re.search(r'\s+', arg4):
        arg4 = ""

    webui_webui = next(option for option in VALID_WEBUI_OPTIONS if arg1 == option.lower())
    sd_sd = next(option for option in VALID_SD_OPTIONS if arg2 == option.lower())

    return (webui_webui, sd_sd), arg3, arg4


def saving():
    j = {
        "ENVNAME": ENVNAME,
        "HOMEPATH": HOME,
        "TEMPPATH": TMP,
        "VENVPATH": VNV,
        "BASEPATH": BASEPATH
    }
    
    with open(KANDANG, 'w') as q:
        for k, v in j.items():
            q.write(f"{k} = '{v}'\n")


def marking(p, n, u):
    t = p / n
    v = {'ui': u, 'launch_args': '', 'tunnel': ''}

    if not t.exists():
        with open(t, 'w') as f:
            json.dump(v, f, indent=4)

    with open(t, 'r') as f:
        d = json.load(f)

    d.update(v)
    with open(t, 'w') as f:
        json.dump(d, f, indent=4)


def key_inject(C, H):
    t = [pantat, nenen]

    for l in t:
        with open(l, "r") as w:
            v = w.read()

        v = v.replace('toket = ""', f'toket = "{C}"')
        v = v.replace('tobrut = ""', f'tobrut = "{H}"')

        with open(l, "w") as b:
            b.write(v)


def sym_link(U, M):
    if U == 'A1111':
        return [
            f"rm -rf {TMP}/* {M}/Stable-diffusion/tmp_ckpt",
            f"rm -rf {M}/Lora/tmp_lora {M}/ControlNet",
            f"mkdir -p {M}/Lora {M}/ESRGAN",
            f"ln -vs {TMP}/ckpt {M}/Stable-diffusion/tmp_ckpt",
            f"ln -vs {TMP}/lora {M}/Lora/tmp_lora",
            f"ln -vs {TMP}/controlnet {M}/ControlNet"
        ]

    elif U == 'ComfyUI':
        return [
            f"rm -rf {TMP}/* {M}/controlnet {M}/clip",
            f"rm -rf {M}/checkpoints/tmp_ckpt {M}/loras/tmp_lora",
            f"ln -vs {TMP}/ckpt {M}/checkpoints/tmp_ckpt",
            f"ln -vs {TMP}/lora {M}/loras/tmp_lora",
            f"ln -vs {TMP}/controlnet {M}/controlnet",
            f"ln -vs {TMP}/clip {M}/clip",
            f"ln -vs {M}/checkpoints {M}/checkpoints_symlink"
        ]

    elif U in ['Forge', 'ReForge']:
        return [
            f"rm -rf {TMP}/* {M}/ControlNet {M}/svd {M}/z123",
            f"rm -rf {M}/Stable-diffusion/tmp_ckpt {M}/Lora/tmp_lora",
            f"mkdir -p {M}/Lora {M}/ESRGAN",
            f"ln -vs {TMP}/ckpt {M}/Stable-diffusion/tmp_ckpt",
            f"ln -vs {TMP}/lora {M}/Lora/tmp_lora",
            f"ln -vs {TMP}/controlnet {M}/ControlNet",
            f"ln -vs {TMP}/z123 {M}/z123",
            f"ln -vs {TMP}/svd {M}/svd"
        ]

    elif U == 'SwarmUI':
        return [
            f"rm -rf {TMP}/* {M}/Stable-Diffusion/tmp_ckpt",
            f"rm -rf {M}/Lora/tmp_lora {M}/controlnet {M}/clip",
            f"ln -vs {TMP}/ckpt {M}/Stable-Diffusion/tmp_ckpt",
            f"ln -vs {TMP}/lora {M}/Lora/tmp_lora",
            f"ln -vs {TMP}/controlnet {M}/controlnet",
            f"ln -vs {TMP}/clip {M}/clip"
        ]


def webui_req(U, W, M):
    from nenen88 import pull, download

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
        f"https://github.com/gutris1/segsmaker/raw/main/script/KC/venv.py {W}",
        f"https://github.com/gutris1/segsmaker/raw/main/script/KC/segsmaker.py {W}"
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


def Extension(U, W, M):
    from nenen88 import clone, say, download

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

        if ENVNAME == 'Kaggle':
            clone('https://github.com/gutris1/sd-encrypt-image')


def installing_webui(U, S, W, M, E, V):
    from nenen88 import download

    webui_req(U, W, M)

    if S == "xl":
        embzip = W / 'embeddingsXL.zip'
        extras = [
            f"https://huggingface.co/pantat88/ui/resolve/main/embeddingsXL.zip {W}",
            f"https://huggingface.co/madebyollin/sdxl-vae-fp16-fix/resolve/main/sdxl.vae.safetensors {V} sdxl_vae.safetensors"
        ]

    else:
        embzip =  W / 'embeddings.zip'
        extras = [
            f"https://huggingface.co/pantat88/ui/resolve/main/embeddings.zip {W}",
            f"https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.safetensors {V}"
        ]

    for item in extras:
        download(item)

    get_ipython().system(f"unzip -qo {embzip} -d {E} && rm {embzip}")

    if U != 'SwarmUI':
        Extension(U, W, M)


def webui_install(ui, which_sd):
    from nenen88 import say, tempe

    alist = {
        'A1111': 'git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui A1111',
        'Forge': 'git clone https://github.com/lllyasviel/stable-diffusion-webui-forge Forge',
        'ComfyUI': 'git clone https://github.com/comfyanonymous/ComfyUI',
        'ReForge': 'git clone https://github.com/Panchovix/stable-diffusion-webui-reForge ReForge',
        'SwarmUI': 'git clone https://github.com/mcmonkeyprojects/SwarmUI'
    }
    
    if ui in alist:
        WEBUI = HOME / ui
        repo = alist[ui]

    MODELS = WEBUI / 'Models' if ui == 'SwarmUI' else WEBUI / 'models'
    EMB = MODELS / 'Embeddings' if ui == 'SwarmUI' else (MODELS / 'embeddings' if ui == 'ComfyUI' else WEBUI / 'embeddings')
    VAE = MODELS / 'vae' if ui == 'ComfyUI' else MODELS / 'VAE'

    say(f"<b>【{{red}} Installing {WEBUI.name}{{d}} 】{{red}}</b>")
    get_ipython().system(repo)

    req_list = [
        "curl -Lo /usr/bin/cl https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64",
        "apt -y install pv",
        "pip install -q gdown aria2",
        "chmod +x /usr/bin/cl"
    ]

    for items in req_list:
        subprocess.run(shlex.split(items), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    installing_webui(ui, which_sd, WEBUI, MODELS, EMB, VAE)

    get_ipython().run_line_magic('run', str(WEBUI / 'venv.py'))

    say("<br><b>【{red} Done{d} 】{red}</b>")

    tempe()
    os.chdir(HOME)


def lets_go():
    args, civitai_key, hf_read_token = prevent_silly()
    if args is None or civitai_key is None:
        return
    webui, sd = args

    z = [
        (STR / '00-startup.py', f"curl -sLo {STR}/00-startup.py https://github.com/gutris1/segsmaker/raw/main/script/KC/00-startup.py"),
        (pantat, f"curl -sLo {pantat} https://github.com/gutris1/segsmaker/raw/main/script/SM/pantat88.py"),
        (nenen, f"curl -sLo {nenen} https://github.com/gutris1/segsmaker/raw/main/script/SM/nenen88.py"),
        (STR / 'cupang.py', f"curl -sLo {STR}/cupang.py https://github.com/gutris1/segsmaker/raw/main/script/SM/cupang.py"),
        (MRK, f"curl -sLo {MRK} https://github.com/gutris1/segsmaker/raw/main/script/SM/marking.py")
    ]

    for x, y in z:
        if not Path(x).exists():
            get_ipython().system(y)

    config = json.load(MARKED.open('r')) if MARKED.exists() else {}
    ui = config.get('ui')
    WEBUI = HOME / ui if ui else None

    if WEBUI is not None and WEBUI.exists():
        git_dir = WEBUI / '.git'
        if git_dir.exists():
            os.chdir(WEBUI)
            if ui in ['A1111', 'ComfyUI', 'SwarmUI']:
                get_ipython().system("git pull origin master")
            elif ui in ['Forge', 'ReForge']:
                get_ipython().system("git pull origin main")

    else:
        display(Image(url=IMG))
        marking(SRC, MARKED, webui)
        key_inject(civitai_key, hf_read_token)
        sys.path.append(str(STR))

        var = [nenen, pantat, KANDANG, MRK]
        for scripts in var:
            get_ipython().run_line_magic('run', str(scripts))

        try:
            webui_install(webui, sd)
        except KeyboardInterrupt:
            print("\nCanceled.")


os.chdir(HOME)
saving()
lets_go()
