from IPython.display import display, Image, clear_output
from IPython import get_ipython
from pathlib import Path
import argparse, sys, json, os, subprocess, shlex, time


R = "\033[31m"
P = "\033[38;5;135m"
RST = "\033[0m"

IMG = "https://github.com/gutris1/segsmaker/raw/main/script/loading.png"
display(Image(url=IMG))
clear_output(wait=True)

VALID_WEBUI_OPTIONS = ["A1111", "Forge", "ComfyUI", "ReForge"]
VALID_SD_OPTIONS = ["1.5", "xl"]

def prevent_silly():
    full_args = ' '.join(sys.argv)

    if '--webui' in full_args:
        webui_value = full_args.split('--webui=')[1].split('--')[0].strip()
        if ',' in webui_value:
            print(f"{P}[{RST}{R}ERROR{RST}{P}]{RST} multiple values for --webui detected >> [{webui_value}] << provide only one valid option")
            print(f"\navailable webui options: [{', '.join(VALID_WEBUI_OPTIONS)}]")
            return None, None

    if '--sd' in full_args:
        sd_value = full_args.split('--sd=')[1].split('--')[0].strip()
        if ',' in sd_value:
            print(f"{P}[{RST}{R}ERROR{RST}{P}]{RST} multiple values for --sd detected >> [{sd_value}] << provide only one valid option")
            print(f"\navailable sd options: [{', '.join(VALID_SD_OPTIONS)}]")
            return None, None

    parser = argparse.ArgumentParser(description="WebUI Installer Script for kaggle and google colab")
    parser.add_argument('--webui', required=True, help="available webui: A1111, Forge, ComfyUI, ReForge")
    parser.add_argument('--sd', required=True, help="available sd: 1.5, xl")
    parser.add_argument('--civitai_key', required=True, help="your CivitAI API key")

    args = parser.parse_args()

    if args.webui not in VALID_WEBUI_OPTIONS:
        print(f"Invalid webui option: {args.webui}")
        print(f"Available webui options are: {', '.join(VALID_WEBUI_OPTIONS)}")
        return None, None

    if args.sd not in VALID_SD_OPTIONS:
        print(f"Invalid sd option: {args.sd}")
        print(f"Available sd options are: {', '.join(VALID_SD_OPTIONS)}")
        return None, None

    civitai_key = args.civitai_key.strip()
    if not civitai_key:
        print("Please enter your civitAI API key")
        return None, None

    if len(civitai_key) < 32:
        print("API key must be at least 32 characters long")
        return None, None

    return args, civitai_key


env, HOME = 'Unknown', None
env_list = {'Colab': '/content', 'Kaggle': '/kaggle/working'}

for env_name, path in env_list.items():
    if os.getenv(env_name.upper() + '_JUPYTER_TRANSPORT') or os.getenv(env_name.upper() + '_DATA_PROXY_TOKEN'):
        env, HOME = env_name, path
        break

if HOME is None:
    print("You are not in Kaggle or Google Colab.\nExiting.")
    sys.exit()

HOME = Path(HOME)
BASEPATH = Path('/content') if env == 'Colab' else Path('/kaggle')
tmp = BASEPATH / 'temp'
vnv = BASEPATH / 'venv'

SRC = HOME / 'gutris1'
MRK = SRC / 'marking.py'
KEY = SRC / 'api-key.json'
MARKED = SRC / 'marking.json'

STR = Path('/root/.ipython/profile_default/startup')
nenen = STR / "nenen88.py"
pantat = STR / "pantat88.py"
KANDANG = STR / 'KANDANG.py'

tmp.mkdir(parents=True, exist_ok=True)
SRC.mkdir(parents=True, exist_ok=True)

with open(KANDANG, 'w') as file:
    file.write(f"HOMEPATH = '{HOME}'\n")
    file.write(f"TEMPPATH = '{tmp}'\n")
    file.write(f"VENVPATH = '{vnv}'\n")
    file.write(f"BASEPATH = '{BASEPATH}'\n")

