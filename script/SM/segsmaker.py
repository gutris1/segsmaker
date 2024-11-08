from IPython.display import display, HTML, clear_output, Image
from multiprocessing import Process, Condition, Value
from IPython import get_ipython
from ipywidgets import widgets
from pathlib import Path
import json, argparse, sys, logging

SRC = Path.home() / '.gutris1'
CSS = SRC / 'setup.css'
MARK = SRC / 'marking.json'
IMG = SRC / "loading.png"

py = '/tmp/venv/bin/python3'

def get_args(ui):
    args_line = {
        'A1111': (
            '--xformers --no-half-vae'
        ),
        'Forge': (
            '--disable-xformers --opt-sdp-attention --cuda-stream --pin-shared-memory'
        ),
        'ComfyUI': (
            '--dont-print-server --preview-method auto --use-pytorch-cross-attention'
        ),
        'ReForge': (
            '--xformers --cuda-stream --pin-shared-memory'
        ),
        'FaceFusion': '',
        'SDTrainer': ''
    }

    return args_line.get(ui, '')

def GPU_check():
    o = get_ipython().getoutput('nvidia-smi')
    return not any("command not found" in ppai for ppai in o)

def load_config():
    global ui
    config = json.load(MARK.open('r')) if MARK.exists() else {}

    ui = config.get('ui', None)
    zrok_token.value = config.get('zrok_token', '')
    ngrok_token.value = config.get('ngrok_token', '')

    launch_argz1 = config.get('launch_args1')
    if launch_argz1:
        launch_args1.value = launch_argz1
    else:
        launch_args1.value = get_args(ui)

    launch_args2.value = config.get('launch_args2', '')

    tunnell = config.get('tunnel')
    if tunnell in ['Pinggy', 'ZROK', 'NGROK']:
        tunnel.value = tunnell
    else:
        tunnel.value = 'Pinggy'

    cpu_cb.value = config.get('cpu_usage', False)

    GPU = GPU_check()

    if ui in ['SDTrainer', 'FaceFusion'] or not GPU:
        cpu_cb.layout.display = 'none'
    else:
        cpu_cb.layout.display = 'block'

    if ui == 'A1111':
        title.value = '<div class="title"><h1>A1111</h1></div>'
    elif ui == 'Forge':
        title.value = '<div class="title"><h1>Forge</h1></div>'
    elif ui == 'ComfyUI':
        title.value = '<div class="title"><h1>ComfyUI</h1></div>'
    elif ui == 'ReForge':
        title.value = '<div class="title"><h1>ReForge</h1></div>'
    elif ui == 'FaceFusion':
        title.value = '<div class="title"><h1>Face Fusion</h1></div>'
    elif ui == 'SDTrainer':
        title.value = '<div class="title"><h1>SD Trainer</h1></div>'

def save_config(zrok_token, ngrok_token, args1, args2, tunnel):
    config = {}
    if MARK.exists():
        with MARK.open('r') as file:
            config = json.load(file)

    config.update({
        "zrok_token": zrok_token,
        "ngrok_token": ngrok_token,
        "launch_args1": args1,
        "launch_args2": args2,
        "tunnel": tunnel,
        "cpu_usage": cpu_cb.value
    })

    with MARK.open('w') as file:
        json.dump(config, file, indent=4)

def load_css():
    with open(CSS, "r") as file:
        data = file.read()

    display(HTML(f"<style>{data}</style>"))

title = widgets.HTML()
zrok_token = widgets.Text(placeholder='Your ZROK Token')
ngrok_token = widgets.Text(placeholder='Your NGROK Token')

launch_args1 = widgets.Text(placeholder='Launch Arguments List')
launch_args2 = widgets.Text(placeholder='Add Launch Arguments List here')
args_box = widgets.VBox([launch_args1, launch_args2], layout=widgets.Layout(
    display='flex',
    flex_flow='column',
    justify_content='space-between'))

options = ["Pinggy", "ZROK", "NGROK"]
tunnel = widgets.RadioButtons(options=options, layout=widgets.Layout(
    display='flex',
    flex_flow='row',
    justify_content='space-between'))

tunnel_button = widgets.Box([tunnel])
top = widgets.HBox([tunnel, title], layout=widgets.Layout(
    display='flex',
    flex_flow='row',
    justify_content='space-between'))

launch_button = widgets.Button(description='Launch')
exit_button = widgets.Button(description='Exit')
cpu_cb = widgets.Checkbox(value=False, description='CPU', layout=widgets.Layout(left='10px'))
button_box = widgets.HBox([launch_button, cpu_cb, exit_button], layout=widgets.Layout(
    display='flex',
    flex_flow='row',
    align_items='center',
    justify_content='space-between'))

token_box = widgets.VBox([zrok_token, ngrok_token, args_box], layout=widgets.Layout(
    width='auto',
    height='auto',
    flex_flow='column',
    align_items='center',
    justify_content='space-between',
    padding='0px'))

launch_panel = widgets.Box([top, token_box, button_box], layout=widgets.Layout(
    width='700px',
    height='350px',
    display='flex',
    flex_flow='column',
    justify_content='space-between',
    padding='20px'))

