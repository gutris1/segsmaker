
from IPython.display import display, HTML, clear_output, Image
from multiprocessing import Process, Condition, Value
from IPython import get_ipython
from ipywidgets import widgets
from pathlib import Path
import json, argparse, sys, logging, yaml

HOME = Path.home()
SRC = HOME / '.gutris1'
CSS = SRC / 'setup.css'
MARK = SRC / 'marking.json'
IMG = SRC / "loading.png"

py = '/tmp/venv/bin/python3'

def get_args(ui):
    args_line = {
        'A1111': ('--xformers --no-half-vae'),
        'Forge': ('--disable-xformers --opt-sdp-attention --cuda-stream --pin-shared-memory'),
        'ComfyUI': ('--dont-print-server --preview-method auto --use-pytorch-cross-attention'),
        'ReForge': ('--xformers --cuda-stream --pin-shared-memory'),
        'FaceFusion': '',
        'SDTrainer': '',
        'SwarmUI': ('--launch_mode none')
    }

    return args_line.get(ui, '')

def GPU_check():
    return Path("/proc/driver/nvidia").exists()

def load_config():
    global ui
    config = json.load(MARK.open('r')) if MARK.exists() else {}

    ui = config.get('ui', None)
    zrok_token.value = config.get('zrok_token', '')
    ngrok_token.value = config.get('ngrok_token', '')

    arg = config.get('launch_args')
    if arg:
        launch_args.value = arg
    else:
        launch_args.value = get_args(ui)

    tunnell = config.get('tunnel')
    if tunnell in ['Pinggy', 'ZROK', 'NGROK']:
        tunnel.value = tunnell
    else:
        tunnel.value = 'Pinggy'
        config.update({"tunnel": tunnel.value})
        with MARK.open('w') as file:
            json.dump(config, file, indent=4)

    if GPU_check():
        cpu_cb.value = False
    else:
        cpu_cb.value = config.get('cpu_usage', False)

    cpu_cb.layout.display = 'none' if ui in ['SDTrainer', 'FaceFusion', 'SwarmUI'] or GPU_check() else 'block'

    ui_titles = {
        'A1111': 'A1111',
        'Forge': 'Forge',
        'ComfyUI': 'ComfyUI',
        'ReForge': 'ReForge',
        'FaceFusion': 'Face Fusion',
        'SDTrainer': 'SD Trainer',
        'SwarmUI': 'SwarmUI'
    }
    title.value = f'<div class="title"><h1>{ui_titles.get(ui, "Unknown UI")}</h1></div>'

def save_config(zrok_token, ngrok_token, launch_args, tunnel):
    config = {}
    if MARK.exists():
        with MARK.open('r') as file:
            config = json.load(file)

    config.update({
        "zrok_token": zrok_token,
        "ngrok_token": ngrok_token,
        "launch_args": launch_args,
        "tunnel": tunnel,
        "cpu_usage": cpu_cb.value
    })

    with MARK.open('w') as file:
        json.dump(config, file, indent=4)

def load_css():
    display(HTML(f"<style>{CSS.read_text()}</style>"))

title = widgets.HTML()
zrok_token = widgets.Text(placeholder='Your ZROK Token')
ngrok_token = widgets.Text(placeholder='Your NGROK Token')

launch_args = widgets.Text(placeholder='Launch Arguments List', layout=widgets.Layout(top='20px'))

options = ["Pinggy", "ZROK", "NGROK"]
tunnel = widgets.RadioButtons(
    options=options,
    layout=widgets.Layout(
        display='flex',
        flex_flow='row',
        justify_content='space-between'
    )
)

top = widgets.HBox(
    [tunnel, title],
    layout=widgets.Layout(
        display='flex',
        flex_flow='row',
        justify_content='space-between'
    )
)

launch_button = widgets.Button(description='Launch')
exit_button = widgets.Button(description='Exit')
cpu_cb = widgets.Checkbox(value=False, description='CPU', layout=widgets.Layout(left='10px'))
button_box = widgets.HBox(
    [launch_button, cpu_cb, exit_button],
    layout=widgets.Layout(
        display='flex',
        flex_flow='row',
        align_items='center',
        justify_content='space-between'
    )
)

token_box = widgets.VBox(
    [zrok_token, ngrok_token, launch_args],
    layout=widgets.Layout(
        width='auto',
        height='auto',
        flex_flow='column',
        align_items='center',
        justify_content='space-between',
        padding='0px'
    )
)

launch_panel = widgets.Box(
    [top, token_box, button_box],
    layout=widgets.Layout(
        width='700px',
        height='300px',
        display='flex',
        flex_flow='column',
        justify_content='space-between',
        padding='20px'
    )
)

cpu_cb.add_class('cpu-cbx')
tunnel.add_class('tunnel')
zrok_token.add_class('zrok')
ngrok_token.add_class('ngrok')
launch_args.add_class('text-input')
launch_button.add_class('buttons')
exit_button.add_class('buttons')
launch_panel.add_class('launch-panel')

parser = argparse.ArgumentParser()
parser.add_argument('--skip-comfyui-check', action='store_true', help='Skip checking custom node dependencies for ComfyUI')
parser.add_argument('--skip-widget', action='store_true', help='Skip displaying the widget')
args, unknown = parser.parse_known_args()

condition = Condition()
is_ready = Value('b', False)

