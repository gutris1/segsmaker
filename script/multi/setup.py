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
reForge = SRC / 'reForge.py'
FaceFusion = SRC / 'FaceFusion.py'

def load_css():
    with open(CSS, "r") as file:
        data = file.read()

    display(HTML(f"<style>{data}</style>"))

def selection(btn):
    multi_panel.close()

    with output:
        if btn == 'A1111':
            get_ipython().run_line_magic('run', f'{A1111}')
        elif btn == 'Forge':
            get_ipython().run_line_magic('run', f'{Forge}')
        elif btn == 'ComfyUI':
            get_ipython().run_line_magic('run', f'{ComfyUI}')
        elif btn == 'reForge':
            get_ipython().run_line_magic('run', f'{reForge}')
        elif btn == 'FaceFusion':
            get_ipython().run_line_magic('run', f'{FaceFusion}')

options = ['A1111', 'Forge', 'ComfyUI', 'reForge', 'FaceFusion']
buttons = []

for btn in options:
    button = widgets.Button(description='')
    button.add_class(btn.lower())
    button.on_click(lambda x, btn=btn: selection(btn))
    buttons.append(button)

output = widgets.Output()

multi_panel = widgets.HBox(
    buttons, layout=widgets.Layout(
        width='780px',
        height='300px'))
multi_panel.add_class('multi-panel')

def multi_widgets():
    if not SRC.exists():
        SRC.mkdir(parents=True, exist_ok=True)

    x = [
        f"curl -sLo {IMG} https://github.com/gutris1/segsmaker/raw/main/script/loading.png",
        f"curl -sLo {CSS} https://github.com/gutris1/segsmaker/raw/main/script/multi/setup.css",
        f"curl -sLo {MARK} https://github.com/gutris1/segsmaker/raw/main/script/multi/marking.py",
        f"curl -sLo {A1111} https://github.com/gutris1/segsmaker/raw/main/script/multi/A1111.py",
        f"curl -sLo {Forge} https://github.com/gutris1/segsmaker/raw/main/script/multi/Forge.py",
        f"curl -sLo {ComfyUI} https://github.com/gutris1/segsmaker/raw/main/script/multi/ComfyUI.py",
        f"curl -sLo {reForge} https://github.com/gutris1/segsmaker/raw/main/script/multi/reForge.py",
        f"curl -sLo {FaceFusion} https://github.com/gutris1/segsmaker/raw/main/script/multi/FaceFusion.py"
    ]

    for y in x:
        get_ipython().system(y)

    load_css()
    display(multi_panel, output)
    os.chdir(HOME)

multi_widgets()
