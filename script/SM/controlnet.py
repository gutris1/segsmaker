from IPython.display import display, HTML, clear_output, Image
from ipywidgets import widgets
from pathlib import Path
from nenen88 import download, say, tempe
import os

SM = None

try:
    from KANDANG import TEMPPATH, HOMEPATH
    TMPLORA = Path(TEMPPATH) / 'lora'
    TMPCN = Path(TEMPPATH) / 'controlnet'
    HOME = Path(HOMEPATH)
    SM = False
except ImportError:
    TMPLORA = '/tmp/lora'
    TMPCN = '/tmp/controlnet'
    HOME = Path.home()
    SM = True

SRCN = Path(__file__).parent
CSSCN = SRCN / "controlnet.css"
IMG = "https://github.com/gutris1/segsmaker/raw/main/script/SM/loading.png"

cn15_list = {
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
        f"https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid_sd15_lora.safetensors {TMPLORA} \
        ip-adapter-faceid_sd15_lora.safetensors"],
    "IP Adapter FaceID Plus 1.5": [
        "https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid-plus_sd15.bin ip-adapter-faceid-plus_sd15.bin",
        f"https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid-plus_sd15_lora.safetensors {TMPLORA} \
        ip-adapter-faceid-plus_sd15_lora.safetensors"],
    "IP Adapter FaceID PlusV2 1.5": [
        "https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid-plusv2_sd15.bin ip-adapter-faceid-plusv2_sd15.bin",
        f"https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid-plusv2_sd15_lora.safetensors {TMPLORA} \
        ip-adapter-faceid-plusv2_sd15_lora.safetensors"],
    "IP Adapter FaceID Portrait 1.5": [
        "https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid-portrait_sd15.bin"]
}

cnxl_list = {
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
    "NoobAI IP Adapter SDXL": [
        "https://huggingface.co/subby2006/noob-ipa/resolve/main/noobIPAMARK1_mark1.safetensors \
        noobIPAMARK1_mark1.safetensors"],

    "IP Adapter FaceID SDXL": [
        "https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid_sdxl.bin ip-adapter-faceid_sdxl.bin",
        f"https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid_sdxl_lora.safetensors {TMPLORA} \
        ip-adapter-faceid_sdxl_lora.safetensors"],
    "IP Adapter FaceID Plusv2 SDXL": [
        "https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid-plusv2_sdxl.bin ip-adapter-faceid-plusv2_sdxl.bin",
        f"https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid-plusv2_sdxl_lora.safetensors {TMPLORA} \
        ip-adapter-faceid-plusv2_sdxl_lora.safetensors"],
    
    "Instant ID": [
        "https://huggingface.co/InstantX/InstantID/resolve/main/ip-adapter.bin ip-adapter_instant_id_sdxl.bin",
        "https://huggingface.co/InstantX/InstantID/resolve/main/ControlNetModel/diffusion_pytorch_model.safetensors control_instant_id_sdxl.safetensors"],
    
    "Controlnet Union SDXL 1.0": [
        "https://huggingface.co/xinsir/controlnet-union-sdxl-1.0/resolve/main/diffusion_pytorch_model.safetensors controlnet-union-sdxl-1.0.safetensors"],
    "Controlnet Union SDXL Pro Max": [
        "https://huggingface.co/xinsir/controlnet-union-sdxl-1.0/resolve/main/diffusion_pytorch_model_promax.safetensors controlnet-union-sdxl-promax.safetensors"]
}

def load_css():
    display(HTML(f"<style>{open(CSSCN).read()}</style>"))

loading = widgets.Output()
output = widgets.Output()

options = ['btn-cn-15', 'btn-cn-xl']
buttons = []

for btn in options:
    button = widgets.Button(description='')
    button.add_class(btn.lower())
    button.on_click(lambda x, btn=btn: Controlnet(btn))
    buttons.append(button)

cn_main_panel = widgets.HBox(layout=widgets.Layout(width='460px', height='405px'))

halflist_xl = len(cnxl_list) // 2
leftside_xl = dict(list(cnxl_list.items())[:halflist_xl])
rightside_xl = dict(list(cnxl_list.items())[halflist_xl:])
checkbox1_xl = widgets.VBox(
    [widgets.Checkbox(value=False, description=name, style={'description_width': '0px'}) for name in leftside_xl],
    layout=widgets.Layout(left='0px'))
checkbox2_xl = widgets.VBox(
    [widgets.Checkbox(value=False, description=name, style={'description_width': '0px'}) for name in rightside_xl],
    layout=widgets.Layout(left='20px'))
checkbox_layout_xl = widgets.HBox([checkbox1_xl, checkbox2_xl], layout=widgets.Layout(align_items='flex-start'))
download_button_xl = widgets.Button(description="Download", layout=widgets.Layout(left='130px'))
select_all_button_xl = widgets.Button(description="Select All", layout=widgets.Layout(left='30px'))
unselect_all_button_xl = widgets.Button(description="Unselect All", layout=widgets.Layout(left='35px'))
bottom_box_xl = widgets.Button(description="", disabled=True)
button_layout_xl = widgets.HBox([select_all_button_xl, unselect_all_button_xl, download_button_xl, bottom_box_xl])
cnxl_panel = widgets.Box(
    [button_layout_xl, checkbox_layout_xl],
    layout=widgets.Layout(display='none', flex_flow='column', width='660px', height='580px', padding='15px')
)

