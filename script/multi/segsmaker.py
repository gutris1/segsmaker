from IPython.display import display, HTML, clear_output
from multiprocessing import Process
from IPython import get_ipython
from ipywidgets import widgets
from pathlib import Path
import json, argparse, time

home = Path.home()
src = home / '.gutris1'
css = src / 'multi.css'
mark = src / 'marking.json'
text = Path('txt.txt')

py = '/tmp/venv/bin/python3'

def get_args(ui):
    if ui == 'A1111':
        return '--xformers --enable-insecure-extension-access --disable-console-progressbars --theme dark'

    elif ui == 'Forge':
        return '--xformers --cuda-stream --pin-shared-memory --enable-insecure-extension-access --disable-console-progressbars --theme dark'

    elif ui == 'ComfyUI':
        return '--dont-print-server --preview-method auto --use-pytorch-cross-attention'

def load_config():
    global ui
    config = json.load(mark.open('r')) if mark.exists() else {}
    
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

    if ui == 'A1111':
        title.value = '<h1>A1111</h1>'
    elif ui == 'Forge':
        title.value = '<h1>Forge</h1>'
    elif ui == 'ComfyUI':
        title.value = '<h1>ComfyUI</h1>'

def save_config(zrok_token, ngrok_token, args1, args2, tunnel):
    config = {}
    if mark.exists():
        with mark.open('r') as file:
            config = json.load(file)

    config.update({
        "zrok_token": zrok_token,
        "ngrok_token": ngrok_token,
        "launch_args1": args1,
        "launch_args2": args2,
        "tunnel": tunnel
    })

    with mark.open('w') as file:
        json.dump(config, file, indent=4)

def load_css(css):
    with css.open("r") as file:
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
button_box = widgets.HBox([launch_button, exit_button], layout=widgets.Layout(
    display='flex',
    flex_flow='row',
    justify_content='space-between'))

token_box = widgets.VBox([zrok_token, ngrok_token, args_box], layout=widgets.Layout(
    width='auto',
    height='auto',
    flex_flow='column',
    align_items='center',
    justify_content='space-between',
    padding='0px'))

main_panel = widgets.Box([top, token_box, button_box], layout=widgets.Layout(
    width='700px',
    height='350px',
    display='flex',
    flex_flow='column',
    justify_content='space-between',
    padding='20px'))

title.add_class('title')
tunnel.add_class('checkbox-wrapper-14')
zrok_token.add_class('zrok')
ngrok_token.add_class('ngrok')
launch_args1.add_class('text-input')
launch_args2.add_class('args2')
launch_button.add_class('buttons')
exit_button.add_class('buttons')
main_panel.add_class('main-panel')

parser = argparse.ArgumentParser()
parser.add_argument('--skip-comfyui-check', action='store_true', help='Skip checking ComfyUI for custom node dependencies')
args, unknown = parser.parse_known_args()

def exiting(b):
    main_panel.close()

def launching(ui, skip_comfyui_check=False):
    args = f'{launch_args1.value} {launch_args2.value}'

    get_ipython().run_line_magic('run', 'venv.py')

    if ui in ['A1111', 'Forge', 'ComfyUI']:
        if ui == 'ComfyUI' and not skip_comfyui_check:
            get_ipython().system(f'{py} apotek.py')
            clear_output(wait=True)

        launch = {
            'Pinggy': f'{py} pinggy.py {args}',
            'ZROK': f'{py} zrok.py {zrok_token.value} {args}',
            'NGROK': f'{py} ngrokk.py {ngrok_token.value} {args}'
        }.get(tunnel.value)

        if launch:
            get_ipython().system(launch)

def if_launch(b):
    global ui, zrok_token, ngrok_token, launch_args1, launch_args2, tunnel
    main_panel.close()

    save_config(
        zrok_token.value,
        ngrok_token.value,
        launch_args1.value,
        launch_args2.value,
        tunnel.value)

    Path('txt.txt').write_text('this is txt')

def something():
    global ui
    while not text.exists():
        time.sleep(2)

    load_config()
    launching(ui, skip_comfyui_check=args.skip_comfyui_check)

def display_widgets():
    if text.exists():
        text.unlink()

    load_config()
    load_css(css)
    display(main_panel)

    launch_button.on_click(if_launch)
    exit_button.on_click(exiting)

if __name__ == '__main__':
    try:
        display_widgets()

        batu = Process(target=something)
        batu.start()

    except KeyboardInterrupt:
        text.unlink()
        pass