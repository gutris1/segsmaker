from IPython.display import display, HTML, clear_output, Image
from ipywidgets import widgets
from IPython import get_ipython
from pathlib import Path
import subprocess, time, os, shlex, json, shutil
from nenen88 import pull, say, download, clone, tempe

version = "v1.10.1"
repo = f"git clone -q -b {version} https://github.com/gutris1/asd"

home = Path.home()
src = home / '.gutris1'
css_setup = src / 'setup.css'
img = src / 'loading.png'
mark = src / 'marking.py'
setup = home / '.conda/setup.py'

tmp = Path('/tmp')
vnv = tmp / 'venv'

sd = home / 'asd'

os.chdir(home)

def load_css():
    with open(css_setup, "r") as file:
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
            get_ipython().system(f'rm -rf {vnv}')

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
        f"rm -rf {home}/tmp {home}/.cache/*",
        f"rm -rf {sd}/models/Stable-diffusion/tmp_ckpt {sd}/models/Lora/tmp_lora {sd}/models/ControlNet",
        f"mkdir -p {sd}/models/Lora",
        f"mkdir -p {sd}/models/ESRGAN",
        f"ln -vs /tmp {home}/tmp",
        f"ln -vs /tmp/ckpt {sd}/models/Stable-diffusion/tmp_ckpt",
        f"ln -vs /tmp/lora {sd}/models/Lora/tmp_lora",
        f"ln -vs /tmp/controlnet {sd}/models/ControlNet"]

def sd_clone():
    time.sleep(1)
    pull(f"https://github.com/gutris1/segsmaker sd {sd}")

    tmp_cleaning()

    os.chdir(sd)
    req = req_list()

    for lines in req:
        subprocess.run(shlex.split(lines), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    scripts = [
        f"https://github.com/gutris1/segsmaker/raw/main/script/controlnet/controlnet.py {sd}/asd",
        f"https://github.com/gutris1/segsmaker/raw/main/script/zrok.py {sd}",
        f"https://github.com/gutris1/segsmaker/raw/main/script/pinggy.py {sd}",
        f"https://github.com/gutris1/segsmaker/raw/main/script/ngrokk.py {sd}",
        f"https://github.com/gutris1/segsmaker/raw/main/script/venv.py {sd}",
        f"https://github.com/gutris1/segsmaker/raw/main/script/multi/segsmaker.py {sd}"]

    upscalers = [
        f"https://huggingface.co/pantat88/ui/resolve/main/4x-UltraSharp.pth {sd}/models/ESRGAN",
        f"https://huggingface.co/pantat88/ui/resolve/main/4x-AnimeSharp.pth {sd}/models/ESRGAN",
        f"https://huggingface.co/pantat88/ui/resolve/main/4x_NMKD-Superscale-SP_178000_G.pth {sd}/models/ESRGAN",
        f"https://huggingface.co/pantat88/ui/resolve/main/4x_RealisticRescaler_100000_G.pth {sd}/models/ESRGAN",
        f"https://huggingface.co/pantat88/ui/resolve/main/8x_RealESRGAN.pth {sd}/models/ESRGAN",
        f"https://huggingface.co/pantat88/ui/resolve/main/4x_foolhardy_Remacri.pth {sd}/models/ESRGAN"]

    line = scripts + upscalers
    for item in line:
        download(item)

    tempe()

def sd_15():
    sd_clone()

    extras = [
        f"https://huggingface.co/pantat88/ui/resolve/main/embeddings.zip {sd}",
        f"https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.safetensors {sd}/models/VAE"]

    for items in extras:
        download(items)

    get_ipython().system(f"unzip -qo {sd}/embeddings.zip -d {sd}/embeddings && rm {sd}/embeddings.zip")

    say("<br><b>【{red} Installing Extensions{d} 】{red}</b>")
    os.chdir(sd / "extensions")
    clone(str(sd / "asd/ext-15.txt"))

def sd_xl():
    sd_clone()

    extras = [
        f"https://civitai.com/api/download/models/182974 {sd}/embeddings",
        f"https://civitai.com/api/download/models/159385 {sd}/embeddings",
        f"https://civitai.com/api/download/models/159184 {sd}/embeddings",
        f"https://civitai.com/api/download/models/264491 {sd}/models/VAE XL_VAE_F1.safetensors"]

    for items in extras:
        download(items)

    say("<br><b>【{red} Installing Extensions{d} 】{red}</b>")
    os.chdir(sd / "extensions")
    clone(str(sd / "asd/ext-xl.txt"))

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

def sd_install(b):
    panel.close()
    clear_output()

    with loading:
        display(Image(filename=str(img)))

    with sd_setup:
        say("<b>【{red} Installing Stable Diffusion{d} 】{red}</b>")
        get_ipython().system(f"{repo}")

        marking(src, 'marking.json', 'A1111')

        if b == 'button-15':
            sd_15()
        elif b == 'button-xl':
            sd_xl()

        get_ipython().run_line_magic('run', f'{mark}')

        venv_install()
        os.chdir(home)

        with loading:
            loading.clear_output(wait=True)
            say("<b>【{red} Done{d} 】{red}</b>")

def go_back(b):
    panel.close()
    clear_output()

    with sd_setup:
        get_ipython().run_line_magic('run', f'{setup}')

loading = widgets.Output()
sd_setup = widgets.Output()

options = ['button-15', 'button-back', 'button-xl']
buttons = []

for btn in options:
    button = widgets.Button(description='')
    button.add_class(btn.lower())
    if btn == 'button-back':
        button.on_click(lambda x: go_back(btn))
    else:
        button.on_click(lambda x, btn=btn: sd_install(btn))
    buttons.append(button)

panel = widgets.HBox(
    buttons, layout=widgets.Layout(
        width='600px',
        height='405px'))

panel.add_class("multi-panel")

def webui_widgets():
    if sd.exists():
        git_dir = sd / '.git'
        if git_dir.exists():
            os.chdir(sd)
            commit_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip().decode('utf-8')

            if commit_hash != version:
                get_ipython().system(f"git pull origin {version}")
                get_ipython().system("git fetch --tags")

        x = [
            f"https://github.com/gutris1/segsmaker/raw/main/script/controlnet/controlnet.py {sd}/asd",
            f"https://github.com/gutris1/segsmaker/raw/main/script/zrok.py {sd}",
            f"https://github.com/gutris1/segsmaker/raw/main/script/pinggy.py {sd}",
            f"https://github.com/gutris1/segsmaker/raw/main/script/ngrokk.py {sd}",
            f"https://github.com/gutris1/segsmaker/raw/main/script/venv.py {sd}",
            f"https://github.com/gutris1/segsmaker/raw/main/script/multi/segsmaker.py {sd}"
        ]

        for y in x:
            download(y)

    else:
        if any([(home / 'forge').exists(), (home / 'ComfyUI').exists()]):
            print('Forge is installed, Uninstall first.' if (home / 'forge').exists() else 'ComfyUI is installed, Uninstall first.')
            get_ipython().run_line_magic('run', f'{mark}')
            return

        load_css()
        display(panel, sd_setup, loading)

webui_widgets()
