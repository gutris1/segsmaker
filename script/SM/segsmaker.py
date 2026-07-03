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

from cupang import Tunnel as Alice
from ssl_uid import UID

R = '\033[31m'
P = '\033[38;5;135m'
RST = '\033[0m'
ERR = f'{P}[{RST}{R}ERROR{RST}{P}]{RST}'

SyS = get_ipython().system
iRON = os.environ

HOME = Path.home()
SRC = HOME / '.gutris1'
CSS = SRC / 'segsmaker.css'
MARK = SRC / 'marking.json'
IMG = SRC / 'loading.png'

j = json.loads(MARK.read_text())

def load_css():
    display(HTML(f'<style>{CSS.read_text()}</style>'))

def save_config():
    j.update({
        'zrok_token': zrok_token.value,
        'ngrok_token': ngrok_token.value,
        'launch_args': launch_args.value,
        'tunnel': tunnel_radio.value,
        'cpu_usage': cpu_cb.value
    })

    MARK.write_text(json.dumps(j, indent=4))

def load_config():
    gpu = Path('/proc/driver/nvidia').exists()

    ui = j.get('ui')
    tunnel = j.get('tunnel')
    d = UID.get(ui, {})

    zrok_token.value = j.get('zrok_token', '')
    ngrok_token.value = j.get('ngrok_token', '')

    launch_args.value = j.get('launch_args') or d.get('args', '')

    if tunnel not in TUNNELS:
        tunnel = 'Pinggy'
        j['tunnel'] = tunnel
        MARK.write_text(json.dumps(j, indent=4))

    tunnel_radio.value = tunnel

    cpu_cb.value = not gpu and j.get('cpu_usage', False)
    cpu_cb.layout.display = 'none' if gpu or ui == 'SwarmUI' else 'block'

    title.value = f"""
    <div class='launcher-title'>
      {''.join(f"<span class='launch-title-{t.lower()}'>{t}</span>" for t in d.get('title', '').split())}
    </div>
    """

    return ui

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
    d = UID[ui]

    env = d['env']
    lib = str(env / 'lib')
    bin = str(env / 'bin')

    D = '/home/studio-lab-user/.conda/envs/default/lib'
    L = f'{D}/libtcmalloc_minimal.so.4'

    if d.get('cm'):
        iRON.pop('MPLBACKEND', None)

    iRON['LD_LIBRARY_PATH'] = f'{lib}:{D}:{iRON.get("LD_LIBRARY_PATH", "")}'

    for k, v in d.get('var', {}).items():
        iRON[k] = v() if callable(v) else v

    if L not in iRON.get('LD_PRELOAD', ''):
        iRON['LD_PRELOAD'] = L

    if bin not in iRON.get('PATH', ''):
        iRON['PATH'] = bin + ':' + iRON.get('PATH', '')

    iRON['PYTHONWARNINGS'] = 'ignore'

def launching(ui, skip_comfyui_check=False):
    args = '' if cpu_cb.value else launch_args.value
    tunnel = tunnel_radio.value

    get_ipython().run_line_magic('run', 'venv.py')

    d = UID[ui]

    py = str(d['env'] / 'bin/python3')
    port = d.get('port', 7860)

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
                if not ft.exists(): SyS(f'{py} -m pip uninstall -qy transformers'); ft.write_text('tf')

            launcher = f'{py} launch.py'

    if cpu_cb.value: args += f" {d.get('cpu', '')}"

    with Zuberg:
        SyS(f'{launcher} {args}')

def waiting(con, ready, ui):
    with con:
        while not ready.value:
            try:
                con.wait()
            except KeyboardInterrupt:
                print(''); clear_output(); sys.exit()

    launching(ui, skip_comfyui_check=args.skip_comfyui_check)

def launch(b):
    launch_panel.close()
    save_config()

    with con:
        ready.value = True
        con.notify()

def exit(b):
    launch_panel.close()

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

JS = """
(() => {
  const baseUrl = JSON.parse(document.querySelector("#jupyter-config-data").textContent).baseUrl;
  document.documentElement.style.setProperty(
    "--segsmaker-bg",
    `url(${location.origin}${baseUrl}files/.gutris1/bg.jpg)`
  );

  setTimeout(() => {
    document.querySelectorAll('.launcher-tunnel-radio label').forEach(label => {
      const text = label.childNodes[0];
      if (text && text.nodeType === Node.TEXT_NODE) {
        const span = document.createElement('span');
        span.textContent = text.textContent.trim();
        label.replaceChild(span, text);
      }
    });

    const tokens = document.querySelectorAll('.launcher-zrok-token input, .launcher-ngrok-token input, .launcher-args input');
    tokens.forEach(el => el.spellcheck = false);
  }, 100);

  setTimeout(() => {
    const box = document.querySelector('.launcher-box');
    box && box.classList.add('loaded');
  }, 400);
})();
"""

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
        ui = load_config()

        if args.skip_widget:
            launching(ui, skip_comfyui_check=args.skip_comfyui_check)

        else:
            load_css()
            display(HTML(f'<script>{JS}</script>'))
            display(launch_panel)

            launch_button.on_click(launch)
            exit_button.on_click(exit)

            Process(target=waiting, args=(con, ready, ui)).start()

    except KeyboardInterrupt:
        pass
