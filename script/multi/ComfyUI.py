from IPython.display import display, HTML, clear_output, Image
from ipywidgets import widgets
from IPython import get_ipython
from pathlib import Path
import subprocess, time, os, shlex, json, shutil
from nenen88 import pull, say, download, clone, tempe

repo = f"git clone -q https://github.com/comfyanonymous/ComfyUI"

home = Path.home()
src = home / '.gutris1'
css_setup = src / 'setup.css'
img = src / 'loading.png'
mark = src / 'marking.py'
setup = home / '.conda/setup.py'

tmp = Path('/tmp')
vnv = tmp / 'venv'

webui = home / "ComfyUI"

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
    url = 'https://huggingface.co/pantat88/back_up/resolve/main/venv.tar.lz4'
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
        get_ipython().system(f'python -m venv {vnv}')
        get_ipython().system(f'{vnv / "bin" / "python"} -m pip install -q --upgrade pip')

def req_list():
    return [
        f"rm -rf {home}/tmp {home}/.cache/*",
        f"rm -rf {webui}/models/checkpoints/tmp_ckpt",
        f"rm -rf {webui}/models/loras/tmp_lora {webui}/models/controlnet",
        f"ln -vs /tmp {home}/tmp",
        f"ln -vs /tmp/ckpt {webui}/models/checkpoints/tmp_ckpt",
        f"ln -vs /tmp/lora {webui}/models/loras/tmp_lora",
        f"ln -vs /tmp/controlnet {webui}/models/controlnet",
        f"ln -vs {webui}/models/checkpoints {webui}/models/checkpoints_symlink"]

def clone_comfyui():
    time.sleep(1)
    pull(f"https://github.com/gutris1/segsmaker cui {webui}")

    tmp_cleaning()

    os.chdir(webui)
    req = req_list()

    for lines in req:
        subprocess.run(shlex.split(lines), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    scripts = [
        f"https://github.com/gutris1/segsmaker/raw/main/script/controlnet/controlnet.py {webui}/asd",
        f"https://github.com/gutris1/segsmaker/raw/main/script/venv.py {webui}",
        f"https://github.com/gutris1/segsmaker/raw/main/script/multi/segsmaker.py {webui}"]

    upscalers = [
        f"https://huggingface.co/pantat88/ui/resolve/main/4x-UltraSharp.pth {webui}/models/upscale_models",
        f"https://huggingface.co/pantat88/ui/resolve/main/4x-AnimeSharp.pth {webui}/models/upscale_models",
        f"https://huggingface.co/pantat88/ui/resolve/main/4x_NMKD-Superscale-SP_178000_G.pth {webui}/models/upscale_models",
        f"https://huggingface.co/pantat88/ui/resolve/main/4x_RealisticRescaler_100000_G.pth {webui}/models/upscale_models",
        f"https://huggingface.co/pantat88/ui/resolve/main/8x_RealESRGAN.pth {webui}/models/upscale_models",
        f"https://huggingface.co/pantat88/ui/resolve/main/4x_foolhardy_Remacri.pth {webui}/models/upscale_models"]

    line = scripts + upscalers
    for item in line:
        download(item)

    tempe()

def install_custom_nodes():
    say("<br><b>【{red} Installing Custom Nodes{d} 】{red}</b>")
    os.chdir(webui / "custom_nodes")
    clone(str(webui / "asd/custom_nodes.txt"))
    print()
    custom_nodes_models = [
        f"https://github.com/sczhou/CodeFormer/releases/download/v0.1.0/codeformer.pth {webui}/models/facerestore_models",
        f"https://github.com/TencentARC/GFPGAN/releases/download/v1.3.4/GFPGANv1.4.pth {webui}/models/facerestore_models"]

    for item in custom_nodes_models:
        download(item)

def sd_15():
    clone_comfyui()

    extras = [
        f"https://huggingface.co/pantat88/ui/resolve/main/embeddings.zip {webui}/models",
        f"https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.safetensors {webui}/models/vae"]

    for items in extras:
        download(items)

    get_ipython().system(f"unzip -qo {webui}/models/embeddings.zip -d {webui}/models/embeddings")
    get_ipython().system(f"rm {webui}/models/embeddings.zip")

    install_custom_nodes()

def sd_xl():
    clone_comfyui()

    extras = [
        f"https://civitai.com/api/download/models/182974 {webui}/models/embeddings",
        f"https://civitai.com/api/download/models/159385 {webui}/models/embeddings",
        f"https://civitai.com/api/download/models/159184 {webui}/models/embeddings",
        f"https://civitai.com/api/download/models/264491 {webui}/models/vae XL_VAE_F1.safetensors"]

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

def sd_install(b):
    panel.close()
    clear_output()

    with loading:
        display(Image(filename=str(img)))

    with sd_setup:
        say("<b>【{red} Installing ComfyUI{d} 】{red}</b>")
        get_ipython().system(f"{repo}")

        marking(src, 'marking.json', 'ComfyUI')

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

if webui.exists():
    git_dir = webui / '.git'
    if git_dir.exists():
        os.chdir(webui)
        commit_hash = os.popen('git rev-parse HEAD').read().strip()

        get_ipython().system("git pull origin master")
        get_ipython().system("git fetch --tags")

    x = [
        f"https://github.com/gutris1/segsmaker/raw/main/script/controlnet/controlnet.py {webui}/asd",
        f"https://github.com/gutris1/segsmaker/raw/main/script/venv.py {webui}",
        f"https://github.com/gutris1/segsmaker/raw/main/ui/cui/apotek.py {webui}",
        f"https://github.com/gutris1/segsmaker/raw/main/ui/cui/ngrokk.py {webui}",
        f"https://github.com/gutris1/segsmaker/raw/main/ui/cui/pinggy.py {webui}",
        f"https://github.com/gutris1/segsmaker/raw/main/ui/cui/zrok.py {webui}",
        f"https://github.com/gutris1/segsmaker/raw/main/script/multi/segsmaker.py {webui}"]

    for y in x:
        download(y)

else:
    load_css()
    display(panel, sd_setup, loading)