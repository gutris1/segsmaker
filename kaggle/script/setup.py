from IPython.display import display, HTML, clear_output
from IPython import get_ipython
from ipywidgets import widgets
from pathlib import Path
import subprocess, shlex, os, sys, json

env, HOME = 'Unknown', None
env_list = {'Colab': '/content', 'Kaggle': '/kaggle/working'}

for env_name, path in env_list.items():
    if os.getenv(env_name.upper() + '_JUPYTER_TRANSPORT') or os.getenv(env_name.upper() + '_DATA_PROXY_TOKEN'):
        env, HOME = env_name, path
        break

if HOME is None:
    print("You are not in Kaggle or Google Colab.\nExiting.")
    sys.exit()

HOME = Path(HOME)
#HOME = Path.home()
SRC = HOME / 'gutris1'
CSS = SRC / 'setup.css'
MARK = SRC / 'marking.py'
IMG = SRC / 'loading.png'

A1111 = SRC / 'A1111.py'
Forge = SRC / 'Forge.py'
ComfyUI = SRC / 'ComfyUI.py'
ReForge = SRC / 'ReForge.py'

#STR = HOME / '.ipython/profile_default/startup'
STR = Path('/root/.ipython/profile_default/startup')
with open(STR / 'HOMEPATH.py', 'w') as file:
    file.write(f"PATHHOME = '{HOME}'\n")

scripts = [
    f"curl -sLo {STR}/00-startup.py https://github.com/gutris1/segsmaker/raw/K/kaggle/script/00-startup.py",
    f"curl -sLo {STR}/pantat88.py https://github.com/gutris1/segsmaker/raw/K/kaggle/script/pantat88.py",
    f"curl -sLo {STR}/nenen88.py https://github.com/gutris1/segsmaker/raw/K/kaggle/script/nenen88.py",
    f"curl -sLo {STR}/util.py https://github.com/gutris1/segsmaker/raw/main/script/util.py",
    f"curl -sLo {STR}/loading.png https://github.com/gutris1/segsmaker/raw/main/script/loading.png",
    f"curl -sLo {STR}/cupang.py https://github.com/gutris1/segsmaker/raw/main/script/cupang.py"
]

for items in scripts:
    subprocess.run(shlex.split(items), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

sys.path.append(str(STR))

def load_css():
    with open(CSS, "r") as file:
        data = file.read()

    display(HTML(f"<style>{data}</style>"))

def marking(path, fn, ui):
    txt = path / fn
    values = {
        'ui': ui,
        'launch_args1': '',
        'launch_args2': '',
        'zrok_token': '',
        'ngrok_token': '',
        'tunnel': ''
    }

    if not txt.exists():
        with open(txt, 'w') as file:
            json.dump(values, file, indent=4)

    with open(txt, 'r') as file:
        data = json.load(file)

    data.update({
        'ui': ui,
        'launch_args1': '',
        'launch_args2': '',
        'tunnel': ''
    })

    with open(txt, 'w') as file:
        json.dump(data, file, indent=4)

def installing_webui(ui, sd_value):
    print(f"{ui} - {sd_value}")

def handle_launch(b):
    multi_panel.close()

    webui_selection = {
        'A1111': A1111,
        'Forge': Forge,
        'ComfyUI': ComfyUI,
        'ReForge': ReForge
    }

    ui = webuiradio1.value
    sd_value = webuiradio2.value
    marking(SRC, 'marking.json', ui)

    with output:
        installing_webui(ui, sd_value)

output = widgets.Output()

civitai_key_box = widgets.Text(placeholder='Enter Your Civitai API KEY Here',
                               layout=widgets.Layout(left='35px', padding='10px', width='320px'))

WEBUI_LIST = ['A1111', 'Forge', 'ComfyUI', 'ReForge']
list1 = {btn: btn.lower() for btn in WEBUI_LIST}

webuiradio1 = widgets.RadioButtons(options=list1, layout=widgets.Layout(width='300px', height='auto'))

WHICH_SD = ['SD 1.5', 'SD XL']
list2 = {btn: btn.lower() for btn in WHICH_SD}

webuiradio2 = widgets.RadioButtons(options=list2,
                                   layout=widgets.Layout(right='50px', width='300px', height='auto'))

radio_list = widgets.HBox([webuiradio1, webuiradio2],
                          layout=widgets.Layout(padding='10px', width='600px', height='400px'))

launch_button = widgets.Button(description='Install')
exit_button = widgets.Button(description='Exit')
button_box = widgets.HBox([exit_button, launch_button], layout=widgets.Layout(
    padding='10px',
    display='flex',
    flex_flow='row',
    justify_content='space-between'))

multi_panel = widgets.VBox([civitai_key_box, radio_list, button_box], layout=widgets.Layout(width='400px', height='340px'))

civitai_key_box.add_class("api-input")
webuiradio1.add_class("webui-radio")
webuiradio2.add_class("webui-radio")
multi_panel.add_class('launch-panel')
launch_button.add_class('buttons')
exit_button.add_class('buttons')

launch_button.on_click(handle_launch)
exit_button.on_click(lambda b: (multi_panel.close(), clear_output()))

def multi_widgets():
    if not SRC.exists():
        SRC.mkdir(parents=True, exist_ok=True)

    x = [
        f"curl -sLo {IMG} https://github.com/gutris1/segsmaker/raw/main/script/loading.png",
        f"curl -sLo {CSS} https://github.com/gutris1/segsmaker/raw/main/script/multi/setup.css",
        f"curl -sLo {MARK} https://github.com/gutris1/segsmaker/raw/main/script/multi/marking.py",
        f"curl -sLo {A1111} https://github.com/gutris1/segsmaker/raw/K/kaggle/script/A1111.py",
        f"curl -sLo {Forge} https://github.com/gutris1/segsmaker/raw/main/script/multi/Forge.py",
        f"curl -sLo {ComfyUI} https://github.com/gutris1/segsmaker/raw/main/script/multi/ComfyUI.py",
        f"curl -sLo {ReForge} https://github.com/gutris1/segsmaker/raw/main/script/multi/ReForge.py"
    ]

    for y in x:
        get_ipython().system(y)

    load_css()
    display(multi_panel, output)
    os.chdir(HOME)

print('Loading Widget...')
clear_output(wait=True)
multi_widgets()
