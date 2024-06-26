from IPython.display import display, HTML, clear_output, Image
from ipywidgets import widgets, Layout
from IPython import get_ipython
from pathlib import Path
import subprocess, time, os, shlex
from nenen88 import pull, say, download, clone, tempe

repo = f"git clone -q https://github.com/comfyanonymous/ComfyUI"

home = Path.home()
webui = home / "ComfyUI"
img = home / ".conda/loading.png"

os.chdir(home)

if webui.exists():
    git_dir = webui / '.git'
    if git_dir.exists():
        os.chdir(webui)
        commit_hash = os.popen('git rev-parse HEAD').read().strip()

        get_ipython().system("git pull origin master")
        get_ipython().system("git fetch --tags")

else:
    css = home / ".conda/setup.css"
    devnull = {"stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL}

    get_ipython().system("pip install -q pyngrok")
    get_ipython().system(f"curl -sLo {css} https://github.com/gutris1/segsmaker/raw/main/ui/sd/asd/setup.css")

    startup = home / ".ipython/profile_default/startup/comfyuickpt.py"
    get_ipython().system(f"curl -sLo {startup} https://github.com/gutris1/segsmaker/raw/main/script/comfyuickpt.py")

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
            f"unlink {webui}/models/checkpoints_symlink",
            f"rm -rf {home}/tmp/* {home}/tmp {webui}/models/checkpoints/tmp_ckpt",
            f"rm -rf {webui}/models/loras/tmp_lora {webui}/models/controlnet",
            f"ln -vs /tmp {home}/tmp",
            f"ln -vs /tmp/ckpt {webui}/models/checkpoints/tmp_ckpt",
            f"ln -vs /tmp/lora {webui}/models/loras/tmp_lora",
            f"ln -vs /tmp/controlnet {webui}/models/controlnet",
            f"ln -vs {webui}/models/checkpoints {webui}/models/checkpoints_symlink"]

    def clone_comfyui(home, webui, devnull):
        time.sleep(1)
        pull(f"https://github.com/gutris1/segsmaker cui {webui}")

        os.chdir(webui)
        req = req_list(home, webui)

        for lines in req:
            subprocess.run(shlex.split(lines), **devnull)
            
        scripts = [
            f"https://github.com/gutris1/segsmaker/raw/main/script/controlnet/cn-xl.css {webui}/asd",
            f"https://github.com/gutris1/segsmaker/raw/main/script/controlnet/cn-1_5.css {webui}/asd",
            f"https://github.com/gutris1/segsmaker/raw/main/script/zrok_reg.py {webui}/asd",
            f"https://github.com/gutris1/segsmaker/raw/main/script/venv.py {webui}"]
            
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

    def install_custom_nodes(webui):
        say("<br><b>【{red} Installing Custom Nodes{d} 】{red}</b>")
        os.chdir(webui / "custom_nodes")
        clone(str(webui / "asd/custom_nodes.txt"))

        custom_nodes_models = [
            f"https://github.com/sczhou/CodeFormer/releases/download/v0.1.0/codeformer.pth {webui}/models/facerestore_models",
            f"https://github.com/TencentARC/GFPGAN/releases/download/v1.3.4/GFPGANv1.4.pth {webui}/models/facerestore_models"]

        for item in custom_nodes_models:
            download(item)

    def sd_1_5(home, webui, devnull):
        clone_comfyui(home, webui, devnull)

        extras = [
            f"https://huggingface.co/pantat88/ui/resolve/main/embeddings.zip {webui}/models",
            f"https://civitai.com/api/download/models/150491 {webui}/models/embeddings edgQuality.pt",
            f"https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.safetensors {webui}/models/vae"]

        for items in extras:
            download(items)

        get_ipython().system(f"unzip -qo {webui}/models/embeddings.zip -d {webui}/models/embeddings")
        get_ipython().system(f"rm {webui}/models/embeddings.zip")

        install_custom_nodes(webui)

        os.rename(str(webui / "asd/cn-1_5.py"), str(webui / "asd/controlnet.py"))

    def sd_xl(home, webui, devnull):
        clone_comfyui(home, webui, devnull)

        extras = [
            f"https://civitai.com/api/download/models/182974 {webui}/models/embeddings",
            f"https://civitai.com/api/download/models/159385 {webui}/models/embeddings",
            f"https://civitai.com/api/download/models/159184 {webui}/models/embeddings",
            f"https://civitai.com/api/download/models/264491 {webui}/models/vae XL_VAE_F1.safetensors"]

        for items in extras:
            download(items)

        install_custom_nodes(webui)

        os.rename(str(webui / "asd/cn-xl.py"), str(webui / "asd/controlnet.py"))

    def sd_install(selection):
        with loading:
            clear_output()
            display(Image(filename=str(img)))

        with sd_setup:
            sd_setup.clear_output()
            say("<b>【{red} Installing ComfyUI{d} 】{red}</b>")
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
