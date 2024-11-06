from IPython.core.magic import register_line_magic
from IPython import get_ipython
from pathlib import Path
from nenen88 import tempe
from KANDANG import HOMEPATH, TEMPPATH
import json

HOME = Path(HOMEPATH)
marked = HOME / 'gutris1/marking.json'
tmp = Path(TEMPPATH)

def purge():
    var_list = [
        'webui', 'models', 'webui_output', 'extensions', 'embeddings',
        'vae', 'ckpt', 'lora', 'tmp_ckpt', 'tmp_lora', 'forge_svd', 'controlnet_widget'
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
        'ReForge': 'ReForge'
    }
    webui = HOME / webui_paths[ui] if ui in webui_paths else None
    webui_output = (
        webui / 'outputs' if ui in ('A1111', 'ReForge', 'Forge') else
        webui / 'output' if ui == 'ComfyUI' else None
    )
    return webui, webui_output

@register_line_magic
def uninstall_webui(line):
    ui = get_name(marked)
    webui, _ = get_webui_paths()
    get_ipython().system(f"rm -rf {webui}")
    print(f'{ui} uninstalled.')
    get_ipython().run_line_magic('cd', f'-q {HOME}')
    get_ipython().kernel.do_shutdown(True)

def set_paths(ui):
    webui_paths = {
        'A1111': ('A1111', 'extensions', 'embeddings', 'VAE', 'Stable-diffusion', 'Lora'),
        'Forge': ('Forge', 'extensions', 'embeddings', 'VAE', 'Stable-diffusion', 'Lora'),
        'ComfyUI': ('ComfyUI', 'custom_nodes', 'embeddings', 'vae', 'checkpoints', 'loras'),
        'ReForge': ('ReForge', 'extensions', 'embeddings', 'VAE', 'Stable-diffusion', 'Lora')
    }

    if ui in webui_paths:
        webui_name, ext, emb, v, c, l = webui_paths[ui]
        webui = HOME / webui_name if webui_name else None

        models = webui / 'models' if webui else None

        webui_output = (
            webui / 'outputs' if ui in ('A1111', 'ReForge', 'Forge') else
            webui / 'output' if ui == 'ComfyUI' else None
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

    controlnet_widget = (webui / 'asd' / 'controlnet.py') if (webui / 'asd').exists() else None
    forge_svd = tmp / 'svd' if ui in ['Forge', 'ReForge'] else None
    tmp_ckpt = tmp / 'ckpt'
    tmp_lora = tmp / 'lora'

    tempe()
