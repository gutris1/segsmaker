from IPython.display import display, HTML, clear_output, Image
from ipywidgets import widgets, Layout
from IPython import get_ipython
from pathlib import Path
import subprocess, time, os, shlex
from nenen88 import pull, say, download, clone, tempe

version = "v1.9.4"
repo = f"git clone -q -b {version} https://github.com/gutris1/asd"

home = Path.home()
webui = home / "asd"
img = home / ".conda/loading.png"

os.chdir(home)

if webui.exists():
    git_dir = webui / '.git'
    if git_dir.exists():
        os.chdir(webui)
        commit_hash = os.popen('git rev-parse HEAD').read().strip()

        if commit_hash != version:
            get_ipython().system(f"git pull origin {version}")
            get_ipython().system("git fetch --tags")

    x = [f"https://github.com/gutris1/segsmaker/raw/main/script/controlnet/controlnet.py {webui}/asd",
         f"https://github.com/gutris1/segsmaker/raw/main/script/controlnet/cn-xl.css {webui}/asd",
         f"https://github.com/gutris1/segsmaker/raw/main/script/controlnet/cn-xl.py {webui}/asd",
         f"https://github.com/gutris1/segsmaker/raw/main/script/controlnet/cn-1_5.css {webui}/asd",
         f"https://github.com/gutris1/segsmaker/raw/main/script/controlnet/cn-1_5.py {webui}/asd",
         f"https://github.com/gutris1/segsmaker/raw/main/script/zrok_reg.py {webui}/asd",
         f"https://github.com/gutris1/segsmaker/raw/main/script/zrok.py {webui}",
         f"https://github.com/gutris1/segsmaker/raw/main/script/pinggy.py {webui}",
         f"https://github.com/gutris1/segsmaker/raw/main/script/ngrokk.py {webui}",
         f"https://github.com/gutris1/segsmaker/raw/main/script/venv.py {webui}"]

    for y in x:
        download(y)

