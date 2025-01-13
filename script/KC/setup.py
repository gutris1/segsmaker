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
# If no known environment is found, default to local values
ENVNAME = "LOCAL"
ENVBASE = str(Path.cwd())
ENVHOME = str(Path.cwd())
print("No Kaggle/Colab environment detected. Using local defaults.")

HOME = Path(ENVHOME)
BASEPATH = Path(ENVBASE)
TMP = BASEPATH / 'temp'
VNV = BASEPATH / 'venv'

SRC = HOME / 'gutris1'
MRK = SRC / 'marking.py'
KEY = SRC / 'api-key.json'
MARKED = SRC / 'marking.json'

USR = Path('/usr/bin')
STR = Path.home() / '.ipython/profile_default/startup'
nenen = STR / 'nenen88.py'
pantat = STR / 'pantat88.py'
KANDANG = STR / 'KANDANG.py'

TMP.mkdir(parents=True, exist_ok=True)
SRC.mkdir(parents=True, exist_ok=True)

VALID_WEBUI_OPTIONS = ["A1111", "Forge", "ComfyUI", "ReForge", "SwarmUI"]
VALID_SD_OPTIONS = ["1.5", "xl"]

SyS = get_ipython().system
CD = os.chdir

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


def ngrok_zrok():
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
    CD(W)

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
        SyS("bash ./dotnet-install.sh --channel 8.0")

    req = sym_link(U, M)
    for lines in req:
        subprocess.run(shlex.split(lines), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    ngrok_zrok()

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
        f"https://huggingface.co/pantat88/ui/resolve/main/4x_foolhardy_Remacri.pth {u}",
        f"https://huggingface.co/subby2006/NMKD-YandereNeoXL/resolve/main/4x_NMKD-YandereNeoXL_200k.pth {u}",
        f"https://huggingface.co/subby2006/NMKD-UltraYandere/resolve/main/4x_NMKD-UltraYandere_300k.pth {u}"
    ]

    line = scripts + upscalers
    for item in line:
        download(item)

    if U not in ['SwarmUI', 'ComfyUI']:
        SyS(f'rm -f {W}/html/card-no-preview.png')
        download(f'https://huggingface.co/pantat88/ui/resolve/main/card-no-preview.png {W}/html')


def webui_extension(U, W, M):
    EXT = W / "custom_nodes" if U == 'ComfyUI' else W / "extensions"

    if U == 'ComfyUI':
        say("<br><b>【{red} Installing Custom Nodes{d} 】{red}</b>")
        CD(EXT)
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
        CD(EXT)
        clone(str(W / "asd/extension.txt"))

        if ENVNAME == 'Kaggle':
            if U in ['A1111', 'ReForge']:
                SyS(f'rm -rf {EXT}/sd-civitai-browser-plus')
                clone('https://github.com/gutris1/sd-civitai-browser-plus-plus')
            else:
                clone('https://github.com/gutris1/sd-encrypt-image')


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

    for item in extras:
        download(item)

    SyS(f"unzip -qo {embzip} -d {E} && rm {embzip}")

    if U != 'SwarmUI':
        webui_extension(U, W, M)


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

    if ENVNAME == "Colab":
        abcd = ["apt -y install python3.10-venv"]
    else:
        abcd = ["pip install ipywidgets jupyterlab_widgets --upgrade"]
        SyS('rm -f /usr/lib/python3.10/sitecustomize.py')

    abcd.extend([
        f'wget -qO {USR}/cl https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64',
        f'chmod +x {USR}/cl', 'pip install gdown aria2', 'apt -y install lz4 pv'
    ])

    for efgh in abcd:
        subprocess.run(shlex.split(efgh), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    webui_installation(ui, which_sd, WEBUI, MODELS, EMB, VAE)

    get_ipython().run_line_magic('run', str(WEBUI / 'venv.py'))
    SyS(f'{VNV}/bin/pip uninstall -qy ngrok pyngrok')

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
        display(Image(url=IMG))

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
    exit()

webui, sd = selection

CD(HOME)
webui_misc()
saving()
key_inject(civitai_key, hf_read_token)
marking(SRC, MARKED, webui)
sys.path.append(str(STR))

var = [nenen, pantat, KANDANG, MRK]
for scripts in var:
    get_ipython().run_line_magic('run', str(scripts))

from nenen88 import clone, say, download, tempe, pull
webui_checker()
