from IPython.display import display, HTML, clear_output
from ipywidgets import widgets, Layout
from IPython import get_ipython
import subprocess
import time
import os
from nenen88 import pull, say, download, clone, tempe

xxx = "/home/studio-lab-user"
zzz = f"{xxx}/asd"

if os.path.exists(zzz):
    say("/home/studio-lab-user/asd{cyan} already exists. Delete it first.")
    say("/home/studio-lab-user/asd{cyan} のおっぱいはすでに存在します。先に消してね。")
    
else:
    mama = f"{xxx}/.conda/setup.css"
    fff = {"shell": True, "stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL}
    gariz = """
    <div class="gradient-text">asd</div>
    """
    subprocess.run(f"curl -sLo {mama} https://github.com/gutris1/segsmaker/raw/main/ui/sd/asd/setup.css",
               **fff)
    
    garis = widgets.Output()
    selected = [None]
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

    def ccss(mama):
        with open(mama, "r") as gantung:
            susu = gantung.read()

        display(HTML(f"<style>{susu}</style>"))

    def gorengan(xxx, zzz):
        return [
            f"pip install -q -r requirements.txt basicsr",
            f"rm -rf {xxx}/tmp/* {xxx}/tmp {zzz}/models/Stable-diffusion/tmp_models {zzz}/models/Lora/tmp_Lora {zzz}/models/ControlNet",
            f"mkdir -p {zzz}/models/Lora",
            f"mkdir -p {zzz}/models/ESRGAN",
            f"ln -vs /tmp {xxx}/tmp",
            f"ln -vs /tmp/models {zzz}/models/Stable-diffusion/tmp_models",
            f"ln -vs /tmp/Lora {zzz}/models/Lora/tmp_Lora",
            f"ln -vs /tmp/ControlNet {zzz}/models/ControlNet",]

    def sd_1_5(xxx, zzz, fff):
        asu = f"git clone -q -b v1.8.0 https://github.com/gutris1/asd"
        subprocess.run(asu, **fff)

        time.sleep(2)
        pull(f"https://github.com/gutris1/segsmaker sd {zzz}")

        # requirements , tmp symlink
        os.chdir(zzz)
        minyak = gorengan(xxx, zzz)
        for tepung in minyak:
            subprocess.run(tepung, **fff)

        # embedding upscaler vae
        jalanan = [
            f"https://huggingface.co/pantat88/ui/resolve/main/embeddings.zip {zzz}",
            f"https://civitai.com/api/download/models/150491 {zzz}/embeddings edgQuality.pt",
            f"https://huggingface.co/pantat88/ui/resolve/main/4x-UltraSharp.pth {zzz}/models/ESRGAN",
            f"https://huggingface.co/pantat88/ui/resolve/main/4x-AnimeSharp.pth {zzz}/models/ESRGAN",
            f"https://huggingface.co/pantat88/ui/resolve/main/4x_NMKD-Superscale-SP_178000_G.pth {zzz}/models/ESRGAN",
            f"https://huggingface.co/pantat88/ui/resolve/main/4x_RealisticRescaler_100000_G.pth {zzz}/models/ESRGAN",
            f"https://huggingface.co/pantat88/ui/resolve/main/8x_RealESRGAN.pth {zzz}/models/ESRGAN",
            f"https://huggingface.co/pantat88/ui/resolve/main/4x_foolhardy_Remacri.pth {zzz}/models/ESRGAN",
            f"https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.safetensors {zzz}/models/VAE"]

        for janda in jalanan:
            download(janda)

        unzip = f"unzip -qo {zzz}/embeddings.zip -d {zzz}/embeddings && rm {zzz}/embeddings.zip"
        subprocess.run(unzip, **fff)

        # extension
        os.chdir(f"{zzz}/extensions")
        clone(f"{zzz}/asd/ext-1_5.txt")

        weww = f"{zzz}/asd/cn-1_5.py"
        woww = f"{zzz}/asd/controlnet.py"
        os.rename(weww, woww)

    def sd_xl(xxx, zzz, fff):
        asu = f"git clone -q -b v1.8.0 https://github.com/gutris1/asd"
        subprocess.run(asu, **fff)

        time.sleep(2)
        pull(f"https://github.com/gutris1/segsmaker sd {zzz}")

        # requirements , tmp symlink
        os.chdir(zzz)
        minyak = gorengan(xxx, zzz)
        for tepung in minyak:
            subprocess.run(tepung, **fff)

        # embedding upscaler vae
        jalanan = [
            f"https://civitai.com/api/download/models/182974 {zzz}/embeddings",
            f"https://civitai.com/api/download/models/356370 {zzz}/embeddings",
            f"https://civitai.com/api/download/models/159385 {zzz}/embeddings",
            f"https://civitai.com/api/download/models/159184 {zzz}/embeddings",
            f"https://huggingface.co/pantat88/ui/resolve/main/4x-UltraSharp.pth {zzz}/models/ESRGAN",
            f"https://huggingface.co/pantat88/ui/resolve/main/4x-AnimeSharp.pth {zzz}/models/ESRGAN",
            f"https://huggingface.co/pantat88/ui/resolve/main/4x_NMKD-Superscale-SP_178000_G.pth {zzz}/models/ESRGAN",
            f"https://huggingface.co/pantat88/ui/resolve/main/4x_RealisticRescaler_100000_G.pth {zzz}/models/ESRGAN",
            f"https://huggingface.co/pantat88/ui/resolve/main/8x_RealESRGAN.pth {zzz}/models/ESRGAN",
            f"https://huggingface.co/pantat88/ui/resolve/main/4x_foolhardy_Remacri.pth {zzz}/models/ESRGAN",
            f"https://civitai.com/api/download/models/264491 {zzz}/models/VAE XL_VAE_F1.safetensors"]

        for janda in jalanan:
            download(janda)

        # extension
        os.chdir(f"{zzz}/extensions")
        clone(f"{zzz}/asd/ext-xl.txt")

        weww = f"{zzz}/asd/cn-xl.py"
        woww = f"{zzz}/asd/controlnet.py"
        os.rename(weww, woww)

    def zrok_in():
        zorok = f"{xxx}/.zrok/bin"
        os.makedirs(zorok, exist_ok=True)
        tarok = f"{zorok}/zrok_0.4.25_linux_amd64.tar.gz"
        subprocess.run(f"curl -sLo {tarok} https://github.com/openziti/zrok/releases/download/v0.4.25/zrok_0.4.25_linux_amd64.tar.gz", **fff)
        subprocess.run(f"tar -xzf {tarok} -C {zorok} --wildcards *zrok", **fff)
        os.remove(tarok)

    def install(selection):  
        with garis:
            display(HTML(gariz))

        with sd_setup:
            sd_setup.clear_output()
            say("【{red} Installing Stable Diffusion{d} 】{red}")
            os.chdir(xxx)

            if selection == 'SD 1.5':
                sd_1_5(xxx, zzz, fff)
            else:
                sd_xl(xxx, zzz, fff)
                
            with garis:
                garis.clear_output()
                
            say("【{red} Done{d} 】{red}")

    def cb(button):
        selected[0] = button.description

    def uuwaaahhh(button):
        selection = selected[0]

        if selection:
            widgets.Widget.close(boxxx)
            sd_setup.clear_output()
            install(selection)

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
    zrok_in()
    tempe()