def marking(path, fn, ui):
    txt = path / fn
    values = {'ui': ui, 'launch_args1': '', 'launch_args2': '', 'tunnel': ''}

    if not txt.exists():
        with open(txt, 'w') as file:
            json.dump(values, file, indent=4)

    with open(txt, 'r') as file:
        data = json.load(file)

    data.update(values)
    with open(txt, 'w') as file:
        json.dump(data, file, indent=4)

def key_inject(api_key):
    target = [pantat, nenen]

    for line in target:
        with open(line, "r") as file:
            variable = file.read()

        value = variable.replace('toket = ""', f'toket = "{api_key}"')
        with open(line, "w") as file:
            file.write(value)

def sym_link(ui, WEBUI):
    if ui == 'A1111':
        return [
            f"rm -rf {tmp}/*",
            f"rm -rf {WEBUI}/models/Stable-diffusion/tmp_ckpt {WEBUI}/models/Lora/tmp_lora {WEBUI}/models/ControlNet",
            f"mkdir -p {WEBUI}/models/Lora {WEBUI}/models/ESRGAN",
            f"ln -vs {tmp}/ckpt {WEBUI}/models/Stable-diffusion/tmp_ckpt",
            f"ln -vs {tmp}/lora {WEBUI}/models/Lora/tmp_lora",
            f"ln -vs {tmp}/controlnet {WEBUI}/models/ControlNet"
        ]

    elif ui == 'ComfyUI':
        return [
            f"rm -rf {tmp}/*",
            f"rm -rf {WEBUI}/models/checkpoints/tmp_ckpt {WEBUI}/models/loras/tmp_lora",
            f"rm -rf {WEBUI}/models/controlnet {WEBUI}/models/clip",
            f"ln -vs {tmp}/ckpt {WEBUI}/models/checkpoints/tmp_ckpt",
            f"ln -vs {tmp}/lora {WEBUI}/models/loras/tmp_lora",
            f"ln -vs {tmp}/controlnet {WEBUI}/models/controlnet",
            f"ln -vs {tmp}/clip {WEBUI}/models/clip",
            f"ln -vs {WEBUI}/models/checkpoints {WEBUI}/models/checkpoints_symlink"
        ]

    elif ui in ['Forge', 'ReForge']:
        return [
            f"rm -rf {tmp}/*",
            f"rm -rf {WEBUI}/models/Stable-diffusion/tmp_ckpt {WEBUI}/models/Lora/tmp_lora",
            f"rm -rf {WEBUI}/models/ControlNet {WEBUI}/models/svd {WEBUI}/models/z123",
            f"mkdir -p {WEBUI}/models/Lora {WEBUI}/models/ESRGAN",
            f"ln -vs {tmp}/ckpt {WEBUI}/models/Stable-diffusion/tmp_ckpt",
            f"ln -vs {tmp}/lora {WEBUI}/models/Lora/tmp_lora",
            f"ln -vs {tmp}/controlnet {WEBUI}/models/ControlNet",
            f"ln -vs {tmp}/z123 {WEBUI}/models/z123",
            f"ln -vs {tmp}/svd {WEBUI}/models/svd"
        ]


