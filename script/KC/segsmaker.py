from IPython.display import clear_output
from IPython import get_ipython
from pathlib import Path
from KANDANG import HOMEPATH, VENVPATH
from cupang import Tunnel as Alice_Zuberg
import json, logging, sys, argparse, os

MD = Path(HOMEPATH) / 'gutris1/marking.json'
py = Path(VENVPATH) / 'bin/python3'
pw = '82a973c04367123ae98bd9abdf80d9eda9b910e2'
cd = Path.cwd()

def shut_up(launch_args, skip_comfyui_check):
    config = json.load(MD.open('r'))
    ui = config.get('ui')

    port = 7801 if ui == 'SwarmUI' else (8188 if ui == 'ComfyUI' else 7860)
    launcher = 'main.py' if ui == 'ComfyUI' else 'launch.py'

    if ui in ['A1111', 'Forge', 'ReForge']:
        launch_args += f' --enable-insecure-extension-access --disable-console-progressbars --theme dark --encrypt-pass={pw}'

    if ui == 'ComfyUI' and not skip_comfyui_check:
        get_ipython().system(f'{py} apotek.py')
        clear_output(wait=True)

    tunnel = f'cl tunnel --url localhost:{port}'
    os.environ['PATH'] = f'{VENVPATH}/bin:' + os.environ['PATH']
    os.environ["PYTHONWARNINGS"] = "ignore"

    if ui == 'SwarmUI':
        os.environ['SWARMPATH'] = str(cd)
        os.environ['SWARM_NO_VENV'] = 'true'
        get_ipython().system('pip install -q rembg')
        get_ipython().system('git pull -q')
        cmd = f"bash ./launch-linux.sh {launch_args}"
    else:
        cmd = f'{py} {launcher} {launch_args}'

    Alice_Synthesis_Thirty = Alice_Zuberg(port)
    Alice_Synthesis_Thirty.logger.setLevel(logging.DEBUG)
    Alice_Synthesis_Thirty.add_tunnel(command=tunnel, name='Cloudflared', pattern=r"[\w-]+\.trycloudflare\.com")

    with Alice_Synthesis_Thirty:
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
