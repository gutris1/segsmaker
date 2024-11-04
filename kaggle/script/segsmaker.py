import json, logging, sys
from pathlib import Path
from IPython import get_ipython
from cupang import Tunnel as Alice_Zuberg
from KANDANG import HOMEPATH

MARKED = Path(HOMEPATH) / 'gutris1/marking.json'
pw = '82a973c04367123ae98bd9abdf80d9eda9b910e2'

def shut_up(launch_args):
    config = json.load(MARKED.open('r')) if MARKED.exists() else {}
    ui = config.get('ui')

    port = 8188 if ui == 'ComfyUI' else 7860
    launch = 'main.py' if ui == 'ComfyUI' else 'launch.py'

    if ui != 'ComfyUI':
        launch_args += f' --enable-insecure-extension-access --disable-console-progressbars --theme dark --encrypt-pass={pw}'

    tunnel = f'cl tunnel --url localhost:{port}'

    Alice_Synthesis_Thirty = Alice_Zuberg(port)
    Alice_Synthesis_Thirty.logger.setLevel(logging.DEBUG)
    Alice_Synthesis_Thirty.add_tunnel(command=tunnel, name='Cloudflared', pattern=r"[\w-]+\.trycloudflare\.com")

    with Alice_Synthesis_Thirty:
        cmd = f'/kaggle/venv/bin/python3 {launch} {launch_args}'
        get_ipython().system(cmd)

if __name__ == '__main__':
    launch_args = ' '.join(sys.argv[1:])

    try:
        shut_up(launch_args)
    except KeyboardInterrupt:
        pass
