from IPython.display import display, HTML, clear_output
from ipywidgets import widgets, Layout
import os
from nenen88 import download, say, tempe

bura = "/home/studio-lab-user/asd/asd/cn-xl.css"
with open(bura, "r") as oppai:
    susu = oppai.read()
display(HTML(f"<style>{susu}</style>"))
    
url_list = {
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
        "https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid_sdxl_lora.safetensors ~/asd/models/Lora/tmp_Lora \
        ip-adapter-faceid_sdxl_lora.safetensors"],
    "IP Adapter FaceID Plusv2 SDXL": [
        "https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid-plusv2_sdxl.bin ip-adapter-faceid-plusv2_sdxl.bin",
        "https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid-plusv2_sdxl_lora.safetensors ~/asd/models/Lora/tmp_Lora \
        ip-adapter-faceid-plusv2_sdxl_lora.safetensors"]}

list_half = len(url_list) // 2
half_list_1 = dict(list(url_list.items())[:list_half])
half_list_2 = dict(list(url_list.items())[list_half:])

cb1 = widgets.VBox(
    [widgets.Checkbox(value=False, description=name, style={'description_width': '0px'})
     for name in half_list_1])
cb1.add_class("checkbox-group1")

cb2 = widgets.VBox(
    [widgets.Checkbox(value=False, description=name, style={'description_width': '0px'})
     for name in half_list_2])
cb2.add_class("checkbox-group2")

db = widgets.Button(description="Download")
db.add_class("download-button")
dbo = widgets.Output()
cbc = widgets.HBox([cb1, cb2], layout=widgets.Layout(align_items='flex-start'))
gariz2 = """<div class="gradient-cn">asd</div>"""
garis2 = widgets.Output()
def sa_cb(b):
    for checkbox in cb1.children + cb2.children:
        checkbox.value = True

def usa_cb(b):
    for checkbox in cb1.children + cb2.children:
        checkbox.value = False
        
sab = widgets.Button(description="Select All")
sab.add_class("select-all-button")
sab.on_click(sa_cb)

usab = widgets.Button(description="Unselect All")
usab.add_class("unselect-all-button")
usab.on_click(usa_cb)

bs = widgets.Button(description="")
bs.add_class("border-style")

bl = widgets.HBox([sab, usab, db, bs])
boks = widgets.VBox([bl, cbc], layout=Layout(
    display='flex',
    flex_flow='column',
    width='630px',
    height='455px',
    padding='0px'))
boks.add_class("boks")
        
def d_b_click(b):
    surl = []
    for checkbox, key in zip(cb1.children + cb2.children, list(url_list.keys())):
        if checkbox.value:
            surl.extend(url_list[key])
            
    widgets.Widget.close(boks)
    dbo.clear_output()
    
    with garis2:
        display(HTML(gariz2))
        
    with dbo:
        say("【{red} Downloading{cyan} Controlnet{magenta} Models{yellow} 】{red}")
        os.chdir("/home/studio-lab-user/asd/models/ControlNet")
        
        for url in surl:
            download(url)
        
        with garis2:
            garis2.clear_output()
            
        say("【{red} Done{d} 】{red}")
            
tempe()
display(boks, dbo, garis2)
db.on_click(d_b_click)
