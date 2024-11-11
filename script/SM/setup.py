import sys, subprocess

python_version = subprocess.run(['python', '--version'], capture_output=True, text=True).stdout.split()[1]
if tuple(map(int, python_version.split('.'))) < (3, 10, 6):
    print(f"[ERROR]: Python version 3.10.6 or higher required, and you are using Python {python_version}\nExiting.")
    sys.exit()

from IPython.display import display, HTML, clear_output
from IPython import get_ipython
from ipywidgets import widgets
from pathlib import Path
import os

HOME = Path.home()
SRC = HOME / '.gutris1'
CSS = SRC / 'setup.css'
MARK = SRC / 'marking.py'
IMG = SRC / 'loading.png'

A1111 = SRC / 'A1111.py'
Forge = SRC / 'Forge.py'
ComfyUI = SRC / 'ComfyUI.py'
ReForge = SRC / 'ReForge.py'

FaceFusion = SRC / 'FaceFusion.py'
SDTrainer = SRC / 'SDTrainer.py'

SRC.mkdir(parents=True, exist_ok=True)
m = f"curl -sLo {CSS} https://github.com/gutris1/segsmaker/raw/main/script/SM/setup.css"
get_ipython().system(m)

def load_css():
    with open(CSS, "r") as file:
        data = file.read()
    display(HTML(f"<style>{data}</style>"))

def selection(btn):
    multi_panel.close()

    webui_selection = {
        'A1111': A1111,
        'Forge': Forge,
        'ComfyUI': ComfyUI,
        'ReForge': ReForge,
        'FaceFusion': FaceFusion,
        'SDTrainer': SDTrainer
    }

    with output:
        script = webui_selection.get(btn)
        if script:
            get_ipython().run_line_magic('run', f'{script}')

output = widgets.Output()
row1 = ['A1111', 'Forge', 'ComfyUI', 'ReForge']
row2 = ['FaceFusion', 'SDTrainer']

buttons1 = []
for btn in row1:
    button = widgets.Button(description='')
    button.add_class(btn.lower())
    button.on_click(lambda x, btn=btn: selection(btn))
    buttons1.append(button)

buttons2 = []
for btn in row2:
    button = widgets.Button(description='')
    button.add_class(btn.lower())
    button.on_click(lambda x, btn=btn: selection(btn))
    buttons2.append(button)
    
hbox1 = widgets.HBox(buttons1, layout=widgets.Layout(width='630px', height='250px'))
hbox2 = widgets.HBox(buttons2, layout=widgets.Layout(width='630px', height='250px'))

multi_panel = widgets.VBox([hbox1, hbox2], layout=widgets.Layout(width='600px', height='500px'))
multi_panel.add_class('multi-panel')

def multi_widgets():
    x = [
        f"curl -sLo {IMG} https://github.com/gutris1/segsmaker/raw/main/script/SM/loading.png",
        f"curl -sLo {MARK} https://github.com/gutris1/segsmaker/raw/main/script/SM/marking.py",
        f"curl -sLo {A1111} https://github.com/gutris1/segsmaker/raw/main/script/SM/A1111.py",
        f"curl -sLo {Forge} https://github.com/gutris1/segsmaker/raw/main/script/SM/Forge.py",
        f"curl -sLo {ComfyUI} https://github.com/gutris1/segsmaker/raw/main/script/SM/ComfyUI.py",
        f"curl -sLo {ReForge} https://github.com/gutris1/segsmaker/raw/main/script/SM/ReForge.py",
        f"curl -sLo {FaceFusion} https://github.com/gutris1/segsmaker/raw/main/script/SM/FaceFusion.py",
        f"curl -sLo {SDTrainer} https://github.com/gutris1/segsmaker/raw/main/script/SM/SDTrainer.py"
    ]

    load_css()
    display(multi_panel, output)

    for y in x:
        get_ipython().system(y)
    os.chdir(HOME)

multi_widgets()
