from IPython.display import display, HTML, clear_output
from multiprocessing import Process, Condition, Value
from IPython import get_ipython
from ipywidgets import widgets
from pathlib import Path
import subprocess
import argparse
import logging
import shlex
import json
import yaml
import time
import sys
import os

SyS = get_ipython().system
iRON = os.environ

HOME = Path.home()
SRC = HOME / '.gutris1'
CSS = SRC / 'segsmaker.css'
MARK = SRC / 'marking.json'
IMG = SRC / 'loading.png'

R = '\033[31m'
P = '\033[38;5;135m'
RST = '\033[0m'
ERR = f'{P}[{RST}{R}ERROR{RST}{P}]{RST}'

def load_css():
    display(HTML(f'<style>{CSS.read_text()}</style>'))

def load_config():
    global ui

    gpu = Path('/proc/driver/nvidia').exists()
    config = json.loads(MARK.read_text()) if MARK.exists() else {}

    ui = config.get('ui')
    tunnel = config.get('tunnel')
    app = UI_CFG.get(ui, {})

    zrok_token.value = config.get('zrok_token', '')
    ngrok_token.value = config.get('ngrok_token', '')

    launch_args.value = config.get('launch_args') or app.get('args', '')

    if tunnel not in TUNNELS:
        tunnel = 'Pinggy'
        config['tunnel'] = tunnel
        MARK.write_text(json.dumps(config, indent=4))

    tunnel_radio.value = tunnel

    cpu_cb.value = not gpu and config.get('cpu_usage', False)
    cpu_cb.layout.display = 'none' if gpu or ui == 'SwarmUI' else 'block'

    title.value = f"""
    <div class='launcher-title'>
      {''.join(f'<span>{t}</span>' for t in app.get('title', 'Unknown').split())}
    </div>
    """

def save_config():
    config = json.loads(MARK.read_text()) if MARK.exists() else {}

    config.update({
        'zrok_token': zrok_token.value,
        'ngrok_token': ngrok_token.value,
        'launch_args': launch_args.value,
        'tunnel': tunnel_radio.value,
        'cpu_usage': cpu_cb.value
    })

    MARK.write_text(json.dumps(config, indent=4))

def NGROK_ZROK(T):
    P = {
        'zrok2': {
            'B': HOME / '.zrok2/zrok2',
            'C': HOME / '.zrok2/environment.json',
            't': zrok_token.value
        },
        'ngrok': {
            'B': HOME / '.ngrok/ngrok',
            'C': HOME / '.config/ngrok.yml',
            't': ngrok_token.value
        }
    }

    p = P[T]
    B, C, t = p['B'], p['C'], p['t']

    if not t:
        print(f'{ERR}: {T.upper()} Token is empty'); sys.exit()
    if not B.exists():
        print(f'{ERR}: {T.upper()} is not installed'); sys.exit()

    E = f'{T} enable {t}' if T == 'zrok2' else f'{T} config add-authtoken {t}'

    if C.exists():
        ct = None
        if T == 'zrok2':
            ct = json.loads(C.read_text()).get('zrok_token')
        elif T == 'ngrok':
            ct = yaml.safe_load(C.read_text()).get('agent', {}).get('authtoken')

        if ct != t:
            if T == 'zrok2':
                SyS(f'{T} disable')
            SyS(E); print()
    else:
        SyS(E); print()

def setENV(ui):
    app = UI_CFG[ui]

    L = '/home/studio-lab-user/.conda/envs/default/lib/libtcmalloc_minimal.so.4'
    D = '/home/studio-lab-user/.conda/envs/default/lib'

    if app.get('ld'):
        iRON['LD_LIBRARY_PATH'] = (D + ':' + iRON.get('LD_LIBRARY_PATH', ''))

    if app.get('cm'):
        iRON.pop('MPLBACKEND', None)

    for k, v in app.get('env', {}).items():
        iRON[k] = v() if callable(v) else v

    if L not in iRON.get('LD_PRELOAD', ''):
        iRON['LD_PRELOAD'] = L

    if app['lib'] not in iRON.get('LD_LIBRARY_PATH', ''):
        iRON['LD_LIBRARY_PATH'] = (app['lib'] + ':' + iRON.get('LD_LIBRARY_PATH', ''))

    if app['bin'] not in iRON.get('PATH', ''):
        iRON['PATH'] = (app['bin'] + ':' + iRON.get('PATH', ''))

    iRON['PYTHONWARNINGS'] = 'ignore'

