from IPython.display import display, HTML, clear_output, Image
from ipywidgets import widgets
from IPython import get_ipython
from pathlib import Path
import subprocess, time, os, shlex, json, shutil
from nenen88 import pull, say, download, clone, tempe

repo = f"git clone -q https://github.com/comfyanonymous/ComfyUI"

HOME = Path.home()
SRC = HOME / '.gutris1'
CSS = SRC / 'setup.css'
IMG = SRC / 'loading.png'
MARK = SRC / 'marking.py'
STP = HOME / '.conda/setup.py'

tmp = Path('/tmp')
vnv = tmp / 'venv'
WEBUI = HOME / "ComfyUI"

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
        f"rm -rf {WEBUI}/models/checkpoints/tmp_ckpt",
        f"rm -rf {WEBUI}/models/loras/tmp_lora {WEBUI}/models/controlnet {WEBUI}/models/clip",
        f"ln -vs /tmp {HOME}/tmp",
        f"ln -vs /tmp/ckpt {WEBUI}/models/checkpoints/tmp_ckpt",
        f"ln -vs /tmp/lora {WEBUI}/models/loras/tmp_lora",
        f"ln -vs /tmp/controlnet {WEBUI}/models/controlnet",
        f"ln -vs /tmp/clip {WEBUI}/models/clip",
        f"ln -vs {WEBUI}/models/checkpoints {WEBUI}/models/checkpoints_symlink"]

def webui_req():
    time.sleep(1)
    pull(f"https://github.com/gutris1/segsmaker comfyui {WEBUI}")

    tmp_cleaning()

    os.chdir(WEBUI)
    req = req_list()

    for lines in req:
        subprocess.run(shlex.split(lines), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    scripts = [
        f"https://github.com/gutris1/segsmaker/raw/main/script/SM/controlnet.py {WEBUI}/asd",
        f"https://github.com/gutris1/segsmaker/raw/main/script/SM/venv.py {WEBUI}",
        f"https://github.com/gutris1/segsmaker/raw/main/script/SM/Launcher.py {WEBUI}",
        f"https://github.com/gutris1/segsmaker/raw/main/script/SM/segsmaker.py {WEBUI}"]

    upscalers = [
        f"https://huggingface.co/pantat88/ui/resolve/main/4x-UltraSharp.pth {WEBUI}/models/upscale_models",
        f"https://huggingface.co/pantat88/ui/resolve/main/4x-AnimeSharp.pth {WEBUI}/models/upscale_models",
        f"https://huggingface.co/pantat88/ui/resolve/main/4x_NMKD-Superscale-SP_178000_G.pth {WEBUI}/models/upscale_models",
        f"https://huggingface.co/pantat88/ui/resolve/main/4x_RealisticRescaler_100000_G.pth {WEBUI}/models/upscale_models",
        f"https://huggingface.co/pantat88/ui/resolve/main/8x_RealESRGAN.pth {WEBUI}/models/upscale_models",
        f"https://huggingface.co/pantat88/ui/resolve/main/4x_foolhardy_Remacri.pth {WEBUI}/models/upscale_models"]

    line = scripts + upscalers
    for item in line:
        download(item)

    tempe()

def install_custom_nodes():
    say("<br><b>【{red} Installing Custom Nodes{d} 】{red}</b>")

    os.chdir(WEBUI / "custom_nodes")
    clone(str(WEBUI / "asd/custom_nodes.txt"))
    print()

    custom_nodes_models = [
        f"https://github.com/sczhou/CodeFormer/releases/download/v0.1.0/codeformer.pth {WEBUI}/models/facerestore_models",
        f"https://github.com/TencentARC/GFPGAN/releases/download/v1.3.4/GFPGANv1.4.pth {WEBUI}/models/facerestore_models"]

    for item in custom_nodes_models:
        download(item)

def sd_15():
    webui_req()

    extras = [
        f"https://huggingface.co/pantat88/ui/resolve/main/embeddings.zip {WEBUI}/models",
        f"https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.safetensors {WEBUI}/models/vae"]

    for items in extras:
        download(items)

    get_ipython().system(f"unzip -qo {WEBUI}/models/embeddings.zip -d {WEBUI}/models/embeddings")
    get_ipython().system(f"rm {WEBUI}/models/embeddings.zip")

    install_custom_nodes()

def sd_xl():
    webui_req()

    extras = [
        f"https://civitai.com/api/download/models/403492 {WEBUI}/models/embeddings",
        f"https://civitai.com/api/download/models/182974 {WEBUI}/models/embeddings",
        f"https://civitai.com/api/download/models/159385 {WEBUI}/models/embeddings",
        f"https://civitai.com/api/download/models/159184 {WEBUI}/models/embeddings",
        f"https://huggingface.co/stabilityai/sdxl-vae/resolve/main/sdxl_vae.safetensors {WEBUI}/models/vae"
    ]

    for items in extras:
        download(items)

    install_custom_nodes()

def marking(path, fn, ui):
    txt = path / fn
    values = {
        'ui': ui,
        'launch_args1': '',
        'launch_args2': '',
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
        'launch_args1': '',
        'launch_args2': '',
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
        say("<b>【{red} Installing ComfyUI{d} 】{red}</b>")
        get_ipython().system(f"{repo}")

        marking(SRC, 'marking.json', 'ComfyUI')

        if b == 'button-15':
            sd_15()
        elif b == 'button-xl':
            sd_xl()

        get_ipython().run_line_magic('run', f'{MARK}')

        with loading:
            loading.clear_output(wait=True)
            get_ipython().run_line_magic('run', f'{WEBUI}/venv.py')
            os.chdir(HOME)
            loading.clear_output(wait=True)
            say("<b>【{red} Done{d} 】{red}</b>")

def go_back(b):
    panel.close()
    clear_output()

    with webui_setup:
        get_ipython().run_line_magic('run', f'{STP}')

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
            commit_hash = os.popen('git rev-parse HEAD').read().strip()

            get_ipython().system("git pull origin master")
            get_ipython().system("git fetch --tags")

        x = [
            f"https://github.com/gutris1/segsmaker/raw/main/script/SM/controlnet.py {WEBUI}/asd",
            f"https://github.com/gutris1/segsmaker/raw/main/script/SM/venv.py {WEBUI}",
            f"https://github.com/gutris1/segsmaker/raw/main/config/comfyui/apotek.py {WEBUI}",
            f"https://github.com/gutris1/segsmaker/raw/main/script/SM/Launcher.py {WEBUI}",
            f"https://github.com/gutris1/segsmaker/raw/main/script/SM/segsmaker.py {WEBUI}"
        ]

        for y in x:
            download(y)

    else:
        webui_list = [
            ('A1111', HOME / 'A1111'),
            ('Forge', HOME / 'Forge'),
            ('ReForge', HOME / 'ReForge'),
            ('FaceFusion', HOME / 'FaceFusion'),
            ('SDTrainer', HOME / 'SDTrainer'),
            ('KohyaSS', HOME / 'KohyaSS')
        ]
        
        for ui_name, path in webui_list:
            if check_webui(ui_name, path, MARK):
                return

        load_css()
        display(panel, webui_setup, loading)

webui_widgets()
