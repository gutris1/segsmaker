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
        f"https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid_sd15_lora.safetensors {tmplora} \
        ip-adapter-faceid_sd15_lora.safetensors"],
    "IP Adapter FaceID Plus 1.5": [
        "https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid-plus_sd15.bin ip-adapter-faceid-plus_sd15.bin",
        f"https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid-plus_sd15_lora.safetensors {tmplora} \
        ip-adapter-faceid-plus_sd15_lora.safetensors"],
    "IP Adapter FaceID PlusV2 1.5": [
        "https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid-plusv2_sd15.bin ip-adapter-faceid-plusv2_sd15.bin",
        f"https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid-plusv2_sd15_lora.safetensors {tmplora} \
        ip-adapter-faceid-plusv2_sd15_lora.safetensors"],
    "IP Adapter FaceID Portrait 1.5": [
        "https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid-portrait_sd15.bin"]
}

download_output = widgets.Output()
loading = widgets.Output()

half_list = len(controlnet_list) // 2
left_side = dict(list(controlnet_list.items())[:half_list])
right_side = dict(list(controlnet_list.items())[half_list:])

checkbox1 = widgets.VBox(
    [widgets.Checkbox(value=False, description=name, style={'description_width': '0px'}) for name in left_side],
    layout=widgets.Layout(left='10px'))

checkbox2 = widgets.VBox(
    [widgets.Checkbox(value=False, description=name, style={'description_width': '0px'}) for name in right_side],
    layout=widgets.Layout(left='-60px'))

checkbox_layout = widgets.HBox(
    [checkbox1, checkbox2],
    layout=widgets.Layout(top='-40px', align_items='flex-start'))

download_button = widgets.Button(description="Download", layout=widgets.Layout(width='130px', left='110px'))

select_all_button = widgets.Button(description="Select All", layout=widgets.Layout(width='130px', left='15px'))
unselect_all_button = widgets.Button(description="Unselect All", layout=widgets.Layout(width='130px', left='20px'))
bottom_box = widgets.Button(description="", disabled=True)

button_layout = widgets.HBox([select_all_button, unselect_all_button, download_button, bottom_box])

controlnet_widget = widgets.Box(
    [button_layout, checkbox_layout],
    layout=widgets.Layout(
        display='flex',
        flex_flow='column',
        width='550px',
        height='490px',
        padding='15px'))

controlnet_widget.add_class("cn-15")
checkbox1.add_class("checkbox")
checkbox2.add_class("checkbox")
select_all_button.add_class("select-all-button-15")
unselect_all_button.add_class("unselect-all-button-15")
download_button.add_class("download-button-15")
bottom_box.add_class("bottom-box-15")

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
