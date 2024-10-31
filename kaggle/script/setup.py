from IPython.display import display, HTML, clear_output, Image
from IPython import get_ipython
from ipywidgets import widgets
from pathlib import Path
import subprocess, os, sys, shlex, json, time

print('Loading Widget...')
clear_output(wait=True)

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

tmp.mkdir(parents=True, exist_ok=True)

SRC = HOME / 'gutris1'
CSS = SRC / 'setup.css'
MRK = SRC / 'marking.py'
IMG = SRC / 'loading.png'
KEY = SRC / 'api-key.json'
MARKED = SRC / 'marking.json'

STR = Path('/root/.ipython/profile_default/startup')
nenen = STR / "nenen88.py"
pantat = STR / "pantat88.py"
KANDANG = STR / 'KANDANG.py'

with open(KANDANG, 'w') as file:
    file.write(f"HOMEPATH = '{HOME}'\n")
    file.write(f"TEMPPATH = '{tmp}'\n")
    file.write(f"VENVPATH = '{vnv}'\n")
    file.write(f"BASEPATH = '{BASEPATH}'\n")

current_key = ""
if KEY.exists():
    with open(KEY, "r") as file:
        value = json.load(file)
        current_key = value.get("civitai-api-key", "")

SRC.mkdir(parents=True, exist_ok=True)
                
def load_css():
    with open(CSS, "r") as file:
        data = file.read()

    display(HTML(f"<style>{data}</style>"))

def marking(path, fn, ui):
    txt = path / fn
    values = {
        'ui': ui,
        'launch_args1': '',
        'launch_args2': '',
        'tunnel': ''
    }

    if not txt.exists():
        with open(txt, 'w') as file:
            json.dump(values, file, indent=4)

    with open(txt, 'r') as file:
        data = json.load(file)

    data.update({
        'ui': ui,
        'launch_args1': '',
        'launch_args2': '',
        'tunnel': ''
    })

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

    tempe()

def Extensions(ui, WEBUI):
    if ui == 'ComfyUI':
        say("<br><b>【{red} Installing Custom Nodes{d} 】{red}</b>")
        os.chdir(WEBUI / "custom_nodes")
        clone(str(WEBUI / "asd/custom_nodes.txt"))
        print()

        custom_nodes_models = [
            f"https://github.com/sczhou/CodeFormer/releases/download/v0.1.0/codeformer.pth {WEBUI}/models/facerestore_models",
            f"https://github.com/TencentARC/GFPGAN/releases/download/v1.3.4/GFPGANv1.4.pth {WEBUI}/models/facerestore_models"]

        for item in custom_nodes_models:
            download(item)

    else:
        say("<br><b>【{red} Installing Extensions{d} 】{red}</b>")
        os.chdir(WEBUI / "extensions")
        clone(str(WEBUI / "asd/ext-xl.txt"))
        get_ipython().system("git clone -q https://github.com/gutris1/sd-encrypt-image")
        
def installing_webui(ui, which_sd, WEBUI, EMB, VAE):
    webui_req(ui, WEBUI)

    if which_sd == "sd 1.5":
        extras = [
            f"https://huggingface.co/pantat88/ui/resolve/main/embeddings.zip {WEBUI}",
            f"https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.safetensors {VAE}"
        ]
        embzip = f"{WEBUI}/embeddings.zip"

    elif which_sd == "sd xl":
        extras = [
            f"https://civitai.com/api/download/models/403492 {EMB}",
            f"https://civitai.com/api/download/models/182974 {EMB}",
            f"https://civitai.com/api/download/models/159385 {EMB}",
            f"https://civitai.com/api/download/models/159184 {EMB}",
            f"https://huggingface.co/stabilityai/sdxl-vae/resolve/main/sdxl_vae.safetensors {VAE}"
        ]
        embzip = None

    for item in extras:
        download(item)

    if which_sd == "sd 1.5":
        get_ipython().system(f"unzip -qo {embzip} -d {EMB} && rm {embzip}")

    Extensions(ui, WEBUI)

def webui_install(ui, which_sd):
    from nenen88 import pull, say, download, clone, tempe

    with loading:
        display(Image(filename=str(IMG)))

    with output:
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

        with loading:
            loading.clear_output(wait=True)
            get_ipython().run_line_magic('run', f'{WEBUI}/venv.py')
            loading.clear_output(wait=True)
            say("<b>【{red} Done{d} 】{red}</b>")
            get_ipython().kernel.do_shutdown(True)
            os.chdir(HOME)