else:
    css = home / ".conda/setup.css"
    devnull = {"stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL}

    get_ipython().system(f"curl -sLo {css} https://github.com/gutris1/segsmaker/raw/main/ui/sd/asd/setup.css")

    loading = widgets.Output()
    button1 = widgets.Button(description='SD 1.5')
    button2 = widgets.Button(description='SDXL')
    install_button = widgets.Button(description='Install')

    button_button = widgets.HBox([button1, button2], layout=Layout(justify_content='space-between'))
    sd_setup = widgets.Output()
    panel = widgets.VBox([button_button, install_button],
                         layout=Layout(
                             width='400px',
                             height='150px',
                             display='flex',
                             flex_flow='column',
                             align_items='center',
                             justify_content='space-between',
                             padding='20px'))
    button1.add_class("b1")
    button2.add_class("b2")
    install_button.add_class("out")
    panel.add_class("boxxx")
    selected = [None]

    def load_css(css):
        with css.open("r") as file:
            ccs = file.read()

        display(HTML(f"<style>{ccs}</style>"))

    def req_list(home, webui):
        return [
            f"rm -rf /tmp/venv /tmp/* {home}/tmp",
            f"rm -rf {webui}/models/Stable-diffusion/tmp_ckpt {webui}/models/Lora/tmp_lora {webui}/models/ControlNet",
            f"mkdir -p {webui}/models/Lora",
            f"mkdir -p {webui}/models/ESRGAN",
            f"ln -vs /tmp {home}/tmp",
            f"ln -vs /tmp/ckpt {webui}/models/Stable-diffusion/tmp_ckpt",
            f"ln -vs /tmp/lora {webui}/models/Lora/tmp_lora",
            f"ln -vs /tmp/controlnet {webui}/models/ControlNet"]

    def sd_clone(home, webui, devnull):
        time.sleep(1)
        pull(f"https://github.com/gutris1/segsmaker sd {webui}")

        os.chdir(webui)
        req = req_list(home, webui)

        for lines in req:
            subprocess.run(shlex.split(lines), **devnull)
            
        scripts = [
            f"https://github.com/gutris1/segsmaker/raw/main/script/controlnet/controlnet.py {webui}/asd",
            f"https://github.com/gutris1/segsmaker/raw/main/script/controlnet/cn-xl.css {webui}/asd",
            f"https://github.com/gutris1/segsmaker/raw/main/script/controlnet/cn-xl.py {webui}/asd",
            f"https://github.com/gutris1/segsmaker/raw/main/script/controlnet/cn-1_5.css {webui}/asd",
            f"https://github.com/gutris1/segsmaker/raw/main/script/controlnet/cn-1_5.py {webui}/asd",
            f"https://github.com/gutris1/segsmaker/raw/main/script/zrok_reg.py {webui}/asd",
            f"https://github.com/gutris1/segsmaker/raw/main/script/zrok.py {webui}",
            f"https://github.com/gutris1/segsmaker/raw/main/script/pinggy.py {webui}",
            f"https://github.com/gutris1/segsmaker/raw/main/script/ngrokk.py {webui}",
            f"https://github.com/gutris1/segsmaker/raw/main/script/venv.py {webui}"]
            
        upscalers = [
            f"https://huggingface.co/pantat88/ui/resolve/main/4x-UltraSharp.pth {webui}/models/ESRGAN",
            f"https://huggingface.co/pantat88/ui/resolve/main/4x-AnimeSharp.pth {webui}/models/ESRGAN",
            f"https://huggingface.co/pantat88/ui/resolve/main/4x_NMKD-Superscale-SP_178000_G.pth {webui}/models/ESRGAN",
            f"https://huggingface.co/pantat88/ui/resolve/main/4x_RealisticRescaler_100000_G.pth {webui}/models/ESRGAN",
            f"https://huggingface.co/pantat88/ui/resolve/main/8x_RealESRGAN.pth {webui}/models/ESRGAN",
            f"https://huggingface.co/pantat88/ui/resolve/main/4x_foolhardy_Remacri.pth {webui}/models/ESRGAN"]
        
        line = scripts + upscalers
        for item in line:
            download(item)

    def sd_1_5(home, webui, devnull):
        sd_clone(home, webui, devnull)

        extras = [
            f"https://huggingface.co/pantat88/ui/resolve/main/embeddings.zip {webui}",
            f"https://civitai.com/api/download/models/150491 {webui}/embeddings edgQuality.pt",
            f"https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.safetensors {webui}/models/VAE"]

        for items in extras:
            download(items)

        get_ipython().system(f"unzip -qo {webui}/embeddings.zip -d {webui}/embeddings && rm {webui}/embeddings.zip")

        say("<br><b>【{red} Installing Extensions{d} 】{red}</b>")
        os.chdir(webui / "extensions")
        clone(str(webui / "asd/ext-1_5.txt"))

    def sd_xl(home, webui, devnull):
        sd_clone(home, webui, devnull)

        extras = [
            f"https://civitai.com/api/download/models/182974 {webui}/embeddings",
            f"https://civitai.com/api/download/models/159385 {webui}/embeddings",
            f"https://civitai.com/api/download/models/159184 {webui}/embeddings",
            f"https://civitai.com/api/download/models/264491 {webui}/models/VAE XL_VAE_F1.safetensors"]

        for items in extras:
            download(items)

        say("<br><b>【{red} Installing Extensions{d} 】{red}</b>")
        os.chdir(webui / "extensions")
        clone(str(webui / "asd/ext-xl.txt"))

    def sd_install(selection):
        with loading:
            clear_output()
            display(Image(filename=str(img)))

        with sd_setup:
            sd_setup.clear_output()
            say("<b>【{red} Installing Stable Diffusion{d} 】{red}</b>")
            get_ipython().system(f"{repo}")

            if selection == 'SD 1.5':
                sd_1_5(home, webui, devnull)
            else:
                sd_xl(home, webui, devnull)
                
            with loading:
                loading.clear_output()
                
            say("<br><b>【{red} Done{d} 】{red}</b>")

    def button_panel(button):
        selected[0] = button.description

    def installing(button):
        selection = selected[0]

        if selection:
            widgets.Widget.close(panel)
            sd_setup.clear_output()
            sd_install(selection)

        else:
            with sd_setup:
                print("at least make a choice")
                print("少なくとも選択してよ。")
            return

    button1.on_click(button_panel)
    button2.on_click(button_panel)
    install_button.on_click(installing)

    load_css(css)
    display(panel, sd_setup, loading)
    tempe()
