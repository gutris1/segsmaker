from IPython.display import display, HTML, clear_output, Image
from ipywidgets import widgets
from IPython import get_ipython
from pathlib import Path
import subprocess, time, os, shlex, json, shutil
from nenen88 import pull, say, download, clone, tempe

version = "v1.10.1"
repo = f"git clone -q -b {version} https://github.com/gutris1/A1111"

HOME = Path.home()
SRC = HOME / '.gutris1'
CSS = SRC / 'setup.css'
IMG = SRC / 'loading.png'
MARK = SRC / 'marking.py'
STP = HOME / '.conda/setup.py'

tmp = Path('/tmp')
vnv = tmp / 'venv'
WEBUI = HOME / 'A1111'
MODELS = WEBUI / 'models'

os.chdir(HOME)

def load_css():
    with open(CSS, "r") as file:
        data = file.read()
    display(HTML(f"<style>{data}</style>"))

def tmp_cleaning():
    for item in tmp.iterdir():
        if item.is_dir() and item != vnv:
            shutil.rmtree(item)
        elif item.is_file() and item != vnv:
            item.unlink()

def req_list():
    return [
        f"rm -rf {HOME}/tmp {HOME}/.cache/*",
        f"rm -rf {MODELS}/Stable-diffusion/tmp_ckpt {MODELS}/Lora/tmp_lora {MODELS}/ControlNet",
        f"mkdir -p {MODELS}/Lora {MODELS}/ESRGAN",
        f"ln -vs /tmp {HOME}/tmp",
        f"ln -vs /tmp/ckpt {MODELS}/Stable-diffusion/tmp_ckpt",
        f"ln -vs /tmp/lora {MODELS}/Lora/tmp_lora",
        f"ln -vs /tmp/controlnet {MODELS}/ControlNet"
    ]

