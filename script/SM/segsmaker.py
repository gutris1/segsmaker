from IPython.display import display, HTML, clear_output
from multiprocessing import Process, Condition, Value
from IPython import get_ipython
from ipywidgets import widgets
from pathlib import Path
import argparse
import logging
import json
import yaml
import sys

SyS = get_ipython().system

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
      <h1>{app.get('title', 'Unknown UI')}</h1>
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

def launching(ui, skip_comfyui_check=False):
    args = launch_args.value
    tunnel = tunnel_radio.value

    get_ipython().run_line_magic('run', 'venv.py')

    if ui in {'ComfyUI', 'SwarmUI'}:
        PY = '/tmp/venv-comfy-swarm/bin/python3'

        if ui == 'ComfyUI':
            port = 8188
            skip_comfyui_check or (SyS(f'{PY} apotek.py'), clear_output(wait=True))
        else:
            port = 7801

    else:
        port = 7860
        PY = '/tmp/python311/bin/python3' if ui == 'Forge-Classic' else '/tmp/venv/bin/python3'
        args += ' --enable-insecure-extension-access --disable-console-progressbars --theme dark'

    if cpu_cb.value:
        if ui == 'A1111':
            args += ' --use-cpu all --precision full --no-half --skip-torch-cuda-test'

        elif ui in {'Forge', 'ReForge', 'ReForge-old', 'Forge-Classic'}:
            args += ' --always-cpu --skip-torch-cuda-test'

        elif ui == 'ComfyUI':
            args += ' --cpu'

    configs = TUNNELS.get(tunnel)

    if not configs:
        return

    try:
        from cupang import Tunnel as Alice_Zuberg

        if configs['auth']:
            NGROK_ZROK(tunnel.lower())

        Alice_Synthesis_Thirty = Alice_Zuberg(port)
        Alice_Synthesis_Thirty.logger.setLevel(logging.DEBUG)

        Alice_Synthesis_Thirty.add_tunnel(
            command=configs['command'](port),
            name=configs['name'],
            pattern=configs['pattern']
        )

        with Alice_Synthesis_Thirty:
            SyS(f'{PY} Launcher.py {args}')

    except KeyboardInterrupt:
        pass

def waiting(con, ready):
    with con:
        while not ready.value:
            try:
                con.wait()
            except KeyboardInterrupt:
                print('')
                clear_output()
                sys.exit()

    load_config()
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
    setTimeout(() => {
      document.querySelectorAll('.launcher-tunnel-radio label').forEach(label => {
        const text = label.childNodes[0];
        if (text && text.nodeType === Node.TEXT_NODE) {
          const span = document.createElement('span');
          span.textContent = text.textContent.trim();
          label.replaceChild(span, text);
        }
      });
    }, 100);

    setTimeout(() => {
      const box = document.querySelector('.launcher-box'),
      inputs = document.querySelectorAll('.launcher-zrok-token input, .launcher-ngrok-token input, .launcher-args input');
      box && box.classList.add('loaded');
      inputs.forEach(el => el.spellcheck = false);
    }, 1000);
    </script>
    """))

UI_CFG = {
    'A1111': {
        'title': 'A1111',
        'args': '--xformers'
    },
    'Forge': {
        'title': 'Forge',
        'args': '--disable-xformers --opt-sdp-attention --cuda-stream'
    },
    'ReForge': {
        'title': 'ReForge',
        'args': '--xformers --cuda-stream'
    },
    'ReForge-old': {
        'title': 'ReForge old',
        'args': '--xformers --cuda-stream'
    },
    'Forge-Classic': {
        'title': 'Forge Classic',
        'args': '--xformers --cuda-stream --persistent-patches'
    },
    'Forge-Neo': {
        'title': 'Forge Neo',
        'args': '--xformers --cuda-stream'
    },
    'ComfyUI': {
        'title': 'ComfyUI',
        'args': '--dont-print-server --use-pytorch-cross-attention'
    },
    'SwarmUI': {
        'title': 'SwarmUI',
        'args': '--launch_mode none'
    }
}

TUNNELS = {
    'Pinggy': {
        'auth': False,
        'name': 'PINGGY',
        'command': lambda port: f'ssh -o StrictHostKeyChecking=no -p 80 -R0:localhost:{port} a.pinggy.io',
        'pattern': r'https://[\w-]+\.run\.pinggy-free\.link'
    },

    'ZROK2': {
        'auth': True,
        'name': 'ZROK2',
        'command': lambda port: f'zrok2 share public localhost:{port} --headless',
        'pattern': r'[\w-]+\.shares\.zrok\.io'
    },

    'NGROK': {
        'auth': True,
        'name': 'NGROK',
        'command': lambda port: f'ngrok http http://localhost:{port} --log stdout',
        'pattern': r'https://[\w-]+\.ngrok-free\.[\w.-]+'
    }
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
]:
    w.add_class(c)

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
