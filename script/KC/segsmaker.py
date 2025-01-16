from IPython.display import clear_output
from IPython import get_ipython
from pathlib import Path
from KANDANG import HOMEPATH, VENVPATH, ENVNAME, TEMPPATH
from cupang import Tunnel as Alice_Zuberg
import subprocess
import argparse
import logging
import shlex
import json
import yaml
import time
import os

ROOT = Path.home()
MD = Path(HOMEPATH) / 'gutris1/marking.json'
py = Path(VENVPATH) / 'bin/python3'
pw = '82a973c04367123ae98bd9abdf80d9eda9b910e2'
cd = Path.cwd()

SyS = get_ipython().system
IRON = os.environ

def setENV(ui):
    if f'{VENVPATH}/bin' not in IRON['PATH']:
        IRON['PATH'] = f'{VENVPATH}/bin:' + IRON['PATH']

    if ui == 'SwarmUI':
        IRON['SWARMPATH'] = str(cd)
        IRON['SWARM_NO_VENV'] = 'true'

    IRON['PYTHONWARNINGS'] = 'ignore'

def Trashing():
    run = lambda cmd: subprocess.run(shlex.split(cmd), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    dirs1 = ["A1111", "Forge", "ComfyUI", "ReForge", "SwarmUI"]
    dirs2 = ["ckpt", "lora", "controlnet", "svd", "z123"]
    paths = [Path(HOMEPATH) / name for name in dirs1] + [Path(TEMPPATH) / name for name in dirs2]

    for path in paths:
        cmd = f"find {path} -type d -name .ipynb_checkpoints -exec rm -rf {{}} +"
        run(cmd)

def NGROK_auth(token):
    yml = ROOT / '.config/ngrok/ngrok.yml'

    if yml.exists():
        with open(yml, 'r') as f:
            current_token = yaml.safe_load(f).get('agent', {}).get('authtoken')
    else:
        current_token = None

    if current_token != token:
        SyS(f'ngrok config add-authtoken {token}')
        print()

def ZROK_enable(token):
    zrok_env = ROOT / '.zrok/environment.json'

    if zrok_env.exists():
        with open(zrok_env, 'r') as f:
            current_token = json.load(f).get('zrok_token')

        if current_token != token:
            SyS('zrok disable')
            SyS(f'zrok enable {token}')
            print()
    else:
        SyS(f'zrok enable {token}')
        print()

def webui_launch(launch_args, skip_comfyui_check, ngrok_token=None, zrok_token=None):
    config = json.load(MD.open('r'))
    ui = config.get('ui')

    setENV(ui)

    port = 7801 if ui == 'SwarmUI' else (8188 if ui == 'ComfyUI' else 7860)
    launcher = 'main.py' if ui == 'ComfyUI' else 'launch.py'

    if ui in ['A1111', 'Forge', 'ReForge']:
        timer = cd / "asd/pinggytimer.txt"
        end_time = int(time.time()) + 3600
        SyS(f"echo -n {end_time} > {timer}")

        launch_args += ' --enable-insecure-extension-access --disable-console-progressbars --theme dark'

        if ENVNAME == 'Kaggle':
            launch_args += f' --encrypt-pass={pw}'
        else:
            if '--share' not in launch_args:
                launch_args += ' --share'

    if ui == 'ComfyUI' and not skip_comfyui_check:
        SyS(f'{py} apotek.py')
        clear_output(wait=True)

    if ui == 'SwarmUI':
        SyS('pip install -q rembg')
        SyS('git pull -q')
        cmd = f"bash ./launch-linux.sh {launch_args}"
    else:
        cmd = f'{py} {launcher} {launch_args}'

    cloudflared = f'cl tunnel --url localhost:{port}'
    pinggy = f'ssh -o StrictHostKeyChecking=no -p 80 -R0:localhost:{port} a.pinggy.io'
    ngrok = f'ngrok http http://localhost:{port} --log stdout'
    zrok = f'zrok share public localhost:{port} --headless'

    Alice_Synthesis_Thirty = Alice_Zuberg(port)
    Alice_Synthesis_Thirty.logger.setLevel(logging.DEBUG)

    if not (ngrok_token or zrok_token):
        Alice_Synthesis_Thirty.add_tunnel(command=cloudflared, name='Cloudflared', pattern=r"[\w-]+\.trycloudflare\.com")
        Alice_Synthesis_Thirty.add_tunnel(command=pinggy, name='Pinggy', pattern=r"https://[\w-]+\.a\.free\.pinggy\.link")

    if ngrok_token:
        NGROK_auth(ngrok_token)
        Alice_Synthesis_Thirty.add_tunnel(command=ngrok, name='NGROK', pattern=r"https://[\w-]+\.ngrok-free\.app")

    if zrok_token:
        ZROK_enable(zrok_token)
        Alice_Synthesis_Thirty.add_tunnel(command=zrok, name='ZROK', pattern=r"https://[\w-]+\.share\.zrok\.io")

    with Alice_Synthesis_Thirty:
        SyS(cmd)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='nothing to read here')
    parser.add_argument('--skip-comfyui-check', action='store_true', help='Skip checking custom node dependencies for ComfyUI')
    parser.add_argument('--N', type=str, help='NGROK tunnel (pass a token or leave empty)', default=None)
    parser.add_argument('--Z', type=str, help='ZROK tunnel (pass a token or leave empty)', default=None)

    args, unknown = parser.parse_known_args()
    launch_args = ' '.join(unknown)

    try:
        Trashing()
        webui_launch(launch_args, args.skip_comfyui_check, args.N, args.Z)
    except KeyboardInterrupt:
        pass
