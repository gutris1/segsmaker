from IPython.display import clear_output
from IPython import get_ipython
from pathlib import Path
from KANDANG import HOMEPATH, VENVPATH
from cupang import Tunnel as Alice_Zuberg
import json, logging, sys, argparse

MD = Path(HOMEPATH) / 'gutris1/marking.json'
py = Path(VENVPATH) / 'bin/python3'
pw = '82a973c04367123ae98bd9abdf80d9eda9b910e2'

def shut_up(launch_args, skip_comfyui_check):
    config = json.load(MD.open('r')) if MD.exists() else {}
    ui = config.get('ui')

    port = 8188 if ui == 'ComfyUI' else 7860
    launcher = 'main.py' if ui == 'ComfyUI' else 'launch.py'

    if ui != 'ComfyUI':
        launch_args += f' --enable-insecure-extension-access --disable-console-progressbars --theme dark --encrypt-pass={pw}'

    if ui == 'ComfyUI' and not skip_comfyui_check:
        get_ipython().system(f'{py} apotek.py')
        clear_output(wait=True)

    tunnel = f'cl tunnel --url localhost:{port}'

    Alice_Synthesis_Thirty = Alice_Zuberg(port)
    Alice_Synthesis_Thirty.logger.setLevel(logging.DEBUG)
    Alice_Synthesis_Thirty.add_tunnel(command=tunnel, name='Cloudflared', pattern=r"[\w-]+\.trycloudflare\.com")

    with Alice_Synthesis_Thirty:
        cmd = f'{py} {launcher} {launch_args}'
        get_ipython().system(cmd)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='nothing to read here')
    parser.add_argument('--skip-comfyui-check', action='store_true', help='Skip checking custom node dependencies for ComfyUI')

    args, unknown = parser.parse_known_args()
    launch_args = ' '.join(unknown)

    try:
        shut_up(launch_args, args.skip_comfyui_check)
    except KeyboardInterrupt:
        pass
