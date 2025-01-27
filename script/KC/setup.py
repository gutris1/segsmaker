from IPython.display import display, Image, clear_output
from IPython import get_ipython
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
    print("You are not in Kaggle or Google Colab.\nExiting.")
    sys.exit()

RST = "\033[0m"
R = "\033[31m"
P = "\033[38;5;135m"
ORANGE = "\033[38;5;208m"
AR = f'{ORANGE}▶{RST}'
ERR = f"{P}[{RST}{R}ERROR{RST}{P}]{RST}"
IMG = "https://github.com/gutris1/segsmaker/raw/main/script/SM/loading.png"

ROOT = Path.home()
SRE = ROOT / 'GUTRIS1'
BIN = str(SRE / 'bin')
PKG = str(SRE / 'lib/python3.10/site-packages')

HOME = Path(ENVHOME)
BASEPATH = Path(ENVBASE)
TMP = BASEPATH / 'temp'
VNV = BASEPATH / 'venv'

SRC = HOME / 'gutris1'
MRK = SRC / 'marking.py'
KEY = SRC / 'api-key.json'
MARKED = SRC / 'marking.json'

USR = Path('/usr/bin')
STR = ROOT / '.ipython/profile_default/startup'
nenen = STR / 'nenen88.py'
pantat = STR / 'pantat88.py'
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


def PythonPortable():
    CD(ROOT)
    SyS('sudo apt-get -qq -y install aria2 pv lz4')
    clear_output(wait=True)

    url = "https://huggingface.co/pantat88/back_up/resolve/main/python310-torch251-cu121.tar.lz4"
    fn = Path(url).name

    aria = f'aria2c --console-log-level=error --stderr=true -c -x16 -s16 -k1M -j5 {url} -o {fn}'
    pv = f'pv {fn} | lz4 -d | tar -xf -'

    Aria2Sub(aria)

    if ENVNAME == "Kaggle":
        for cmd in [
            'pip install ipywidgets jupyterlab_widgets --upgrade',
            'rm -f /usr/lib/python3.10/sitecustomize.py'
        ]: SyS(f'{cmd}>/dev/null 2>&1')
    else:
        print(f'\n{AR} installing Python...')

    SyS(pv)
    Path(ROOT / fn).unlink()

    if BIN not in iRON["PATH"]:
        iRON["PATH"] = BIN + ":" + iRON["PATH"]

    if PKG not in iRON["PYTHONPATH"]:
        iRON["PYTHONPATH"] = PKG + ":" + iRON["PYTHONPATH"]


