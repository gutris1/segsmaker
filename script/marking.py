from IPython.core.magic import register_line_magic
from IPython import get_ipython
from pathlib import Path
import json
import os

from _segsmaker_ import HOME, SRC
from nenen88 import tempe

CD = os.chdir
iRON = os.environ
SyS = get_ipython().system

TMP = Path('/tmp')
MARK = SRC / 'marking.json'

ui = json.load(MARK.open()).get('ui')

SSL = 'SAGEMAKER_INTERNAL_IMAGE_URI' in iRON

def _del():
    l = [
        'WebUI', 'Models', 'WebUI_Output', 'Extensions', 'Embeddings', 'UNET', 'CLIP', 'VAE', 'TE',
        'CKPT', 'LORA', 'TMP_CKPT', 'TMP_LORA', 'Forge_SVD', 'Controlnet_Widget', 'Upscalers'
    ]
    for v in l:
        if v in globals(): del globals()[v]


def _var():
    default = ('extensions', 'embeddings', 'VAE', 'Stable-diffusion', 'Lora', 'ESRGAN', None)

    maps = {
        'A1111': default,
        'Forge': default,

        'ReForge': (
            'extensions', 'embeddings', 'VAE',
            'Stable-diffusion', 'Lora', 'ESRGAN',
            'text_encoders'
        ),

        'ReForge-old': default,
        'Forge-Classic': default,

        'Forge-Neo': (
            'extensions', 'embeddings', 'VAE',
            'Stable-diffusion', 'Lora', 'ESRGAN',
            'text_encoder'
        ),

        'ComfyUI': (
            'custom_nodes', 'embeddings', 'vae',
            'checkpoints', 'loras', 'upscale_models',
            'text_encoders'
        ),

        'SwarmUI': (
            'Extensions', 'Embeddings', 'VAE',
            'Stable-Diffusion', 'Lora', 'upscale_models',
            None
        )
    }

    ext, embed, vae, ckpt, lora, upscaler, te = maps.get(ui, (None,) * 7)

    WebUI = HOME / ui
    Models = WebUI / ('Models' if ui == 'SwarmUI' else 'models')

    WebUI_Output = WebUI / (
        'Output' if ui == 'SwarmUI'
        else 'output' if ui in ['Forge-Classic', 'Forge-Neo', 'ComfyUI', 'SDTrainer']
        else 'outputs'
    )

    Extensions = (
        WebUI / 'src' / ext
        if ui == 'SwarmUI' and ext
        else WebUI / ext if ext
        else None
    )

    Embeddings = (
        Models / embed
        if ui in ['Forge-Classic', 'Forge-Neo', 'ComfyUI', 'SwarmUI']
        else WebUI / embed if embed
        else None
    )

    VAE = Models / vae if vae else None
    CKPT = Models / ckpt if ckpt else None
    LORA = Models / lora if lora else None

    Upscalers = Models / upscaler if upscaler and ui else None

    TE = Models / te if te and ui in ['Forge-Neo', 'ComfyUI'] else None

    return WebUI, Models, WebUI_Output, Extensions, Embeddings, VAE, CKPT, LORA, Upscalers, TE

if SSL:
    @register_line_magic
    def clear_output_images(line):
        _, _, output, _, _, _, _, _, _, _ = _var()
        SyS(f'rm -rf {output}/* ~/.cache/*')
        print(f'{ui} outputs cleared.')
        CD(HOME)

    @register_line_magic
    def uninstall_webui(line):
        SyS(f'rm -rf ~/{ui} ~/tmp ~/.cache/*')
        print(f'{ui} uninstalled.')
        CD(HOME)

        from util import restart_kernel
        restart_kernel()

if ui:
    _del()

    WebUI, Models, WebUI_Output, Extensions, Embeddings, VAE, CKPT, LORA, Upscalers, TE = _var()

    Controlnet_Widget = WebUI / 'asd/controlnet.py' if WebUI else None

    Forge_SVD = TMP / 'svd' if ui in ['Forge', 'ReForge', 'ReForge-old'] else None
    UNET = TMP / 'unet' if ui in ['Forge', 'ComfyUI', 'SwarmUI'] else None
    CLIP = TMP / 'clip' if ui in ['Forge', 'ComfyUI', 'SwarmUI'] else None

    TMP_CKPT = TMP / 'ckpt'
    TMP_LORA = TMP / 'lora'

    tempe()
