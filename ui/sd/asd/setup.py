from IPython.display import display, HTML, clear_output
from ipywidgets import widgets, Layout
from IPython import get_ipython
from pathlib import Path
import subprocess, time, os, shlex
from nenen88 import pull, say, download, clone, tempe

version = "v1.9.3"
xxx = "/home/studio-lab-user"
zzz = Path(xxx) / "asd"

if zzz.exists():
    git_dir = zzz / '.git'
    if git_dir.exists():
        os.chdir(zzz)
        commit_hash = os.popen('git rev-parse HEAD').read().strip()

        if commit_hash != version:
            get_ipython().system(f"git pull origin {version}")
            get_ipython().system("git fetch --tags")

else:
    mama = f"{xxx}/.conda/setup.css"
    fff = {"stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL}

    get_ipython().system(f"rm -rf {xxx}/.zrok")
    get_ipython().system(f"curl -sLo {mama} https://github.com/gutris1/segsmaker/raw/main/ui/sd/asd/setup.css")

    gariz = """<div class="gradient-text">asd</div>"""
    garis = widgets.Output()
    b1 = widgets.Button(description='SD 1.5')
    b2 = widgets.Button(description='SDXL')
    ikuuuhhh = widgets.Button(description='Install')

    b1b2 = widgets.HBox([b1, b2], layout=Layout(justify_content='space-between'))
    sd_setup = widgets.Output()
    boxxx = widgets.VBox([b1b2, ikuuuhhh], layout=Layout(
        width='400px',
        height='150px',
        display='flex',
        flex_flow='column',
        align_items='center',
        justify_content='space-between',
        padding='20px'))

    b1.add_class("b1")
    b2.add_class("b2")
    ikuuuhhh.add_class("out")
    boxxx.add_class("boxxx")
    selected = [None]

    def ccss(mama):
        with open(mama, "r") as gantung:
            susu = gantung.read()

        display(HTML(f"<style>{susu}</style>"))

    def req_list(xxx, zzz):
        return [
            f"pip install -q -r requirements.txt basicsr insightface onnxruntime-gpu",
            f"rm -rf {xxx}/tmp/* {xxx}/tmp {zzz}/models/Stable-diffusion/tmp_ckpt {zzz}/models/Lora/tmp_lora {zzz}/models/ControlNet",
            f"mkdir -p {zzz}/models/Lora",
            f"mkdir -p {zzz}/models/ESRGAN",
            f"ln -vs /tmp {xxx}/tmp",
            f"ln -vs /tmp/ckpt {zzz}/models/Stable-diffusion/tmp_ckpt",
            f"ln -vs /tmp/lora {zzz}/models/Lora/tmp_lora",
            f"ln -vs /tmp/controlnet {zzz}/models/ControlNet"
        ]

    def sd_clone(xxx, zzz, fff):
        time.sleep(1)
        pull(f"https://github.com/gutris1/segsmaker sd {zzz}")

        os.chdir(zzz)
        req = req_list(xxx, zzz)
        for lines in req:
            subprocess.run(shlex.split(lines), **fff)

    def sd_1_5(xxx, zzz, fff):
        sd_clone(xxx, zzz, fff)

        extras = [
            f"https://huggingface.co/pantat88/ui/resolve/main/embeddings.zip {zzz}",
            f"https://civitai.com/api/download/models/150491 {zzz}/embeddings edgQuality.pt",
            f"https://huggingface.co/pantat88/ui/resolve/main/4x-UltraSharp.pth {zzz}/models/ESRGAN",
            f"https://huggingface.co/pantat88/ui/resolve/main/4x-AnimeSharp.pth {zzz}/models/ESRGAN",
            f"https://huggingface.co/pantat88/ui/resolve/main/4x_NMKD-Superscale-SP_178000_G.pth {zzz}/models/ESRGAN",
            f"https://huggingface.co/pantat88/ui/resolve/main/4x_RealisticRescaler_100000_G.pth {zzz}/models/ESRGAN",
            f"https://huggingface.co/pantat88/ui/resolve/main/8x_RealESRGAN.pth {zzz}/models/ESRGAN",
            f"https://huggingface.co/pantat88/ui/resolve/main/4x_foolhardy_Remacri.pth {zzz}/models/ESRGAN",
            f"https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.safetensors {zzz}/models/VAE",
            f"https://github.com/gutris1/segsmaker/raw/main/script/zrok_reg.py {zzz}/asd",
            f"https://github.com/gutris1/segsmaker/raw/main/script/zrok.py {zzz}",
            f"https://github.com/gutris1/segsmaker/raw/main/script/pinggy.py {zzz}"
        ]

        for items in extras:
            download(items)

        get_ipython().system(f"unzip -qo {zzz}/embeddings.zip -d {zzz}/embeddings && rm {zzz}/embeddings.zip")

        say("<br><b>【{red} Installing Extensions{d} 】{red}</b>")
        os.chdir(f"{zzz}/extensions")
        clone(f"{zzz}/asd/ext-1_5.txt")

        os.rename(f"{zzz}/asd/cn-1_5.py", f"{zzz}/asd/controlnet.py")

    def sd_xl(xxx, zzz, fff):
        sd_clone(xxx, zzz, fff)

        extras = [
            f"https://civitai.com/api/download/models/182974 {zzz}/embeddings",
            f"https://civitai.com/api/download/models/159385 {zzz}/embeddings",
            f"https://civitai.com/api/download/models/159184 {zzz}/embeddings",
            f"https://huggingface.co/pantat88/ui/resolve/main/4x-UltraSharp.pth {zzz}/models/ESRGAN",
            f"https://huggingface.co/pantat88/ui/resolve/main/4x-AnimeSharp.pth {zzz}/models/ESRGAN",
            f"https://huggingface.co/pantat88/ui/resolve/main/4x_NMKD-Superscale-SP_178000_G.pth {zzz}/models/ESRGAN",
            f"https://huggingface.co/pantat88/ui/resolve/main/4x_RealisticRescaler_100000_G.pth {zzz}/models/ESRGAN",
            f"https://huggingface.co/pantat88/ui/resolve/main/8x_RealESRGAN.pth {zzz}/models/ESRGAN",
            f"https://huggingface.co/pantat88/ui/resolve/main/4x_foolhardy_Remacri.pth {zzz}/models/ESRGAN",
            f"https://civitai.com/api/download/models/264491 {zzz}/models/VAE XL_VAE_F1.safetensors",
            f"https://github.com/gutris1/segsmaker/raw/main/script/zrok_reg.py {zzz}/asd",
            f"https://github.com/gutris1/segsmaker/raw/main/script/zrok.py {zzz}",
            f"https://github.com/gutris1/segsmaker/raw/main/script/pinggy.py {zzz}"
        ]

        for items in extras:
            download(items)

        say("<br><b>【{red} Installing Extensions{d} 】{red}</b>")
        os.chdir(f"{zzz}/extensions")
        clone(f"{zzz}/asd/ext-xl.txt")

        os.rename(f"{zzz}/asd/cn-xl.py", f"{zzz}/asd/controlnet.py")

    def zrok_install():
        zrok = Path(f"{xxx}/.zrok/bin")
        zrok.mkdir(parents=True, exist_ok=True)
        url = "https://github.com/openziti/zrok/releases/download/v0.4.25/zrok_0.4.25_linux_amd64.tar.gz"
        z = zrok / Path(url).name

        get_ipython().system(f"curl -sLo {z} {url}")
        get_ipython().system(f"tar -xzf {z} -C {zrok} --wildcards *zrok")
        get_ipython().system(f"rm -rf {xxx}/.cache/* {z}")

    def sd_install(selection):  
        with garis:
            display(HTML(gariz))

        with sd_setup:
            sd_setup.clear_output()
            os.chdir(xxx)
            say("<b>【{red} Installing Stable Diffusion{d} 】{red}</b>")
            get_ipython().system(f"git clone -q -b {version} https://github.com/gutris1/asd")

            if selection == 'SD 1.5':
                sd_1_5(xxx, zzz, fff)
            else:
                sd_xl(xxx, zzz, fff)
                
            with garis:
                garis.clear_output()
                
            say("<br><b>【{red} Done{d} 】{red}</b>")

    def cb(button):
        selected[0] = button.description

    def uuwaaahhh(button):
        selection = selected[0]

        if selection:
            widgets.Widget.close(boxxx)
            sd_setup.clear_output()
            sd_install(selection)

        else:
            with sd_setup:
                print("at least make a choice")
                print("少なくとも選択してよ。")
            return

    b1.on_click(cb)
    b2.on_click(cb)
    ikuuuhhh.on_click(uuwaaahhh)

    ccss(mama)
    display(boxxx, sd_setup, garis)
    zrok_install()
    tempe()