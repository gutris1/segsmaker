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
    l = [
        'WebUI', 'Models', 'WebUI_Output', 'Extensions', 'Embeddings', 'UNET', 'CLIP', 'VAE',
        'CKPT', 'LORA', 'TMP_CKPT', 'TMP_LORA', 'Forge_SVD', 'Controlnet_Widget', 'Upscalers'
    ]
    for v in l:
        if v in globals(): del globals()[v]

def getWebUIName(path):
    return json.load(open(path, 'r')).get('ui', None)

def setWebUIVAR(ui):
    default = ('extensions', 'embeddings', 'VAE', 'Stable-diffusion', 'Lora', 'ESRGAN')

    maps = {
        'A1111': default,
        'Forge': default,
        'ReForge': default,
        'Forge-Classic': default,
        'ComfyUI': ('custom_nodes', 'embeddings', 'vae', 'checkpoints', 'loras', 'upscale_models'),
        'SwarmUI': ('Extensions', 'Embeddings', 'VAE', 'Stable-Diffusion', 'Lora', 'upscale_models'),
        'FaceFusion': (None,) * 6,
        'SDTrainer': (None, None, 'VAE', 'sd-models', None, None)
    }

    ext, embed, vae, ckpt, lora, upscaler = maps.get(ui, (None,) * 6)

    WebUI = HOME / ui
    Models = WebUI / ('Models' if ui == 'SwarmUI' else 'models')
    WebUI_Output = WebUI / ('Output' if ui == 'SwarmUI' else 'output' if ui in ['Forge-Classic', 'ComfyUI', 'SDTrainer'] else 'outputs')
    Extensions = (WebUI / 'src' / ext if ui == 'SwarmUI' and ext else WebUI / ext if ext else None)
    Embeddings = (Models / embed if ui in ['Forge-Classic', 'ComfyUI', 'SwarmUI'] else WebUI / embed if embed else None)
    VAE = Models / vae if vae else None
    CKPT = Models / ckpt if ckpt else None
    LORA = Models / lora if lora else None
    Upscalers = Models / upscaler if upscaler and ui not in ['FaceFusion', 'SDTrainer'] else None

    return WebUI, Models, WebUI_Output, Extensions, Embeddings, VAE, CKPT, LORA, Upscalers

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