halflist_15 = len(cn15_list) // 2
leftside_15 = dict(list(cn15_list.items())[:halflist_15])
rightside_15 = dict(list(cn15_list.items())[halflist_15:])
checkbox1_15 = widgets.VBox(
    [widgets.Checkbox(value=False, description=name, style={'description_width': '0px'}) for name in leftside_15],
    layout=widgets.Layout(left='10px'))
checkbox2_15 = widgets.VBox(
    [widgets.Checkbox(value=False, description=name, style={'description_width': '0px'}) for name in rightside_15],
    layout=widgets.Layout(left='-60px'))
checkbox_layout_15 = widgets.HBox([checkbox1_15, checkbox2_15], layout=widgets.Layout(align_items='flex-start'))
download_button_15 = widgets.Button(description="Download", layout=widgets.Layout(width='130px', left='110px'))
select_all_button_15 = widgets.Button(description="Select All", layout=widgets.Layout(width='130px', left='15px'))
unselect_all_button_15 = widgets.Button(description="Unselect All", layout=widgets.Layout(width='130px', left='20px'))
bottom_box_15 = widgets.Button(description="", disabled=True)
button_layout_15 = widgets.HBox([select_all_button_15, unselect_all_button_15, download_button_15, bottom_box_15])
cn15_panel = widgets.Box(
    [button_layout_15, checkbox_layout_15],
    layout=widgets.Layout(display='none', flex_flow='column', width='550px', height='490px', padding='15px')
)

cn_main_panel.add_class('cn-panel')

cn15_panel.add_class("cn-15")
checkbox_layout_15.add_class('checkbox_layout_15')
checkbox1_15.add_class("checkbox")
checkbox2_15.add_class("checkbox")
select_all_button_15.add_class("select-all-button-15")
unselect_all_button_15.add_class("unselect-all-button-15")
download_button_15.add_class("download-button-15")
bottom_box_15.add_class("bottom-box-15")

cnxl_panel.add_class("cn-xl")
checkbox_layout_xl.add_class('checkbox_layout_xl')
checkbox1_xl.add_class("checkbox")
checkbox2_xl.add_class("checkbox")
select_all_button_xl.add_class("select-all-button-xl")
unselect_all_button_xl.add_class("unselect-all-button-xl")
download_button_xl.add_class("download-button-xl")
bottom_box_xl.add_class("bottom-box-xl")

def Controlnet(btn):
    cn_main_panel.close()
    if btn == 'btn-cn-15':
        cn15_panel.layout.display = 'flex'
    elif btn == 'btn-cn-xl':
        cnxl_panel.layout.display = 'flex'

def SelectAll(b):
    if cn15_panel.layout.display == 'flex':
        for check in checkbox1_15.children + checkbox2_15.children:
            check.value = True
    elif cnxl_panel.layout.display == 'flex':
        for check in checkbox1_xl.children + checkbox2_xl.children:
            check.value = True

def UnselectAll(b):
    if cn15_panel.layout.display == 'flex':
        for check in checkbox1_15.children + checkbox2_15.children:
            check.value = False
    elif cnxl_panel.layout.display == 'flex':
        for check in checkbox1_xl.children + checkbox2_xl.children:
            check.value = False

def Download(b):
    cn15_panel.close()
    cnxl_panel.close()
    tempe()

    with loading:
        display(Image(url=IMG))

    download_list = []

    if cn15_panel.layout.display == 'flex':
        cn15_panel.layout.display = 'none'
        for check, key in zip(checkbox1_15.children + checkbox2_15.children, list(cn15_list.keys())):
            if check.value:
                download_list.extend(cn15_list[key])

    elif cnxl_panel.layout.display == 'flex':
        cnxl_panel.layout.display = 'none'
        for check, key in zip(checkbox1_xl.children + checkbox2_xl.children, list(cnxl_list.keys())):
            if check.value:
                download_list.extend(cnxl_list[key])

    with output:
        os.chdir(TMPCN)
        for url in download_list:
            download(url)

        loading.clear_output()
        os.chdir(HOME)

z = [(CSSCN, f"curl -sLo {CSSCN} https://github.com/gutris1/segsmaker/raw/main/script/SM/controlnet.css")]
for x, y in z:
    if not SM:
        if not Path(x).exists():
            get_ipython().system(y)
    else:
        get_ipython().system(y)

load_css()
cn_main_panel.children = buttons
display(cn_main_panel, cn15_panel, cnxl_panel, loading, output)

select_all_button_15.on_click(SelectAll)
unselect_all_button_15.on_click(UnselectAll)
download_button_15.on_click(Download)
select_all_button_xl.on_click(SelectAll)
unselect_all_button_xl.on_click(UnselectAll)
download_button_xl.on_click(Download)
