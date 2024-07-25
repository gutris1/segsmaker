from IPython.display import display, HTML, clear_output, Image
from IPython import get_ipython
from ipywidgets import widgets
from pathlib import Path
from nenen88 import download, say, tempe

src_cn = Path(__file__).parent
css_cn = src_cn / "cn.css"
tmplora = '/tmp/lora'
tmpcn = '/tmp/controlnet'
img = Path.home() / ".gutris1/loading.png"
    
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
        f"https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid_sdxl_lora.safetensors {tmplora} \
        ip-adapter-faceid_sdxl_lora.safetensors"],
    "IP Adapter FaceID Plusv2 SDXL": [
        "https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid-plusv2_sdxl.bin ip-adapter-faceid-plusv2_sdxl.bin",
        f"https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid-plusv2_sdxl_lora.safetensors {tmplora} \
        ip-adapter-faceid-plusv2_sdxl_lora.safetensors"],
    
    "Instant ID": [
        "https://huggingface.co/InstantX/InstantID/resolve/main/ip-adapter.bin ip-adapter_instant_id_sdxl.bin",
        "https://huggingface.co/InstantX/InstantID/resolve/main/ControlNetModel/diffusion_pytorch_model.safetensors control_instant_id_sdxl.safetensors"],
    
    "Controlnet Union SDXL 1.0": [
        "https://huggingface.co/xinsir/controlnet-union-sdxl-1.0/resolve/main/diffusion_pytorch_model.safetensors controlnet-union-sdxl-1.0.safetensors"],
    "Controlnet Union SDXL Pro Max": [
        "https://huggingface.co/xinsir/controlnet-union-sdxl-1.0/resolve/main/diffusion_pytorch_model_promax.safetensors controlnet-union-sdxl-promax.safetensors"]
}

download_output = widgets.Output()
loading = widgets.Output()

half_list = len(controlnet_list) // 2
left_side = dict(list(controlnet_list.items())[:half_list])
right_side = dict(list(controlnet_list.items())[half_list:])

checkbox1 = widgets.VBox(
    [widgets.Checkbox(value=False, description=name, style={'description_width': '0px'}) for name in left_side],
    layout=widgets.Layout(left='5px'))

checkbox2 = widgets.VBox(
    [widgets.Checkbox(value=False, description=name, style={'description_width': '0px'}) for name in right_side],
    layout=widgets.Layout(left='10px'))

checkbox_layout = widgets.HBox(
    [checkbox1, checkbox2],
    layout=widgets.Layout(top='-40px', align_items='flex-start'))

download_button = widgets.Button(description="Download", layout=widgets.Layout(left='130px'))
select_all_button = widgets.Button(description="Select All", layout=widgets.Layout(left='30px'))
unselect_all_button = widgets.Button(description="Unselect All", layout=widgets.Layout(left='35px'))
bottom_box = widgets.Button(description="", disabled=True)

button_layout = widgets.HBox([select_all_button, unselect_all_button, download_button, bottom_box])

controlnet_widget = widgets.Box(
    [button_layout, checkbox_layout],
    layout=widgets.Layout(
        display='flex',
        flex_flow='column',
        width='640px',
        height='580px',
        padding='15px'))

controlnet_widget.add_class("cn-xl")
checkbox1.add_class("checkbox")
checkbox2.add_class("checkbox")
select_all_button.add_class("select-all-button-xl")
unselect_all_button.add_class("unselect-all-button-xl")
download_button.add_class("download-button-xl")
bottom_box.add_class("bottom-box-xl")

def load_css():
    with open(css_cn, "r") as file:
        content = file.read()

    display(HTML(f"<style>{content}</style>"))

def select_all_checkboxes(b):
    for check in checkbox1.children + checkbox2.children:
        check.value = True

def unselect_all_checkboxes(b):
    for check in checkbox1.children + checkbox2.children:
        check.value = False

def downloading(b):
    controlnet_widget.close()
    clear_output(wait=True)

    download_list = []

    for check, key in zip(checkbox1.children + checkbox2.children, list(controlnet_list.keys())):
        if check.value:
            download_list.extend(controlnet_list[key])

    with loading:
        display(Image(filename=str(img)))
        
    with download_output:
        get_ipython().run_line_magic('cd', f'-q {tmpcn}')

        for url in download_list:
            download(url)

        loading.clear_output()
        say("【{red} Done{d} 】{red}")
        get_ipython().run_line_magic('cd', '-q ~')

tempe()
load_css()
display(controlnet_widget, download_output, loading)

select_all_button.on_click(select_all_checkboxes)
unselect_all_button.on_click(unselect_all_checkboxes)
download_button.on_click(downloading)