def Aria2Sub(cmd):
    Aria2Process = subprocess.Popen(
        shlex.split(cmd),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    result = ""
    br = False
    while True:
        lines = Aria2Process.stderr.readline()
        if lines == '' and Aria2Process.poll() is not None:
            break
        if lines:
            result += lines
            for outputs in lines.splitlines():
                if re.match(r'\[#\w{6}\s.*\]', outputs):
                    lines = outputs.splitlines()
                    for line in lines:
                        print(f"\r{' '*500}\r {line}", end="")
                        sys.stdout.flush()
                    br = True
                    break
    if br:
        print()
    stripe = result.find("======+====+===========")
    if stripe:
        for lines in result[stripe:].splitlines():
            if '|' in lines and 'OK' in lines:
                print(f"  {lines}")
    Aria2Process.wait()


def install_tunnel():
    SyS(f'wget -qO {USR}/cl https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64')
    SyS(f'chmod +x {USR}/cl')

    bins = {
        "zrok": {
            "bin": USR / 'zrok',
            "url": "https://github.com/openziti/zrok/releases/download/v0.4.44/zrok_0.4.44_linux_amd64.tar.gz"
        },
        "ngrok": {
            "bin": USR / 'ngrok',
            "url": "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz"
        }
    }

    for n, b in bins.items():
        if b["bin"].exists():
            continue

        url = b["url"]
        name = Path(url).name

        SyS(f"wget -qO {name} {url}")
        SyS(f"tar -xzf {name} -C {USR}")
        SyS(f"rm -f {name}")


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
    configs = {
        'A1111': {
            'pre': [
                f'rm -rf {M / "Stable-diffusion/tmp_ckpt"} {M / "Lora/tmp_lora"} {M / "ControlNet"} {TMP}/*'
            ],
            'links': [
                (TMP / "ckpt", M / "Stable-diffusion/tmp_ckpt"),
                (TMP / "lora", M / "Lora/tmp_lora"),
                (TMP / "controlnet", M / "ControlNet")
            ]
        },

        'ReForge': {
            'pre': [
                f'rm -rf {M / "Stable-diffusion/tmp_ckpt"} {M / "Lora/tmp_lora"} {M / "ControlNet"}',
                f'rm -rf {M / "svd"} {M / "z123"} {TMP}/*'
            ],
            'links': [
                (TMP / "ckpt", M / "Stable-diffusion/tmp_ckpt"),
                (TMP / "lora", M / "Lora/tmp_lora"),
                (TMP / "controlnet", M / "ControlNet"),
                (TMP / "z123", M / "z123"),
                (TMP / "svd", M / "svd")
            ]
        },

        'Forge': {
            'pre': [
                f'rm -rf {M / "Stable-diffusion/tmp_ckpt"} {M / "Lora/tmp_lora"} {M / "ControlNet"}',
                f'rm -rf {M / "svd"} {M / "z123"} {M / "clip"} {M / "unet"} {TMP}/*'
            ],
            'links': [
                (TMP / "ckpt", M / "Stable-diffusion/tmp_ckpt"),
                (TMP / "lora", M / "Lora/tmp_lora"),
                (TMP / "controlnet", M / "ControlNet"),
                (TMP / "z123", M / "z123"),
                (TMP / "svd", M / "svd"),
                (TMP / "clip", M / "clip"),
                (TMP / "unet", M / "unet")
            ]
        },

        'ComfyUI': {
            'pre': [
                f'rm -rf {M / "checkpoints/tmp_ckpt"} {M / "loras/tmp_lora"} {M / "controlnet"}',
                f'rm -rf {M / "clip"} {M / "unet"} {TMP}/*'
            ],
            'links': [
                (TMP / "ckpt", M / "checkpoints/tmp_ckpt"),
                (TMP / "lora", M / "loras/tmp_lora"),
                (TMP / "controlnet", M / "controlnet"),
                (TMP / "clip", M / "clip"),
                (TMP / "unet", M / "unet"),
                (M / "checkpoints", M / "checkpoints_symlink")
            ]
        },

        'SwarmUI': {
            'pre': [
                f'rm -rf {M / "Stable-Diffusion/tmp_ckpt"} {M / "Lora/tmp_lora"} {M / "controlnet"}',
                f'rm -rf {M / "clip"} {M / "unet"} {TMP}/*'
            ],
            'links': [
                (TMP / "ckpt", M / "Stable-Diffusion/tmp_ckpt"),
                (TMP / "lora", M / "Lora/tmp_lora"),
                (TMP / "controlnet", M / "controlnet"),
                (TMP / "clip", M / "clip"),
                (TMP / "unet", M / "unet")
            ]
        }
    }

    cfg = configs.get(U)
    [SyS(f'{cmd}') for cmd in cfg['pre']]

    if U in ['A1111', 'Forge', 'ReForge']:
        [(M / d).mkdir(parents=True, exist_ok=True) for d in ["Lora", "ESRGAN"]]

    [SyS(f'ln -s {src} {tg}') for src, tg in cfg['links']]


def webui_req(U, W, M):
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

    sym_link(U, M)
    install_tunnel()

    scripts = [
        f"https://github.com/gutris1/segsmaker/raw/main/script/SM/controlnet.py {W}/asd",
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
        f"https://huggingface.co/pantat88/ui/resolve/main/4x_foolhardy_Remacri.pth {u}",
        f"https://huggingface.co/subby2006/NMKD-YandereNeoXL/resolve/main/4x_NMKD-YandereNeoXL_200k.pth {u}",
        f"https://huggingface.co/subby2006/NMKD-UltraYandere/resolve/main/4x_NMKD-UltraYandere_300k.pth {u}"
    ]

    line = scripts + upscalers
    for item in line: download(item)

    if U not in ['SwarmUI', 'ComfyUI']:
        SyS(f'rm -f {W}/html/card-no-preview.png')
        download(f'https://huggingface.co/pantat88/ui/resolve/main/card-no-preview.png {W}/html')


def webui_extension(U, W, M):
    EXT = W / "custom_nodes" if U == 'ComfyUI' else W / "extensions"
    CD(EXT)

    if U == 'ComfyUI':
        say("<br><b>【{red} Installing Custom Nodes{d} 】{red}</b>")
        clone(str(W / "asd/custom_nodes.txt"))
        print()

        for faces in [
            f"https://github.com/sczhou/CodeFormer/releases/download/v0.1.0/codeformer.pth {M}/facerestore_models",
            f"https://github.com/TencentARC/GFPGAN/releases/download/v1.3.4/GFPGANv1.4.pth {M}/facerestore_models"
        ]: download(faces)

    else:
        say("<br><b>【{red} Installing Extensions{d} 】{red}</b>")
        clone(str(W / "asd/extension.txt"))

        if ENVNAME == 'Kaggle':
            clone('https://github.com/gutris1/sd-civitai-browser-plus-plus')
        else:
            clone('https://github.com/BlafKing/sd-civitai-browser-plus')


def webui_installation(U, S, W, M, E, V):
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

    for item in extras: download(item)

    SyS(f"unzip -qo {embzip} -d {E} && rm {embzip}")

    if U != 'SwarmUI': webui_extension(U, W, M)


def webui_selection(ui, which_sd):
    repo_url = {
        'A1111': 'https://github.com/AUTOMATIC1111/stable-diffusion-webui A1111',
        'Forge': 'https://github.com/lllyasviel/stable-diffusion-webui-forge Forge',
        'ComfyUI': 'https://github.com/comfyanonymous/ComfyUI',
        'ReForge': 'https://github.com/Panchovix/stable-diffusion-webui-reForge ReForge',
        'SwarmUI': 'https://github.com/mcmonkeyprojects/SwarmUI'
    }

    if ui in repo_url:
        WEBUI = HOME / ui
        repo = repo_url[ui]

    MODELS = WEBUI / 'Models' if ui == 'SwarmUI' else WEBUI / 'models'
    EMB = MODELS / 'Embeddings' if ui == 'SwarmUI' else (MODELS / 'embeddings' if ui == 'ComfyUI' else WEBUI / 'embeddings')
    VAE = MODELS / 'vae' if ui == 'ComfyUI' else MODELS / 'VAE'

    say(f"<b>【{{red}} Installing {WEBUI.name}{{d}} 】{{red}}</b>")
    clone(repo)

    webui_installation(ui, which_sd, WEBUI, MODELS, EMB, VAE)

    say("<br><b>【{red} Done{d} 】{red}</b>")
    tempe()
    CD(HOME)


def webui_checker():
    config = json.load(MARKED.open('r')) if MARKED.exists() else {}
    ui = config.get('ui')
    WEBUI = HOME / ui if ui else None

    if WEBUI is not None and WEBUI.exists():
        git_dir = WEBUI / '.git'
        if git_dir.exists():
            CD(WEBUI)
            if ui in ['A1111', 'ComfyUI', 'SwarmUI']:
                SyS("git pull origin master")
            elif ui in ['Forge', 'ReForge']:
                SyS("git pull origin main")

    else:
        try:
            webui_selection(webui, sd)
        except KeyboardInterrupt:
            print("\nCanceled.")


def webui_misc():
    z = [
        (STR / '00-startup.py', f"wget -qO {STR}/00-startup.py https://github.com/gutris1/segsmaker/raw/main/script/KC/00-startup.py"),
        (pantat, f"wget -qO {pantat} https://github.com/gutris1/segsmaker/raw/main/script/SM/pantat88.py"),
        (nenen, f"wget -qO {nenen} https://github.com/gutris1/segsmaker/raw/main/script/SM/nenen88.py"),
        (STR / 'cupang.py', f"wget -qO {STR}/cupang.py https://github.com/gutris1/segsmaker/raw/main/script/SM/cupang.py"),
        (MRK, f"wget -qO {MRK} https://github.com/gutris1/segsmaker/raw/main/script/SM/marking.py")
    ]

    for x, y in z:
        if not Path(x).exists():
            SyS(y)


selection, civitai_key, hf_read_token = prevent_silly()
if selection is None or civitai_key is None:
    sys.exit()

webui, sd = selection

if not SRE.exists():
    PythonPortable()

clear_output()
display(Image(url=IMG))

CD(HOME)
webui_misc()
saving()
key_inject(civitai_key, hf_read_token)
marking(SRC, MARKED, webui)
sys.path.append(str(STR))

for scripts in [nenen, pantat, KANDANG, MRK]:
    get_ipython().run_line_magic('run', str(scripts))

from nenen88 import clone, say, download, tempe, pull # type: ignore
webui_checker()