cpu_cb.add_class('cpu-cbx')
tunnel.add_class('tunnel')
zrok_token.add_class('zrok')
ngrok_token.add_class('ngrok')
launch_args1.add_class('text-input')
launch_args2.add_class('args2')
launch_button.add_class('buttons')
exit_button.add_class('buttons')
launch_panel.add_class('launch-panel')

parser = argparse.ArgumentParser()
parser.add_argument('--skip-comfyui-check', action='store_true', help='Skip checking custom node dependencies for ComfyUI')
parser.add_argument('--skip-widget', action='store_true', help='Skip displaying the widget')
args, unknown = parser.parse_known_args()

condition = Condition()
is_ready = Value('b', False)

def zrok_enable():
    zrok_path = Path('/home/studio-lab-user/.zrok')
    if not zrok_path.exists():
        print("ZROK is not installed.")
        return

    env = zrok_path / 'environment.json'
    if env.exists():
        with open(env, 'r') as f:
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

def import_cupang():
    try:
        from cupang import Tunnel as Alice_Zuberg
    except ImportError:
        strup = Path.home() / '.ipython/profile_default/startup'
        dl = f'curl -sLo {strup}/cupang.py https://github.com/gutris1/segsmaker/raw/main/script/SM/cupang.py'
        get_ipython().system(dl)
        sys.path.append(str(strup))

def launching(ui, skip_comfyui_check=False):
    import_cupang()
    args = f'{launch_args1.value} {launch_args2.value}'

    if cpu_cb.value:
        if ui == 'A1111':
            args += ' --use-cpu all --precision full --no-half --skip-torch-cuda-test'
        elif ui in ['ReForge', 'Forge']:
            args += ' --always-cpu --skip-torch-cuda-test'
        elif ui == 'ComfyUI':
            args += ' --cpu'

    get_ipython().run_line_magic('run', 'venv.py')

    log_file = Path('segsmaker.log')
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="{message}", style="{"
    )

    if ui in ['A1111', 'Forge', 'ComfyUI', 'ReForge']:
        log_msg = 'comfyui' if ui == 'ComfyUI' else 'A1111/Forge'
        log_file.write_text(log_msg + '\n')
        port = 8188 if ui == 'ComfyUI' else 7860
        
        if ui == 'ComfyUI' and not skip_comfyui_check:
            get_ipython().system(f'{py} apotek.py')
            clear_output(wait=True)

        tunnel_list, cmd = tunnel_cmd(tunnel.value, port, args, ui, FF=False, SDT=False)

    elif ui == 'FaceFusion':
        log_file.write_text('Face-Fusion\n')
        port = 7860
        tunnel_list, cmd = tunnel_cmd(tunnel.value, port, args, ui, FF=True, SDT=False)

    elif ui == 'SDTrainer':
        log_file.write_text('SD-Trainer\n')
        port = 28000
        tunnel_list, cmd = tunnel_cmd(tunnel.value, port, args, ui, FF=False, SDT=True)

    if cmd:        
        if tunnel.value == 'NGROK':
            get_ipython().system(cmd)
        else:
            configs = tunnel_configs(tunnel.value, port)
            run_tunnel(cmd, configs, port)

def tunnel_cmd(tunnel_value, port, args, ui, FF, SDT):
    global py

    if ui != 'ComfyUI' and not FF and not SDT:
        args += ' --enable-insecure-extension-access --disable-console-progressbars --theme dark'

    if FF:
        display(Image(filename=str(IMG)))
        clear_output(wait=True)
        py = '/tmp/venv-fusion/bin/python3'
        c = f'{py} launch.py {args}'
    elif SDT:
        py = 'HF_HOME=huggingface /tmp/venv-sd-trainer/bin/python3'
        c = f'{py} launch.py {args}'
    elif ui == 'ComfyUI':
        c = f'{py} launch.py {args}'
    else:
        c = f'{py} slauncher.py {args}'

    tunnel_list = {
        'Pinggy': c,
        'ZROK': c,
        'NGROK': c
    }

    return tunnel_list, tunnel_list.get(tunnel_value)

def tunnel_configs(tunnel_value, port):
    config_list = {
        'Pinggy': {
            'command': f"ssh -o StrictHostKeyChecking=no -p 80 -R0:localhost:{port} a.pinggy.io",
            'name': "PINGGY",
            'pattern': r"https://[\w-]+\.a\.free\.pinggy\.link"
        },
        'ZROK': {
            'command': f"zrok share public localhost:{port} --headless",
            'name': "ZROK",
            'pattern': r"https://[\w-]+\.share\.zrok\.io"
        }
    }

    return config_list.get(tunnel_value)

def run_tunnel(cmd, configs, port):
    try:
        from cupang import Tunnel as Alice_Zuberg

        if tunnel.value == 'ZROK':
            zrok_enable()

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
    global ui, zrok_token, ngrok_token, launch_args1, launch_args2, tunnel
    launch_panel.close()

    save_config(
        zrok_token.value,
        ngrok_token.value,
        launch_args1.value,
        launch_args2.value,
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
