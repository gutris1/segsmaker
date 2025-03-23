from IPython.core.magic import register_line_magic
from IPython import get_ipython
from pathlib import Path
from nenen88 import tempe
import json
import os

SM = None

try:
    from KANDANG import TEMPPATH, HOMEPATH
    TMP = Path(TEMPPATH)
    HOME = Path(HOMEPATH)
    SM = False
except ImportError:
    TMP = Path('/tmp')
    HOME = Path.home()
    SM = True

marked = Path(__file__).parent / 'marking.json'

SyS = get_ipython().system
CD = os.chdir

def purgeVAR():
    var_list = [
        'WebUI', 'Models', 'WebUI_Output', 'Extensions', 'Embeddings', 'UNET', 'CLIP',
        'VAE', 'CKPT', 'LORA', 'TMP_CKPT', 'TMP_LORA', 'Forge_SVD', 'Controlnet_Widget', 'Upscalers'
    ]
    for var in var_list:
        if var in globals():
            del globals()[var]

def getWebUIName(path):
    return json.load(open(path, 'r')).get('ui', None)

def setWebUIVAR(ui):
    path_list = {
        'A1111': ('A1111', 'extensions', 'embeddings', 'VAE', 'Stable-diffusion', 'Lora', 'ESRGAN'),
        'Forge': ('Forge', 'extensions', 'embeddings', 'VAE', 'Stable-diffusion', 'Lora', 'ESRGAN'),
        'ComfyUI': ('ComfyUI', 'custom_nodes', 'embeddings', 'vae', 'checkpoints', 'loras', 'upscale_models'),
        'ReForge': ('ReForge', 'extensions', 'embeddings', 'VAE', 'Stable-diffusion', 'Lora', 'ESRGAN'),
        'FaceFusion': ('FaceFusion', None, None, None, None, None, None),
        'SDTrainer': ('SDTrainer', None, None, 'VAE', 'sd-models', None, None),
        'SwarmUI': ('SwarmUI', 'Extensions', 'Embeddings', 'VAE', 'Stable-Diffusion', 'Lora', 'upscale_models')
    }

    U, extension, embed, vae, ckpt, lora, upscaler = path_list[ui]
    W = HOME / U if U else None
    M = W / ('Models' if ui == 'SwarmUI' else 'models') if W else None
    EXT = W / 'src' / extension if ui == 'SwarmUI' and extension else W / extension if extension else None
    E = (
        M / embed if ui in ['ComfyUI', 'SwarmUI'] else
        W / embed if ui in ['A1111', 'Forge', 'ReForge'] else
        None
    )
    V = M / vae if M and vae else None
    C = M / ckpt if M and ckpt else None
    L = M / lora if M and lora else None
    UPS = M / upscaler if ui not in ['FaceFusion', 'SDTrainer'] else None
    O = W / (
        'Output' if ui == 'SwarmUI' else 'output' if ui in ['ComfyUI', 'SDTrainer'] else 'outputs'
    ) if W else None

    return W, M, O, EXT, E, V, C, L, UPS

if SM:
    @register_line_magic
    def clear_output_images(line):
        ui = getWebUIName(marked)
        _, _, output, _, _, _, _, _, _ = setWebUIVAR(ui)
        SyS(f"rm -rf {output}/* {HOME / '.cache/*'}")
        CD(HOME)
        print(f'{ui} outputs cleared.')

    @register_line_magic
    def uninstall_webui(line):
        ui = getWebUIName(marked)
        webui, _, _, _, _, _, _, _, _ = setWebUIVAR(ui)
        SyS(f"rm -rf {webui} {HOME / 'tmp'} {HOME / '.cache/*'}")
        print(f'{ui} uninstalled.')
        CD(HOME)
        get_ipython().kernel.do_shutdown(True)

if marked.exists():
    purgeVAR()

    ui = getWebUIName(marked)
    WebUI, Models, WebUI_Output, Extensions, Embeddings, VAE, CKPT, LORA, Upscalers = setWebUIVAR(ui)

    Controlnet_Widget = WebUI / 'asd/controlnet.py' if WebUI else None
    Forge_SVD = TMP / 'svd' if ui in ['Forge', 'ReForge'] else None
    UNET = TMP / 'unet' if ui in ['Forge', 'ComfyUI', 'SwarmUI'] else None
    CLIP = TMP / 'clip' if ui in ['Forge', 'ComfyUI', 'SwarmUI'] else None
    TMP_CKPT = TMP / 'ckpt'
    TMP_LORA = TMP / 'lora'

    tempe()