def webui_req():
    time.sleep(1)
    pull(f"https://github.com/gutris1/segsmaker a1111 {WEBUI}")

    tmp_cleaning()

    os.chdir(WEBUI)
    req = req_list()
    for lines in req:
        subprocess.run(shlex.split(lines), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    scripts = [
        f"https://github.com/gutris1/segsmaker/raw/main/script/SM/controlnet.py {WEBUI}/asd",
        f"https://github.com/gutris1/segsmaker/raw/main/script/SM/venv.py {WEBUI}",
        f"https://github.com/gutris1/segsmaker/raw/main/script/SM/Launcher.py {WEBUI}",
        f"https://github.com/gutris1/segsmaker/raw/main/script/SM/segsmaker.py {WEBUI}"
    ]

    upscalers = [
        f"https://huggingface.co/pantat88/ui/resolve/main/4x-UltraSharp.pth {MODELS}/ESRGAN",
        f"https://huggingface.co/pantat88/ui/resolve/main/4x-AnimeSharp.pth {MODELS}/ESRGAN",
        f"https://huggingface.co/pantat88/ui/resolve/main/4x_NMKD-Superscale-SP_178000_G.pth {MODELS}/ESRGAN",
        f"https://huggingface.co/pantat88/ui/resolve/main/4x_RealisticRescaler_100000_G.pth {MODELS}/ESRGAN",
        f"https://huggingface.co/pantat88/ui/resolve/main/8x_RealESRGAN.pth {MODELS}/ESRGAN",
        f"https://huggingface.co/pantat88/ui/resolve/main/4x_foolhardy_Remacri.pth {MODELS}/ESRGAN"
    ]

    line = scripts + upscalers
    for item in line:
        download(item)

    tempe()

def Extensions():
    say("<br><b>【{red} Installing Extensions{d} 】{red}</b>")
    os.chdir(WEBUI / "extensions")
    clone(str(WEBUI / "asd/extension.txt"))

def sd_15():
    webui_req()

    extras = [
        f"https://huggingface.co/pantat88/ui/resolve/main/embeddings.zip {WEBUI}",
        f"https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.safetensors {MODELS}/VAE"]

    for items in extras:
        download(items)

    get_ipython().system(f"unzip -qo {WEBUI}/embeddings.zip -d {WEBUI}/embeddings && rm {WEBUI}/embeddings.zip")
    Extensions()

def sd_xl():
    webui_req()

    extras = [
        f"https://civitai.com/api/download/models/403492 {WEBUI}/embeddings",
        f"https://civitai.com/api/download/models/182974 {WEBUI}/embeddings",
        f"https://civitai.com/api/download/models/159385 {WEBUI}/embeddings",
        f"https://civitai.com/api/download/models/159184 {WEBUI}/embeddings",
        f"https://huggingface.co/stabilityai/sdxl-vae/resolve/main/sdxl_vae.safetensors {MODELS}/VAE"
    ]

    for items in extras:
        download(items)
    Extensions()

def marking(path, fn, ui):
    txt = path / fn
    values = {
        'ui': ui,
        'launch_args': '',
        'zrok_token': '',
        'ngrok_token': '',
        'tunnel': ''
    }

    if not txt.exists():
        with open(txt, 'w') as file:
            json.dump(values, file, indent=4)

    with open(txt, 'r') as file:
        data = json.load(file)

    data.update({
        'ui': ui,
        'launch_args': '',
        'tunnel': ''
    })

    with open(txt, 'w') as file:
        json.dump(data, file, indent=4)

def webui_install(b):
    panel.close()
    clear_output()

    with loading:
        display(Image(filename=str(IMG)))

    with webui_setup:
        say("<b>【{red} Installing Stable Diffusion{d} 】{red}</b>")
        get_ipython().system(repo)

        marking(SRC, 'marking.json', WEBUI.name)

        if b == 'button-15':
            sd_15()
        elif b == 'button-xl':
            sd_xl()

        get_ipython().run_line_magic('run', str(MARK))

        with loading:
            loading.clear_output(wait=True)
            get_ipython().run_line_magic('run', str(WEBUI / 'venv.py'))

            os.chdir(HOME)
            loading.clear_output(wait=True)
            say("<b>【{red} Done{d} 】{red}</b>")

def go_back(b):
    panel.close()
    clear_output()

    with webui_setup:
        get_ipython().run_line_magic('run', str(STP))

loading = widgets.Output()
webui_setup = widgets.Output()

options = ['button-15', 'button-back', 'button-xl']
buttons = []

for btn in options:
    button = widgets.Button(description='')
    button.add_class(btn.lower())
    if btn == 'button-back':
        button.on_click(lambda x: go_back(btn))
    else:
        button.on_click(lambda x, btn=btn: webui_install(btn))
    buttons.append(button)

panel = widgets.HBox(
    buttons, layout=widgets.Layout(
        width='450px',
        height='250px'))

panel.add_class("multi-panel")

def check_webui(ui_name, path, mark):
    if path.exists():
        print(f'{ui_name} is installed, Uninstall first.')
        get_ipython().run_line_magic('run', f'{mark}')
        return True
    return False

def webui_widgets():
    if WEBUI.exists():
        git_dir = WEBUI / '.git'
        if git_dir.exists():
            os.chdir(WEBUI)
            commit_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip().decode('utf-8')

            if commit_hash != version:
                get_ipython().system(f"git pull origin {version}")
                get_ipython().system("git fetch --tags")

        x = [
            f"https://github.com/gutris1/segsmaker/raw/main/script/SM/controlnet.py {WEBUI}/asd",
            f"https://github.com/gutris1/segsmaker/raw/main/script/SM/Launcher.py {WEBUI}",
            f"https://github.com/gutris1/segsmaker/raw/main/script/SM/venv.py {WEBUI}",
            f"https://github.com/gutris1/segsmaker/raw/main/script/SM/segsmaker.py {WEBUI}"
        ]

        for y in x:
            download(y)

    else:
        webui_list = [
            ('Forge', HOME / 'Forge'),
            ('ComfyUI', HOME / 'ComfyUI'),
            ('ReForge', HOME / 'ReForge'),
            ('FaceFusion', HOME / 'FaceFusion'),
            ('SDTrainer', HOME / 'SDTrainer'),
            ('SwarmUI', HOME / 'SwarmUI')
        ]
        
        for ui_name, path in webui_list:
            if check_webui(ui_name, path, MARK):
                return

        load_css()
        display(panel, webui_setup, loading)

webui_widgets()