def launching(ui, skip_comfyui_check=False):
    from cupang import Tunnel as Alice

    args = '' if cpu_cb.value else launch_args.value
    tunnel = tunnel_radio.value

    get_ipython().run_line_magic('run', 'venv.py')

    app = UI_CFG[ui]

    py = app['py']
    port = app.get('port', 7860)

    setENV(ui)

    t = TUNNELS.get(tunnel)
    if t['a']: NGROK_ZROK(tunnel.lower())

    Zuberg = Alice(port)
    Zuberg.logger.setLevel(logging.DEBUG)
    Zuberg.add_tunnel(command=t['c'](port), name=t['n'], pattern=t['p'])

    if ui == 'SwarmUI':
        SyS('git pull -q')
        launcher = 'bash ./launch-linux.sh'

    else:
        if ui == 'ComfyUI':
            if not skip_comfyui_check: SyS(f'{py} apotek.py'); clear_output(wait=True)
            launcher = f'{py} main.py'

        else:
            iRON.setdefault('IIB_ACCESS_CONTROL', 'disable')
            iRON.setdefault('IIB_SKIP_OPTIONAL_DEPS', '1')

            args += ' --enable-insecure-extension-access --disable-console-progressbars --theme dark'

            Path('asd/pinggytimer.txt').write_text(str(int(time.time()) + 3600))

            if ui == 'Forge':
                ft = Path('FT.txt')
                if not ft.exists(): SyS(f"{app['py']} -m pip uninstall -qy transformers"); ft.write_text('tf')

            launcher = f'{py} launch.py'

    if cpu_cb.value: args += f" {app.get('cpu', '')}"

    with Zuberg:
        SyS(f'{launcher} {args}')

def waiting(con, ready):
    with con:
        while not ready.value:
            try:
                con.wait()
            except KeyboardInterrupt:
                print(''); clear_output(); sys.exit()

    launching(ui, skip_comfyui_check=args.skip_comfyui_check)

def launch(b):
    global ui, zrok_token, ngrok_token, launch_args, tunnel_radio

    launch_panel.close()
    save_config()

    with con:
        ready.value = True
        con.notify()

def exit(b):
    launch_panel.close()

def launcher_loaded():
    display(HTML("""
    <script>
    setTimeout(() => {{
      document.querySelectorAll('.launcher-tunnel-radio label').forEach(label => {{
        const text = label.childNodes[0];
        if (text && text.nodeType === Node.TEXT_NODE) {{
          const span = document.createElement('span');
          span.textContent = text.textContent.trim();
          label.replaceChild(span, text);
        }}
      }});
    }}, 100);
    
    setTimeout(() => {{
      const box = document.querySelector('.launcher-box'),
      tokens = document.querySelectorAll('.launcher-zrok-token input, .launcher-ngrok-token input, .launcher-args input');
    
      box && box.classList.add('loaded');
      tokens.forEach(el => el.spellcheck = false);
    }}, 400);
    </script>
    """))

TUNNELS = {
    'Pinggy': {
        'a': False,
        'n': 'PINGGY',
        'c': lambda port: f'ssh -o StrictHostKeyChecking=no -p 80 -R0:localhost:{port} a.pinggy.io',
        'p': r'https://[\w-]+\.run\.pinggy-free\.link'
    },

    'ZROK2': {
        'a': True,
        'n': 'ZROK2',
        'c': lambda port: f'zrok2 share public localhost:{port} --headless',
        'p': r'[\w-]+\.shares\.zrok\.io'
    },

    'NGROK': {
        'a': True,
        'n': 'NGROK',
        'c': lambda port: f'ngrok http http://localhost:{port} --log stdout',
        'p': r'https://[\w-]+\.ngrok-free\.[\w.-]+'
    }
}

