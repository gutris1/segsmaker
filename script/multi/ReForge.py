from IPython.display import display, HTML, clear_output, Image
from ipywidgets import widgets
from IPython import get_ipython
from pathlib import Path
import subprocess, time, os, shlex, json, shutil
from nenen88 import pull, say, download, clone, tempe

repo = f"git clone -q https://github.com/Panchovix/stable-diffusion-webui-reForge ReForge"

HOME = Path.home()
SRC = HOME / '.gutris1'
CSS = SRC / 'setup.css'
IMG = SRC / 'loading.png'
MARK = SRC / 'marking.py'
STP = HOME / '.conda/setup.py'

tmp = Path('/tmp')
vnv = tmp / 'venv'
WEBUI = HOME / 'ReForge'

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

def venv_install():
    url = 'https://huggingface.co/pantat88/back_up/resolve/main/venv_torch231.tar.lz4'
    fn = Path(url).name

    def check_venv(folder):
        du = get_ipython().getoutput(f'du -s -b {folder}')
        return int(du[0].split()[0]) if du else 0

    while True:
        if vnv.exists():
            size = check_venv(vnv)
            if size > 7 * 1024**3:
                return
            get_ipython().system(f'rm -rf {vnv}/* {vnv}')

        os.chdir(tmp)

        say("<br><b>【{red} Installing VENV{d} 】{red}</b>")
        download(url)

        get_ipython().system(f'pv {fn} | lz4 -d | tar xf -')
        Path(fn).unlink()

        get_ipython().system(f'rm -rf {vnv / "bin" / "pip*"}')
        get_ipython().system(f'rm -rf {vnv / "bin" / "python*"}')
        get_ipython().system(f'python3 -m venv {vnv}')
        get_ipython().system(f'{vnv / "bin" / "python3"} -m pip install -q --upgrade --force-reinstall pip')

def req_list():
    return [
        f"rm -rf {HOME}/tmp {HOME}/.cache/*",
        f"rm -rf {WEBUI}/models/Stable-diffusion/tmp_ckpt {WEBUI}/models/Lora/tmp_lora {WEBUI}/models/ControlNet",
        f"rm -rf {WEBUI}/models/svd {WEBUI}/models/z123",
        f"mkdir -p {WEBUI}/models/Lora",
        f"mkdir -p {WEBUI}/models/ESRGAN",
        f"ln -vs /tmp {HOME}/tmp",
        f"ln -vs /tmp/ckpt {WEBUI}/models/Stable-diffusion/tmp_ckpt",
        f"ln -vs /tmp/lora {WEBUI}/models/Lora/tmp_lora",
        f"ln -vs /tmp/controlnet {WEBUI}/models/ControlNet",
        f"ln -vs /tmp/z123 {WEBUI}/models/z123",
        f"ln -vs /tmp/svd {WEBUI}/models/svd"]

