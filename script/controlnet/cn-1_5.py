from IPython.display import display, HTML, clear_output, Image
from nenen88 import download, say, tempe
from ipywidgets import widgets, Layout
from pathlib import Path
import os

home = Path.home()
conda = home / ".conda"
img = conda / "loading.png"

webui = Path(__file__).parent.parent
css = Path(__file__).parent / "cn-1_5.css"

with open(css, "r") as file:
    css = file.read()
display(HTML(f"<style>{css}</style>"))
    
controlnet_list = {
    "Openpose": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_openpose_fp16.safetensors openpose.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_openpose_fp16.yaml openpose.yaml"],
    "Canny": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_canny_fp16.safetensors canny.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_canny_fp16.yaml canny.yaml"],
    "Depth": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11f1p_sd15_depth_fp16.safetensors depth.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11f1p_sd15_depth_fp16.yaml depth.yaml"],
    "Lineart": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_lineart_fp16.safetensors lineart.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_lineart_fp16.yaml lineart.yaml"],
    "Lineart Anime": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15s2_lineart_anime_fp16.safetensors lineart_anime.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15s2_lineart_anime_fp16.yaml lineart_anime.yaml"],
    "ip2p": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11e_sd15_ip2p_fp16.safetensors ip2p.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11e_sd15_ip2p_fp16.yaml ip2p.yaml"],
    "Shuffle": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11e_sd15_shuffle_fp16.safetensors shuffle.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11e_sd15_shuffle_fp16.yaml shuffle.yaml"],
    "Inpaint": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_inpaint_fp16.safetensors inpaint.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_inpaint_fp16.yaml inpaint.yaml"],
    "MLSD": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_mlsd_fp16.safetensors mlsd.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_mlsd_fp16.yaml mlsd.yaml"],
    "Normalbae": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_normalbae_fp16.safetensors normalbae.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_normalbae_fp16.yaml normalbae.yaml"],
    "Scribble": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_scribble_fp16.safetensors scribble.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_scribble_fp16.yaml scribble.yaml"],
    "Seg": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_seg_fp16.safetensors seg.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_seg_fp16.yaml seg.yaml"],
    "Softedge": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_softedge_fp16.safetensors softedge.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_softedge_fp16.yaml softedge.yaml"],
    "Tile": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11f1e_sd15_tile_fp16.safetensors tile.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11f1e_sd15_tile_fp16.yaml tile.yaml"],
    
    "IP Adapter 1.5": [
        "https://huggingface.co/h94/IP-Adapter/resolve/main/models/ip-adapter_sd15.safetensors ip-adapter_sd15.safetensors"],
    "IP Adapter 1.5 Light": [
        "https://huggingface.co/h94/IP-Adapter/resolve/main/models/ip-adapter_sd15_light.safetensors ip-adapter_sd15_light.safetensors"],
    "IP Adapter 1.5 VIT-G": [
        "https://huggingface.co/h94/IP-Adapter/resolve/main/models/ip-adapter_sd15_vit-G.safetensors ip-adapter_sd15_vit-G.safetensors"],
    "IP Adapter Plus 1.5": [
        "https://huggingface.co/h94/IP-Adapter/resolve/main/models/ip-adapter-plus_sd15.safetensors ip-adapter-plus_sd15.safetensors"],
    "IP Adapter Plus Face 1.5": [
        "https://huggingface.co/h94/IP-Adapter/resolve/main/models/ip-adapter-plus-face_sd15.safetensors ip-adapter-plus-face_sd15.safetensors"],
    "IP Adapter Full Face 1.5": [
        "https://huggingface.co/h94/IP-Adapter/resolve/main/models/ip-adapter-full-face_sd15.safetensors ip-adapter-full-face_sd15.safetensors"],

    "IP Adapter FaceID 1.5": [
        "https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid_sd15.bin",
        f"https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid_sd15_lora.safetensors {webui}/models/Lora/tmp_lora \
        ip-adapter-faceid_sd15_lora.safetensors"],
    "IP Adapter FaceID Plus 1.5": [
        "https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid-plus_sd15.bin ip-adapter-faceid-plus_sd15.bin",
        f"https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid-plus_sd15_lora.safetensors {webui}/models/Lora/tmp_lora \
        ip-adapter-faceid-plus_sd15_lora.safetensors"],
    "IP Adapter FaceID PlusV2 1.5": [
        "https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid-plusv2_sd15.bin ip-adapter-faceid-plusv2_sd15.bin",
        f"https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid-plusv2_sd15_lora.safetensors {webui}/models/Lora/tmp_lora \
        ip-adapter-faceid-plusv2_sd15_lora.safetensors"],
    "IP Adapter FaceID Portrait 1.5": [
        "https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid-portrait_sd15.bin"]
}

half_list = len(controlnet_list) // 2
left_side = dict(list(controlnet_list.items())[:half_list])
right_side = dict(list(controlnet_list.items())[half_list:])

checkbox1 = widgets.VBox(
    [widgets.Checkbox(value=False, description=name, style={'description_width': '0px'})
     for name in left_side])
checkbox1.add_class("checkbox-group1")

checkbox2 = widgets.VBox(
    [widgets.Checkbox(value=False, description=name, style={'description_width': '0px'})
     for name in right_side])
checkbox2.add_class("checkbox-group2")

download_button = widgets.Button(description="Download")
download_button.add_class("download-button")
download_output = widgets.Output()
checkbox_layout = widgets.HBox([checkbox1, checkbox2], layout=widgets.Layout(align_items='flex-start'))

loading = widgets.Output()

def select_all_checkboxs(b):
    for check in checkbox1.children + checkbox2.children:
        check.value = True

def unselect_all_checkboxs(b):
    for check in checkbox1.children + checkbox2.children:
        check.value = False
        
select_all_button = widgets.Button(description="Select All")
select_all_button.add_class("select-all-button")
select_all_button.on_click(select_all_checkboxs)

unselect_all_button = widgets.Button(description="Unselect All")
unselect_all_button.add_class("unselect-all-button")
unselect_all_button.on_click(unselect_all_checkboxs)

bottom_box = widgets.Button(description="")
bottom_box.add_class("border-style")

button_layout = widgets.HBox([select_all_button, unselect_all_button, download_button, bottom_box])
controlnet_widget = widgets.VBox([button_layout, checkbox_layout],
                                 layout=Layout(
                                     display='flex',
                                     flex_flow='column',
                                     width='630px',
                                     height='455px',
                                     align_items='center',
                                     padding='10px'))

controlnet_widget.add_class("controlnet-1-5")
        
def download_button_click(b):
    download_list = []
    for check, key in zip(checkbox1.children + checkbox2.children, list(controlnet_list.keys())):
        if check.value:
            download_list.extend(controlnet_list[key])

    clear_output(wait=True)
    widgets.Widget.close(controlnet_widget)

    with loading:
        display(Image(filename=str(img)))
        
    with download_output:
        os.chdir(f"{webui}/models/ControlNet")
        for url in download_list:
            download(url)

        loading.clear_output()
        say("【{red} Done{d} 】{red}")
            
tempe()
display(controlnet_widget, download_output, loading)
download_button.on_click(download_button_click)