UI_CFG = {
    'A1111': {
        'title': 'A1111',
        'args': '--xformers',
        'py': '/tmp/venv/bin/python3',
        'lib': '/tmp/venv/lib',
        'bin': '/tmp/venv/bin',
        'cpu': '--use-cpu all --precision full --no-half --skip-torch-cuda-test',
    },

    'Forge': {
        'title': 'Forge',
        'args': '--disable-xformers --opt-sdp-attention --cuda-stream',
        'py': '/tmp/venv/bin/python3',
        'lib': '/tmp/venv/lib',
        'bin': '/tmp/venv/bin',
        'cpu': '--always-cpu --skip-torch-cuda-test',
    },

    'ReForge': {
        'title': 'ReForge',
        'args': '--xformers --cuda-stream',
        'py': '/tmp/venv/bin/python3',
        'lib': '/tmp/venv/lib',
        'bin': '/tmp/venv/bin',
        'cpu': '--always-cpu --skip-torch-cuda-test',
    },

    'ReForge-old': {
        'title': 'ReForge old',
        'args': '--xformers --cuda-stream',
        'py': '/tmp/venv/bin/python3',
        'lib': '/tmp/venv/lib',
        'bin': '/tmp/venv/bin',
        'cpu': '--always-cpu --skip-torch-cuda-test',
    },

    'Forge-Classic': {
        'title': 'Forge Classic',
        'args': '--xformers --cuda-stream --persistent-patches',
        'py': '/tmp/python311/bin/python3',
        'lib': '/tmp/python311/lib',
        'bin': '/tmp/python311/bin',
        'cpu': '--always-cpu --skip-torch-cuda-test',
        'ld': True,
    },

    'Forge-Neo': {
        'title': 'Forge Neo',
        'args': '--xformers --cuda-stream',
        'py': '/tmp/NEO/bin/python3',
        'lib': '/tmp/NEO/lib',
        'bin': '/tmp/NEO/bin',
        'cpu': '--cpu --skip-torch-cuda-test',
        'ld': True,
        'cm': True,
    },

    'ComfyUI': {
        'title': 'ComfyUI',
        'args': '--dont-print-server --use-pytorch-cross-attention',
        'py': '/tmp/venv-comfy-swarm/bin/python3',
        'lib': '/tmp/venv-comfy-swarm/lib',
        'bin': '/tmp/venv-comfy-swarm/bin',
        'port': 8188,
        'cpu': '--cpu',
    },

    'SwarmUI': {
        'title': 'SwarmUI',
        'args': '--launch_mode none',
        'py': '/tmp/venv-comfy-swarm/bin/python3',
        'lib': '/tmp/venv-comfy-swarm/lib',
        'bin': '/tmp/venv-comfy-swarm/bin',
        'port': 7801,
        'env': {'SWARMPATH': lambda: str(Path.cwd()), 'SWARM_NO_VENV': 'true'},
    },
}

tunnel_radio = widgets.RadioButtons(options=list(TUNNELS))

zrok_token = widgets.Text(placeholder='ZROK2 Token')
ngrok_token = widgets.Text(placeholder='NGROK Token')
token_box = widgets.VBox([zrok_token, ngrok_token])

title = widgets.HTML()
top_row = widgets.HBox([tunnel_radio, token_box, title])

launch_args = widgets.Text(placeholder='Launch Arguments List')

launch_button = widgets.Button(description='Launch')
exit_button = widgets.Button(description='Exit')
cpu_cb = widgets.Checkbox(value=False, description='CPU')
bottom_row = widgets.HBox([exit_button, cpu_cb, launch_button])

launch_panel = widgets.Box([top_row, launch_args, bottom_row])

for w, c in [
    (launch_panel, 'launcher-box'),
    (title, 'launcher-webui-title'),
    (top_row, 'launcher-top-row'),
    (bottom_row, 'launcher-bottom-row'),
    (cpu_cb, 'launcher-cpu-cb'),
    (tunnel_radio, 'launcher-tunnel-radio'),
    (token_box, 'launcher-token-box'),
    (zrok_token, 'launcher-zrok-token'),
    (ngrok_token, 'launcher-ngrok-token'),
    (launch_args, 'launcher-args'),
    (launch_button, 'launcher-button'),
    (exit_button, 'launcher-button')
]: w.add_class(c)

parser = argparse.ArgumentParser()
parser.add_argument('--skip-comfyui-check', action='store_true', help='Skip checking custom node dependencies for ComfyUI')
parser.add_argument('--skip-widget', action='store_true', help='Skip displaying the widget')
args, unknown = parser.parse_known_args()

con = Condition()
ready = Value('b', False)

if __name__ == '__main__':
    try:
        load_config()

        if args.skip_widget:
            launching(ui, skip_comfyui_check=args.skip_comfyui_check)
        else:
            load_css()
            launcher_loaded()
            display(launch_panel)

            launch_button.on_click(launch)
            exit_button.on_click(exit)

            Process(target=waiting, args=(con, ready)).start()
    except KeyboardInterrupt:
        pass
