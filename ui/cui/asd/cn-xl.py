from IPython.display import display, HTML, clear_output, Image
from nenen88 import download, say, tempe
from ipywidgets import widgets, Layout
from pathlib import Path
import os

home = Path.home()
img = home / ".conda/loading.png"

webui = Path(__file__).parent.parent
css = webui / "asd/cn-xl.css"
tmp_lora = webui / "models/loras/tmp_lora"

with open(css, "r") as file:
    css = file.read()
display(HTML(f"<style>{css}</style>"))
    
controlnet_list = {
    "Diffusers XL Canny Mid": [
        "https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/diffusers_xl_canny_mid.safetensors \
        diffusers_xl_canny_mid.safetensors"],
    "Diffusers XL Depth Mid": [
        "https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/diffusers_xl_depth_mid.safetensors \
        diffusers_xl_depth_mid.safetensors"],
        
    "Kohya Controllite XL Blur": [
        "https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/kohya_controllllite_xl_blur.safetensors \
        kohya_controllllite_xl_blur.safetensors"],
    "Kohya Controllite XL Blur Anime": [
        "https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/kohya_controllllite_xl_blur_anime.safetensors \
        kohya_controllllite_xl_blur_anime.safetensors"],
    "Kohya Controllite XL Canny": [
        "https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/kohya_controllllite_xl_canny.safetensors \
        kohya_controllllite_xl_canny.safetensors"],
    "Kohya Controllite XL Canny Anime": [
        "https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/kohya_controllllite_xl_canny_anime.safetensors \
        kohya_controllllite_xl_canny_anime.safetensors"],
    "Kohya Controllite XL Depth": [
        "https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/kohya_controllllite_xl_depth.safetensors \
        kohya_controllllite_xl_depth.safetensors"],
    "Kohya Controllite XL Depth Anime": [
        "https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/kohya_controllllite_xl_depth_anime.safetensors \
        kohya_controllllite_xl_depth_anime.safetensors"],
    "Kohya Controllite XL Openpose Anime": [
        "https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/kohya_controllllite_xl_openpose_anime.safetensors \
        kohya_controllllite_xl_openpose_anime.safetensors"],
    "Kohya Controllite XL Openpose Anime V2": [
        "https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/kohya_controllllite_xl_openpose_anime_v2.safetensors \
        kohya_controllllite_xl_openpose_anime_v2.safetensors"],
    "Kohya Controllite XL Scribble Anime": [
        "https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/kohya_controllllite_xl_scribble_anime.safetensors \
        kohya_controllllite_xl_scribble_anime.safetensors"],


    "T2I Adapter XL Canny": [
        "https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/t2i-adapter_xl_canny.safetensors \
        t2i-adapter_xl_canny.safetensors"],
    "T2I Adapter XL Openpose": [
        "https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/t2i-adapter_xl_openpose.safetensors \
        t2i-adapter_xl_openpose.safetensors"],
    "T2I Adapter XL Sketch": [
        "https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/t2i-adapter_xl_sketch.safetensors \
        t2i-adapter_xl_sketch.safetensors"],
    "T2I Adapter Diffusers XL Canny": [
        "https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/t2i-adapter_diffusers_xl_canny.safetensors \
        t2i-adapter_diffusers_xl_canny.safetensors"],
    "T2I Adapter Diffusers XL Depth Midas": [
        "https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/t2i-adapter_diffusers_xl_depth_midas.safetensors \
        t2i-adapter_diffusers_xl_depth_midas.safetensors"],
    "T2I Adapter Diffusers XL Depth Zoe": [
        "https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/t2i-adapter_diffusers_xl_depth_zoe.safetensors \
        t2i-adapter_diffusers_xl_depth_zoe.safetensors"],
    "T2I Adapter Diffusers XL Lineart": [
        "https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/t2i-adapter_diffusers_xl_lineart.safetensors \
        t2i-adapter_diffusers_xl_lineart.safetensors"],
    "T2I Adapter Diffusers XL Openpose": [
        "https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/t2i-adapter_diffusers_xl_openpose.safetensors \
        t2i-adapter_diffusers_xl_openpose.safetensors"],
    "T2I Adapter Diffusers XL Sketch": [
        "https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/t2i-adapter_diffusers_xl_sketch.safetensors \
        t2i-adapter_diffusers_xl_sketch.safetensors"],

    "IP Adapter SDXL": [
        "https://huggingface.co/h94/IP-Adapter/resolve/main/sdxl_models/ip-adapter_sdxl.safetensors \
        ip-adapter_sdxl.safetensors"],
    "IP Adapter SDXL VIT-H": [
        "https://huggingface.co/h94/IP-Adapter/resolve/main/sdxl_models/ip-adapter_sdxl_vit-h.safetensors \
        ip-adapter_sdxl_vit-h.safetensors"],
    "IP Adapter Plus SDXL VIT-H": [
        "https://huggingface.co/h94/IP-Adapter/resolve/main/sdxl_models/ip-adapter-plus_sdxl_vit-h.safetensors \
        ip-adapter-plus_sdxl_vit-h.safetensors"],
    "IP Adapter Plus Face SDXL VIT-H": [
        "https://huggingface.co/h94/IP-Adapter/resolve/main/sdxl_models/ip-adapter-plus-face_sdxl_vit-h.safetensors \
        ip-adapter-plus-face_sdxl_vit-h.safetensors"],

    "IP Adapter FaceID SDXL": [
        "https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid_sdxl.bin ip-adapter-faceid_sdxl.bin",
        f"https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid_sdxl_lora.safetensors {tmp_lora} \
        ip-adapter-faceid_sdxl_lora.safetensors"],
    "IP Adapter FaceID Plusv2 SDXL": [
        "https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid-plusv2_sdxl.bin ip-adapter-faceid-plusv2_sdxl.bin",
        f"https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid-plusv2_sdxl_lora.safetensors {tmp_lora} \
        ip-adapter-faceid-plusv2_sdxl_lora.safetensors"],
    
    "Instant ID": [
        "https://huggingface.co/InstantX/InstantID/resolve/main/ip-adapter.bin ip-adapter_instant_id_sdxl.bin",
        "https://huggingface.co/InstantX/InstantID/resolve/main/ControlNetModel/diffusion_pytorch_model.safetensors control_instant_id_sdxl.safetensors"]
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
                                     height='480px',
                                     padding='0px'))

controlnet_widget.add_class("controlnet-xl")
        
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
        os.chdir(f"{webui}/models/controlnet")
        for url in download_list:
            download(url)

        loading.clear_output()
        say("【{red} Done{d} 】{red}")
            
tempe()
display(controlnet_widget, download_output, loading)
download_button.on_click(download_button_click)