def webui_req(ui, WEBUI):
    from nenen88 import pull, download

    if ui == 'A1111':
        pull(f"https://github.com/gutris1/segsmaker sd {WEBUI}")
    elif ui == 'Forge':
        pull(f"https://github.com/gutris1/segsmaker forge {WEBUI}")
    elif ui == 'ComfyUI':
        pull(f"https://github.com/gutris1/segsmaker cui {WEBUI}")
    elif ui == 'ReForge':
        pull(f"https://github.com/gutris1/segsmaker reforge {WEBUI}")

    os.chdir(WEBUI)
    req = sym_link(ui, WEBUI)

    for lines in req:
        subprocess.run(shlex.split(lines), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    scripts = [
        f"https://github.com/gutris1/segsmaker/raw/K/script/controlnet/controlnet.py {WEBUI}/asd",
        f"https://github.com/gutris1/segsmaker/raw/K/kaggle/script/venv.py {WEBUI}",
        f"https://github.com/gutris1/segsmaker/raw/K/script/multi/segsmaker.py {WEBUI}"
    ]

    upscalers_path = f"{WEBUI}/models/upscale_models" if ui == 'ComfyUI' else f"{WEBUI}/models/ESRGAN"
    upscalers = [
        f"https://huggingface.co/pantat88/ui/resolve/main/4x-UltraSharp.pth {upscalers_path}",
        f"https://huggingface.co/pantat88/ui/resolve/main/4x-AnimeSharp.pth {upscalers_path}",
        f"https://huggingface.co/pantat88/ui/resolve/main/4x_NMKD-Superscale-SP_178000_G.pth {upscalers_path}",
        f"https://huggingface.co/pantat88/ui/resolve/main/4x_RealisticRescaler_100000_G.pth {upscalers_path}",
        f"https://huggingface.co/pantat88/ui/resolve/main/8x_RealESRGAN.pth {upscalers_path}",
        f"https://huggingface.co/pantat88/ui/resolve/main/4x_foolhardy_Remacri.pth {upscalers_path}"
    ]

    line = scripts + upscalers
    for item in line:
        download(item)


def Extensions(ui, WEBUI):
    from nenen88 import clone, say

    if ui == 'ComfyUI':
        say("<br><b>【{red} Installing Custom Nodes{d} 】{red}</b>")
        os.chdir(WEBUI / "custom_nodes")
        clone(str(WEBUI / "asd/custom_nodes.txt"))
        print()

        custom_nodes_models = [
            f"https://github.com/sczhou/CodeFormer/releases/download/v0.1.0/codeformer.pth {WEBUI}/models/facerestore_models",
            f"https://github.com/TencentARC/GFPGAN/releases/download/v1.3.4/GFPGANv1.4.pth {WEBUI}/models/facerestore_models"
        ]

        for item in custom_nodes_models:
            download(item)

    else:
        say("<br><b>【{red} Installing Extensions{d} 】{red}</b>")
        os.chdir(WEBUI / "extensions")
        clone(str(WEBUI / "asd/ext-xl.txt"))
        get_ipython().system("git clone -q https://github.com/gutris1/sd-encrypt-image")


def installing_webui(ui, which_sd, WEBUI, EMB, VAE):
    from nenen88 import download
    webui_req(ui, WEBUI)

    if which_sd == "1.5":
        embzip = f"{WEBUI}/embeddings.zip"
        extras = [
            f"https://huggingface.co/pantat88/ui/resolve/main/embeddings.zip {WEBUI}",
            f"https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.safetensors {VAE}"
        ]

    elif which_sd == "xl":
        embzip = None
        extras = [
            f"https://civitai.com/api/download/models/403492 {EMB}",
            f"https://civitai.com/api/download/models/182974 {EMB}",
            f"https://civitai.com/api/download/models/159385 {EMB}",
            f"https://civitai.com/api/download/models/159184 {EMB}",
            f"https://huggingface.co/stabilityai/sdxl-vae/resolve/main/sdxl_vae.safetensors {VAE}"
        ]

    for item in extras:
        download(item)

    if which_sd == "1.5":
        get_ipython().system(f"unzip -qo {embzip} -d {EMB} && rm {embzip}")

    Extensions(ui, WEBUI)


def webui_install(ui, which_sd):
    from nenen88 import say, tempe

    if ui == 'A1111':
        WEBUI = HOME / 'A1111'
        repo = f'git clone -q -b {version} https://github.com/gutris1/A1111'
        say("<b>【{red} Installing A1111{d} 】{red}</b>")

    elif ui == 'Forge':
        WEBUI = HOME / 'Forge'
        repo = f'git clone -q https://github.com/lllyasviel/stable-diffusion-webui-forge Forge'
        say("<b>【{red} Installing Forge{d} 】{red}</b>")

    elif ui == 'ComfyUI':
        WEBUI = HOME / 'ComfyUI'
        repo = f'git clone -q https://github.com/comfyanonymous/ComfyUI'
        say("<b>【{red} Installing ComfyUI{d} 】{red}</b>")

    elif ui == 'ReForge':
        WEBUI = HOME / 'ReForge'
        repo = f'git clone -q https://github.com/Panchovix/stable-diffusion-webui-reForge ReForge'
        say("<b>【{red} Installing ReForge{d} 】{red}</b>")

    EMB = f"{WEBUI}/models/embeddings" if ui == 'ComfyUI' else f"{WEBUI}/embeddings"
    VAE = f"{WEBUI}/models/vae" if ui == 'ComfyUI' else f"{WEBUI}/models/VAE"

    req_list = [
        "curl -LO /kaggle/working/new_tunnel https://github.com/DEX-1101/sd-webui-notebook/raw/main/res/new_tunnel",
        "curl -Lo /usr/bin/cl https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64",
        "apt-get update",
        "apt -y install pv",
        "pip install -q gdown aria2 cloudpickle",
        "chmod +x /usr/bin/cl"
    ]

    for items in req_list:
        subprocess.run(shlex.split(items), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    get_ipython().system(f"{repo}")
    time.sleep(1)
    installing_webui(ui, which_sd, WEBUI, EMB, VAE)

    get_ipython().run_line_magic('run', f'{MRK}')
    get_ipython().run_line_magic('run', f'{WEBUI}/venv.py')

    say("<br><b>【{red} Done{d} 】{red}</b>")

    tempe()
    os.chdir(HOME)
    os._exit(00)


def lets_go():
    args, civitai_key = prevent_silly()
    if args is None or civitai_key is None:
        return

    z = [
        (STR / '00-startup.py', f"curl -sLo {STR}/00-startup.py https://github.com/gutris1/segsmaker/raw/K/kaggle/script/00-startup.py"),
        (pantat, f"curl -sLo {pantat} https://github.com/gutris1/segsmaker/raw/K/kaggle/script/pantat88.py"),
        (nenen, f"curl -sLo {nenen} https://github.com/gutris1/segsmaker/raw/K/kaggle/script/nenen88.py"),
        (STR / 'util.py', f"curl -sLo {STR}/util.py https://github.com/gutris1/segsmaker/raw/main/script/util.py"),
        (STR / 'cupang.py', f"curl -sLo {STR}/cupang.py https://github.com/gutris1/segsmaker/raw/K/kaggle/script/cupang.py"),
        (MRK, f"curl -sLo {MRK} https://github.com/gutris1/segsmaker/raw/K/kaggle/script/marking.py")
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
            commit_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip().decode('utf-8')

            if ui == 'A1111':
                if commit_hash != version:
                    get_ipython().system(f"git pull origin {version}")
                    get_ipython().system("git fetch --tags")

            elif ui == 'ComfyUI':
                get_ipython().system("git pull origin master")
                get_ipython().system("git fetch --tags")

            elif ui in ['Forge', 'ReForge']:
                get_ipython().system("git pull origin main")
                get_ipython().system("git fetch --tags")

    else:
        display(Image(url=IMG))
        sys.path.append(str(STR))
        get_ipython().run_line_magic('run', f'{nenen}')
        get_ipython().run_line_magic('run', f'{KANDANG}')

        marking(SRC, MARKED, args.webui)
        key_inject(civitai_key)

        try:
            webui_install(args.webui, args.sd)
        except KeyboardInterrupt:
            print("\nCanceled.")


version = 'v1.10.1'
os.chdir(HOME)
lets_go()
