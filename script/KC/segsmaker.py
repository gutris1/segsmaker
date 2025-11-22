from KANDANG import HOMEPATH, ENVNAME, TEMPPATH
from cupang import Tunnel as Alice_Zuberg
from IPython.display import clear_output
from IPython import get_ipython
from pathlib import Path
import subprocess
import argparse
import logging
import shlex
import json
import yaml
import time
import os

ROOT = Path.home()
CWD = Path.cwd()
PW = '82a973c04367123ae98bd9abdf80d9eda9b910e2'

SyS = get_ipython().system
iRON = os.environ

iRON['PYTHONWARNINGS'] = 'ignore'

def Trashing():
    run = lambda cmd: subprocess.run(shlex.split(cmd), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    dirs1 = ['A1111', 'Forge', 'ReForge', 'Forge-Classic', 'Forge-Neo','ComfyUI', 'SwarmUI']
    dirs2 = ['ckpt', 'lora', 'controlnet', 'svd', 'z123']

    paths = [Path(HOMEPATH) / name for name in dirs1] + [Path(TEMPPATH) / name for name in dirs2]
    for path in paths:
        cmd = f'find {path} -type d -name .ipynb_checkpoints -exec rm -rf {{}} +'
        run(cmd)

def NGROK_auth(token):
    yml = ROOT / '.config/ngrok/ngrok.yml'

    if yml.exists():
        current_token = yaml.safe_load(yml.read_text()).get('agent', {}).get('authtoken')
    else:
        current_token = None

    if current_token != token:
        SyS(f'ngrok config add-authtoken {token}')
        print()

def ZROK_enable(token):
    zrok_env = ROOT / '.zrok/environment.json'

    if zrok_env.exists():
        current_token = json.loads(zrok_env.read_text()).get('zrok_token')

        if current_token != token:
            SyS('zrok disable')
            SyS(f'zrok enable {token}')
            print()
    else:
        SyS(f'zrok enable {token}')
        print()

def webui_launch(launch_args, skip_comfyui_check, ngrok_token=None, zrok_token=None):
    ui = json.load((Path(HOMEPATH) / 'gutris1/marking.json').open('r')).get('ui')

    if ui in ['A1111', 'Forge', 'ReForge', 'Forge-Classic', 'Forge-Neo']:
        port = 7860
        SyS(f"echo -n {int(time.time()) + 3600} > {CWD / 'asd/pinggytimer.txt'}")
        launch_args += ' --enable-insecure-extension-access --disable-console-progressbars --theme dark'

        if '--share' in launch_args: launch_args = launch_args.replace('--share', '')
        if ENVNAME == 'Kaggle': launch_args += f' --encrypt-pass={PW}'
        iRON.setdefault('IIB_ACCESS_CONTROL', 'disable')

        if ui == 'Forge' and not (CWD / 'FT.txt').exists():
            SyS('pip uninstall -qy transformers')
            (CWD / 'FT.txt').write_text('blyat')

        cmd = f'python3 launch.py {launch_args}'

    elif ui in ['ComfyUI', 'SwarmUI']:
        if ui == 'ComfyUI':
            port = 8188
            skip_comfyui_check or (SyS('python3 apotek.py'), clear_output(wait=True))
            cmd = f'python3 main.py {launch_args}'

        else:
            SyS('pip install -q "pydantic>=1.9.0,<2.0.0"')
            port = 7801
            iRON['SWARMPATH'] = str(CWD)
            iRON['SWARM_NO_VENV'] = 'true'
            cmd = f'bash ./launch-linux.sh {launch_args}'

    cloudflared = f'cl tunnel --url localhost:{port}'
    pinggy = f'ssh -o StrictHostKeyChecking=no -p 80 -R0:localhost:{port} a.pinggy.io'
    ngrok = f'ngrok http http://localhost:{port} --log stdout'
    zrok = f'zrok share public localhost:{port} --headless'
    gradio = f'gradio-tun {port}'

    Alice_Synthesis_Thirty = Alice_Zuberg(port)
    Alice_Synthesis_Thirty.logger.setLevel(logging.DEBUG)
    Add = lambda command, name, pattern: Alice_Synthesis_Thirty.add_tunnel(command=command, name=name, pattern=pattern)

    if not (ngrok_token or zrok_token):
        Add(gradio, 'Gradio', r'https://[\w-]+\.gradio\.live')
        Add(pinggy, 'Pinggy', r'https://[\w-]+\.a\.free\.pinggy\.link')
        Add(cloudflared, 'Cloudflared', r'[\w-]+\.trycloudflare\.com')

    if ngrok_token:
        NGROK_auth(ngrok_token)
        Add(ngrok, 'NGROK', r'https://[\w-]+\.ngrok-free\.[\w.-]+')

    if zrok_token:
        ZROK_enable(zrok_token)
        Add(zrok, 'ZROK', r'https://[\w-]+\.share\.zrok\.[\w.-]+')

    with Alice_Synthesis_Thirty:
        SyS(cmd)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='nothing to read here')
    parser.add_argument('--skip-comfyui-check', action='store_true', help='Skip checking custom node dependencies for ComfyUI')
    parser.add_argument('--N', type=str, help='NGROK tunnel (pass a token or do nothing)', default=None)
    parser.add_argument('--Z', type=str, help='ZROK tunnel (pass a token or do nothing)', default=None)

    args, unknown = parser.parse_known_args()
    launch_args = ' '.join(unknown)

    try:
        Trashing()
        webui_launch(launch_args, args.skip_comfyui_check, args.N, args.Z)
    except KeyboardInterrupt:
        pass