def ZROK_enable():
    if not zrok_token.value:
        print("[ERROR]: ZROK Token is empty")
        sys.exit()

    zrokbin = HOME / '.zrok/bin/zrok'
    if not zrokbin.exists():
        print("[ERROR]: ZROK is not installed")
        sys.exit()

    zrok_env = HOME / '.zrok/environment.json'
    if zrok_env.exists():
        with open(zrok_env, 'r') as f:
            current_value = json.load(f)
            current_token = current_value.get('zrok_token')

        if current_token == zrok_token.value:
            pass
        else:
            get_ipython().system('zrok disable')
            get_ipython().system(f'zrok enable {zrok_token.value}')
            print()
    else:
        get_ipython().system(f'zrok enable {zrok_token.value}')
        print()

def NGROK_auth():
    if not ngrok_token.value:
        print("[ERROR]: NGROK Token is empty")
        sys.exit()

    ngrokbin = HOME / '.ngrok/bin/ngrok'
    if not ngrokbin.exists():
        print("[ERROR]: NGROK is not installed")
        sys.exit()

    ngrok_yml = HOME / '.config/ngrok/ngrok.yml'
    if ngrok_yml.exists():
        with open(ngrok_yml, 'r') as f:
            current_value = yaml.safe_load(f)
            current_token = current_value.get('agent', {}).get('authtoken')

        if current_token == ngrok_token.value:
            pass
        else:
            get_ipython().system(f'ngrok config add-authtoken {ngrok_token.value}')
            print()
    else:
        get_ipython().system(f'ngrok config add-authtoken {ngrok_token.value}')
        print()

def launching(ui, skip_comfyui_check=False):
    global py
    args = f'{launch_args.value}'
    tunnel_name = tunnel.value

    get_ipython().run_line_magic('run', 'venv.py')

    if cpu_cb.value:
        if ui == 'A1111':
            args += ' --use-cpu all --precision full --no-half --skip-torch-cuda-test'
        elif ui in ['ReForge', 'Forge']:
            args += ' --always-cpu --skip-torch-cuda-test'
        elif ui == 'ComfyUI':
            args += ' --cpu'

    if ui == 'SDTrainer':
        port = 28000
    elif ui == 'SwarmUI':
        port = 7801
    elif ui == 'ComfyUI':
        port = 8188
        if not skip_comfyui_check:
            get_ipython().system(f'{py} apotek.py')
            clear_output(wait=True)
    else:
        port = 7860

    if ui in ['A1111', 'Forge', 'ReForge']:
        args += ' --enable-insecure-extension-access --disable-console-progressbars --theme dark'
    elif ui == 'FaceFusion':
        py = '/tmp/venv-fusion/bin/python3'
    elif ui == 'SDTrainer':
        py = 'HF_HOME=huggingface /tmp/venv-sd-trainer/bin/python3'

    tunnel_config = {
        'Pinggy': {
            'command': f"ssh -o StrictHostKeyChecking=no -p 80 -R0:localhost:{port} a.pinggy.io",
            'name': "PINGGY",
            'pattern': r"https://[\w-]+\.a\.free\.pinggy\.link"
        },
        'NGROK': {
            'command': f"ngrok http http://localhost:{port} --log stdout",
            'name': "NGROK",
            'pattern': r"https://[\w-]+\.ngrok-free\.app"
        },
        'ZROK': {
            'command': f"zrok share public localhost:{port} --headless",
            'name': "ZROK",
            'pattern': r"https://[\w-]+\.share\.zrok\.io"
        }
    }

    c = f'{py} Launcher.py {args}'
    cmd = {key: c for key in ['Pinggy', 'ZROK', 'NGROK']}.get(tunnel_name)
    configs = tunnel_config.get(tunnel_name)

    if cmd and configs:
        try:
            from cupang import Tunnel as Alice_Zuberg

            if tunnel_name == 'ZROK':
                ZROK_enable()

            if tunnel_name == 'NGROK':
                NGROK_auth()

            Alice_Synthesis_Thirty = Alice_Zuberg(port)
            Alice_Synthesis_Thirty.logger.setLevel(logging.DEBUG)
            Alice_Synthesis_Thirty.add_tunnel(command=configs['command'], name=configs['name'], pattern=configs['pattern'])

            with Alice_Synthesis_Thirty:
                get_ipython().system(cmd)

        except KeyboardInterrupt:
            pass

def waiting(condition, is_ready):
    with condition:
        while not is_ready.value:
            try:
                condition.wait()
            except KeyboardInterrupt:
                print('')
                clear_output()
                sys.exit()

    load_config()
    launching(ui, skip_comfyui_check=args.skip_comfyui_check)

def launch(b):
    global ui, zrok_token, ngrok_token, launch_args, tunnel
    launch_panel.close()

    save_config(
        zrok_token.value,
        ngrok_token.value,
        launch_args.value,
        tunnel.value)

    with condition:
        is_ready.value = True
        condition.notify()

def exit(b):
    launch_panel.close()

def display_widgets():
    load_config()
    load_css()
    display(launch_panel)

    launch_button.on_click(launch)
    exit_button.on_click(exit)

if __name__ == '__main__':
    try:
        if args.skip_widget:
            load_config()
            launching(ui, skip_comfyui_check=args.skip_comfyui_check)

        else:
            display_widgets()
            p = Process(target=waiting, args=(condition, is_ready))
            p.start()

    except KeyboardInterrupt:
        pass
