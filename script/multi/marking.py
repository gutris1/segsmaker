from IPython.core.magic import register_line_magic
from pathlib import Path
from nenen88 import tempe
import json

home = Path.home()
gutris1 = home / '.gutris1'
marked = gutris1 / 'marking.json'
tmp = Path('/tmp')

def purge():
    var_list = [
        'webui',
        'models',
        'webui_output',
        'extensions',
        'embeddings',
        'vae',
        'ckpt',
        'lora',
        'tmp_ckpt',
        'tmp_lora',
        'forge_svd',
        'controlnet_models'
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
        'A1111': 'asd',
        'Forge': 'forge',
        'ComfyUI': 'ComfyUI'
    }

    webui = home / webui_paths[ui]
    webui_output = webui / 'outputs' if ui == 'A1111' else webui / 'output'
    return webui, webui_output

@register_line_magic
def clear_output_images(line):
    ui = get_name(marked)
    _, webui_output = get_webui_paths()
    get_ipython().system(f"rm -rf {webui_output}/* {home / '.cache/*'}")
    get_ipython().run_line_magic('cd', '-q ~')
    print(f'{ui} outputs cleared.')

@register_line_magic
def uninstall_webui(line):
    ui = get_name(marked)
    webui, _ = get_webui_paths()
    get_ipython().system(f"rm -rf {webui} {home / 'tmp'} {home / '.cache/*'}")
    get_ipython().run_line_magic('cd', '-q ~')
    print(f'{ui} uninstalled.')

def set_paths(ui):
    webui_paths = {
        'A1111': ('asd', 'extensions', 'embeddings', 'VAE', 'Stable-diffusion', 'Lora'),
        'Forge': ('forge', 'extensions', 'embeddings', 'VAE', 'Stable-diffusion', 'Lora'),
        'ComfyUI': ('ComfyUI', 'custom_nodes', 'embeddings', 'vae', 'checkpoints', 'loras')
    }

    if ui in webui_paths:
        webui_name, ext, emb, v, c, l = webui_paths[ui]
        webui = home / webui_name
        models = webui / 'models'
        webui_output = webui / 'outputs' if ui == 'A1111' else webui / 'output'
        extensions = webui / ext
        embeddings = models / emb if ui == 'ComfyUI' else webui / emb
        vae = models / v
        ckpt = models / c
        lora = models / l
        return webui, models, webui_output, extensions, embeddings, vae, ckpt, lora

if marked.exists():
    purge()

    ui = get_name(marked)
    webui, models, webui_output, extensions, embeddings, vae, ckpt, lora = set_paths(ui)

    controlnet_models = webui / 'asd/controlnet.py'
    forge_svd = tmp / 'svd' if ui == 'Forge' else None
    tmp_ckpt = tmp / 'ckpt'
    tmp_lora = tmp / 'lora'
    tempe()