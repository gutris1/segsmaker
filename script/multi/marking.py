from IPython.core.magic import register_line_magic
from IPython import get_ipython
from pathlib import Path
from nenen88 import tempe
import json

HOME = Path.home()
SRC = HOME / '.gutris1'
marked = SRC / 'marking.json'
tmp = Path('/tmp')

def purge():
    var_list = [
        'webui', 'models', 'webui_output', 'extensions', 'embeddings',
        'vae', 'ckpt', 'lora', 'tmp_ckpt', 'tmp_lora', 'forge_svd', 'controlnet_models'
    ]
    for var in var_list:
        if var in globals():
            del globals()[var]

def get_name(path):
    with open(path, 'r') as file:
        value = json.load(file)
        return value.get('ui', None)

def get_webui_paths():
    ui = get_name(marked)
    webui_paths = {
        'A1111': 'A1111',
        'Forge': 'Forge',
        'ComfyUI': 'ComfyUI',
        'ReForge': 'ReForge',
        'FaceFusion': 'FaceFusion',
        'SDTrainer': 'SDTrainer'
    }
    webui = HOME / webui_paths[ui] if ui in webui_paths else None
    webui_output = (
        webui / 'outputs' if ui in ('A1111', 'ReForge') else
        webui / 'output' if ui in ('ComfyUI', 'Forge', 'SDTrainer') else
        None
    )
    return webui, webui_output

@register_line_magic
def clear_output_images(line):
    ui = get_name(marked)
    _, webui_output = get_webui_paths()
    get_ipython().system(f"rm -rf {webui_output}/* {HOME / '.cache/*'}")
    get_ipython().run_line_magic('cd', '-q ~')
    print(f'{ui} outputs cleared.')

@register_line_magic
def uninstall_webui(line):
    ui = get_name(marked)
    webui, _ = get_webui_paths()
    get_ipython().system(f"rm -rf {webui} {HOME / 'tmp'} {HOME / '.cache/*'}")
    get_ipython().run_line_magic('cd', '-q ~')
    print(f'{ui} uninstalled.')
    get_ipython().kernel.do_shutdown(True)

def set_paths(ui):
    webui_paths = {
        'A1111': ('A1111', 'extensions', 'embeddings', 'VAE', 'Stable-diffusion', 'Lora'),
        'Forge': ('Forge', 'extensions', 'embeddings', 'VAE', 'Stable-diffusion', 'Lora'),
        'ComfyUI': ('ComfyUI', 'custom_nodes', 'embeddings', 'vae', 'checkpoints', 'loras'),
        'ReForge': ('ReForge', 'extensions', 'embeddings', 'VAE', 'Stable-diffusion', 'Lora'),
        'FaceFusion': ('FaceFusion', None, None, None, None, None),
        'SDTrainer': ('SDTrainer', None, None, 'VAE', 'sd-models', None)
    }

    if ui in webui_paths:
        webui_name, ext, emb, v, c, l = webui_paths[ui]
        webui = HOME / webui_name if webui_name else None

        models = webui if ui == 'SDTrainer' else (webui / 'models' if webui else None)

        webui_output = (
            webui / 'outputs' if ui in ('A1111', 'ReForge') else
            webui / 'output' if ui in ('ComfyUI', 'Forge', 'SDTrainer') else
            None
        )

        extensions = webui / ext if ext else None
        embeddings = (
            models / emb if ui == 'ComfyUI' else
            webui / emb if ui in ('A1111', 'Forge', 'ReForge') else
            None
        )

        vae = models / v if models and v else None
        ckpt = models / c if models and c else None
        lora = models / l if models and l else None
        
        return webui, models, webui_output, extensions, embeddings, vae, ckpt, lora

if marked.exists():
    purge()

    ui = get_name(marked)
    webui, models, webui_output, extensions, embeddings, vae, ckpt, lora = set_paths(ui)

    controlnet_models = (webui / 'asd' / 'controlnet.py') if (webui / 'asd').exists() else None
    forge_svd = tmp / 'svd' if ui in ['Forge', 'ReForge'] else None
    tmp_ckpt = tmp / 'ckpt'
    tmp_lora = tmp / 'lora'

    tempe()
