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
    d = ('extensions', 'embeddings', 'VAE', 'Stable-diffusion', 'Lora', 'ESRGAN', None)

    F = {
        'A1111': d,
        'Forge': d,

        'ReForge': (
            'extensions', 'embeddings', 'VAE',
            'Stable-diffusion', 'Lora', 'ESRGAN',
            'text_encoders'
        ),

        'ReForge-old': d,
        'Forge-Classic': d,

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
            'text_encoders'
        )
    }

    ext, embed, vae, ckpt, lora, ups, te = F[ui]

    WebUI = HOME / ui
    Models = WebUI / ('Models' if ui == 'SwarmUI' else 'models')

    WebUI_Output = WebUI / (
        'Output' if ui == 'SwarmUI'
        else 'output' if ui in ['Forge-Classic', 'Forge-Neo', 'ComfyUI']
        else 'outputs'
    )

    Extensions = (WebUI / 'src' / ext) if ui == 'SwarmUI' else (WebUI / ext)
    Embeddings = Models / embed

    VAE = Models / vae
    CKPT = Models / ckpt
    LORA = Models / lora
    Upscalers = Models / ups
    TE = Models / te if te else None

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