def webui_req():
    time.sleep(1)
    pull(f"https://github.com/gutris1/segsmaker reforge {WEBUI}")

    tmp_cleaning()

    os.chdir(WEBUI)
    req = req_list()

    for lines in req:
        subprocess.run(shlex.split(lines), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    scripts = [
        f"https://github.com/gutris1/segsmaker/raw/main/script/controlnet/controlnet.py {WEBUI}/asd",
        f"https://github.com/gutris1/segsmaker/raw/main/script/zrok.py {WEBUI}",
        f"https://github.com/gutris1/segsmaker/raw/main/script/pinggy.py {WEBUI}",
        f"https://github.com/gutris1/segsmaker/raw/main/script/ngrokk.py {WEBUI}",
        f"https://github.com/gutris1/segsmaker/raw/main/script/venv.py {WEBUI}",
        f"https://github.com/gutris1/segsmaker/raw/main/script/multi/segsmaker.py {WEBUI}"]

    upscalers = [
        f"https://huggingface.co/pantat88/ui/resolve/main/4x-UltraSharp.pth {WEBUI}/models/ESRGAN",
        f"https://huggingface.co/pantat88/ui/resolve/main/4x-AnimeSharp.pth {WEBUI}/models/ESRGAN",
        f"https://huggingface.co/pantat88/ui/resolve/main/4x_NMKD-Superscale-SP_178000_G.pth {WEBUI}/models/ESRGAN",
        f"https://huggingface.co/pantat88/ui/resolve/main/4x_RealisticRescaler_100000_G.pth {WEBUI}/models/ESRGAN",
        f"https://huggingface.co/pantat88/ui/resolve/main/8x_RealESRGAN.pth {WEBUI}/models/ESRGAN",
        f"https://huggingface.co/pantat88/ui/resolve/main/4x_foolhardy_Remacri.pth {WEBUI}/models/ESRGAN"]

    line = scripts + upscalers
    for item in line:
        download(item)

    tempe()

def sd_15():
    webui_req()

    extras = [
        f"https://huggingface.co/pantat88/ui/resolve/main/embeddings.zip {WEBUI}",
        f"https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.safetensors {WEBUI}/models/VAE"]

    for items in extras:
        download(items)

    get_ipython().system(f"unzip -qo {WEBUI}/embeddings.zip -d {WEBUI}/embeddings && rm {WEBUI}/embeddings.zip")

    say("<br><b>【{red} Installing Extensions{d} 】{red}</b>")
    os.chdir(WEBUI / "extensions")
    clone(str(WEBUI / "asd/ext-15.txt"))

def sd_xl():
    webui_req()

    extras = [
        f"https://civitai.com/api/download/models/182974 {WEBUI}/embeddings",
        f"https://civitai.com/api/download/models/159385 {WEBUI}/embeddings",
        f"https://civitai.com/api/download/models/159184 {WEBUI}/embeddings",
        f"https://civitai.com/api/download/models/264491 {WEBUI}/models/VAE XL_VAE_F1.safetensors"]

    for items in extras:
        download(items)

    say("<br><b>【{red} Installing Extensions{d} 】{red}</b>")
    os.chdir(WEBUI / "extensions")
    clone(str(WEBUI / "asd/ext-xl.txt"))

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
        say("<b>【{red} Installing ReForge{d} 】{red}</b>")
        get_ipython().system(f"{repo}")

        marking(SRC, 'marking.json', 'ReForge')

        if b == 'button-15':
            sd_15()
        elif b == 'button-xl':
            sd_xl()

        get_ipython().run_line_magic('run', f'{MARK}')

        venv_install()
        os.chdir(HOME)

        with loading:
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
        height='300px'))

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

            get_ipython().system("git pull origin main")
            get_ipython().system("git fetch --tags")

        x = [
            f"https://github.com/gutris1/segsmaker/raw/main/script/controlnet/controlnet.py {WEBUI}/asd",
            f"https://github.com/gutris1/segsmaker/raw/main/script/zrok.py {WEBUI}",
            f"https://github.com/gutris1/segsmaker/raw/main/script/pinggy.py {WEBUI}",
            f"https://github.com/gutris1/segsmaker/raw/main/script/ngrokk.py {WEBUI}",
            f"https://github.com/gutris1/segsmaker/raw/main/script/venv.py {WEBUI}",
            f"https://github.com/gutris1/segsmaker/raw/main/script/multi/segsmaker.py {WEBUI}"
        ]

        for y in x:
            download(y)

    else:
        webui_list = [
            ('A1111', HOME / 'A1111'),
            ('Forge', HOME / 'Forge'),
            ('ComfyUI', HOME / 'ComfyUI'),
            ('FaceFusion', HOME / 'FaceFusion')
        ]
        
        for ui_name, path in webui_list:
            if check_webui(ui_name, path, MARK):
                return

        load_css()
        display(panel, webui_setup, loading)

webui_widgets()