def handle_launch(b):
    try:
        def webui_selection():
            with aiueo:
                PLAY('-u https://huggingface.co/pantat88/ui/resolve/main/2.wav')
            multi_panel.close()
            webui_selection = {
                'A1111': 'A1111',
                'Forge': 'Forge',
                'ComfyUI': 'ComfyUI',
                'ReForge': 'ReForge'
            }
            ui = webuiradio1.value
            which_sd = webuiradio2.value
            marking(SRC, MARKED, ui)
            webui_install(ui, which_sd)

        def key_input(b):
            api_key = civitai_key_box.value.strip()

            with output:
                if not api_key:
                    PLAY('-u https://huggingface.co/pantat88/ui/resolve/main/3.wav')
                    print("Please enter your CivitAI API KEY / CivitAI APIキーのおっぱいを入力してください。")
                    return

                if len(api_key) < 32:
                    PLAY('-u https://huggingface.co/pantat88/ui/resolve/main/3.wav')
                    print("API key must be at least 32 characters long / APIキーは少なくとも32オッパイの長さに達する必要があります。")
                    return

                key_value = {"civitai-api-key": api_key}
                with open(KEY, "w") as file:
                    json.dump(key_value, file, indent=4)

            key_inject(api_key)
            output.clear_output()
            sys.path.append(str(STR))
            get_ipython().run_line_magic('run', f'{nenen}')
            get_ipython().run_line_magic('run', f'{KANDANG}')
            webui_selection()

        key_input(b)

    except KeyboardInterrupt:
        print('Canceled')

aiueo = widgets.Output()
output = widgets.Output()
loading = widgets.Output()

civitai_key_box = widgets.Text(
    value=current_key,
    placeholder='Enter Your Civitai API KEY Here',
    layout=widgets.Layout(left='26px', padding='10px', width='300px')
)

WEBUI_LIST = ['A1111', 'Forge', 'ComfyUI', 'ReForge']
list1 = {btn: btn for btn in WEBUI_LIST}

SD_LIST = ['SD 1.5', 'SD XL']
list2 = {btn: btn.lower() for btn in SD_LIST}

webuiradio1 = widgets.RadioButtons(options=list1)
webuiradio2 = widgets.RadioButtons(options=list2, layout=widgets.Layout(left='25px'))

radio_list = widgets.HBox(
    [webuiradio1, webuiradio2],
    layout=widgets.Layout(padding='10px', width='360px', height='360px')
)

install_button = widgets.Button(description='Install')
exit_button = widgets.Button(description='Exit')
button_box = widgets.HBox(
    [exit_button, install_button],
    layout=widgets.Layout(padding='10px', display='flex',flex_flow='row', justify_content='space-between')
)

multi_panel = widgets.VBox(
    [civitai_key_box, radio_list, button_box],
    layout=widgets.Layout(width='360px', height='360px')
)

civitai_key_box.add_class("api-input")
webuiradio1.add_class("webui-radio")
webuiradio2.add_class("webui-radio")
multi_panel.add_class('launch-panel')
install_button.add_class('buttons')
exit_button.add_class('buttons')

MGC = 'https://github.com/neighthan/jupyter-magics/raw/master/jupyter_magics/bell_magic.py'
BELL = STR / 'bell_magic.py'
z = [(BELL, f"curl -sLo {BELL} {MGC}")]
for x, y in z:
    if not Path(x).exists():
        get_ipython().system(y)

get_ipython().run_line_magic('run', f'{BELL}')
sys.path.append(str(STR))
from bell_magic import NotificationMagics
PLAY = NotificationMagics(get_ipython()).notify

def radio1webui(b):
    if b['name'] == 'value' and b['new']:
        with aiueo:
            PLAY('-u https://huggingface.co/pantat88/ui/resolve/main/1.wav')

def radio2webui(b):
    if b['name'] == 'value' and b['new']:
        with aiueo:
            PLAY('-u https://huggingface.co/pantat88/ui/resolve/main/3.wav')

def exiting(b):
    multi_panel.close()
    with aiueo:
        PLAY('-u https://huggingface.co/pantat88/ui/resolve/main/2.wav')
        output.clear_output()

webuiradio1.observe(radio1webui, names='value')
webuiradio2.observe(radio2webui, names='value')

install_button.on_click(handle_launch)
exit_button.on_click(exiting)

def multi_widgets():
    config = json.load(MARKED.open('r')) if MARKED.exists() else {}
    ui = config.get('ui')
    WEBUI = HOME / ui if ui else None

    if ui:
        if WEBUI and WEBUI.exists():
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
        z = [
            (STR / '00-startup.py', f"curl -sLo {STR}/00-startup.py https://github.com/gutris1/segsmaker/raw/K/kaggle/script/00-startup.py"),
            (pantat, f"curl -sLo {pantat} https://github.com/gutris1/segsmaker/raw/K/kaggle/script/pantat88.py"),
            (nenen, f"curl -sLo {nenen} https://github.com/gutris1/segsmaker/raw/K/kaggle/script/nenen88.py"),
            (STR / 'util.py', f"curl -sLo {STR}/util.py https://github.com/gutris1/segsmaker/raw/main/script/util.py"),
            (STR / 'cupang.py', f"curl -sLo {STR}/cupang.py https://github.com/gutris1/segsmaker/raw/main/script/cupang.py"),
            (CSS, f"curl -sLo {CSS} https://github.com/gutris1/segsmaker/raw/K/kaggle/script/setup.css"),
            (IMG, f"curl -sLo {IMG} https://github.com/gutris1/segsmaker/raw/main/script/loading.png"),
            (MRK, f"curl -sLo {MRK} https://github.com/gutris1/segsmaker/raw/K/kaggle/script/marking.py")
        ]

        for x, y in z:
            if not Path(x).exists():
                get_ipython().system(y)
        
        clear_output()
        load_css()
        display(multi_panel, aiueo, output, loading)

version = 'v1.10.1'

os.chdir(HOME)
multi_widgets()
