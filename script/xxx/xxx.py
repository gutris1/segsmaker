from pathlib import Path
from IPython.display import display, HTML, clear_output
from IPython import get_ipython
from ipywidgets import widgets
import os

home = Path.home()
src = home / '.gutris1'
css = src / 'xxx.css'
mark = src / 'marking.py'
img = src / 'loading.png'

A1111 = src / 'A1111.py'
Forge = src / 'Forge.py'
ComfyUI = src / 'ComfyUI.py'

os.chdir(home)
src.mkdir(parents=True, exist_ok=True)

x = [
    f"curl -sLo {css} https://github.com/gutris1/segsmaker/raw/main/script/xxx/xxx.css",
    f"curl -sLo {img} https://github.com/gutris1/segsmaker/raw/main/script/loading.png",
    f"curl -sLo {mark} https://github.com/gutris1/segsmaker/raw/main/script/xxx/marking.py",
    f"curl -sLo {A1111} https://github.com/gutris1/segsmaker/raw/main/script/xxx/A1111.py",
    f"curl -sLo {Forge} https://github.com/gutris1/segsmaker/raw/main/script/xxx/Forge.py",
    f"curl -sLo {ComfyUI} https://github.com/gutris1/segsmaker/raw/main/script/xxx/ComfyUI.py"]
    
for y in x:
    get_ipython().system(y)

def dupe_button(desc):
    button = widgets.Button(description=desc)
    button.add_class("buttons")
    return button

output = widgets.Output()
buttons = [dupe_button(desc) for desc in ['A1111', 'Forge', 'ComfyUI']]
selection_panel = widgets.HBox(buttons, layout=widgets.Layout(
    width='500px',
    height='100%',
    display='flex',
    flex_flow='row',
    align_items='center',
    justify_content='space-between',
    padding='20px'))

selection_panel.add_class("main-panel")

def load_css(css):
    with css.open("r") as file:
        data = file.read()

    display(HTML(f"<style>{data}</style>"))

def selection(b):
    selection_panel.close()
    clear_output()

    with output:
        if b.description == 'A1111':
            get_ipython().magic(f'run {A1111}')

        elif b.description == 'Forge':
            get_ipython().magic(f'run {Forge}')

        elif b.description == 'ComfyUI':
            get_ipython().magic(f'run {ComfyUI}')

load_css(css)
display(selection_panel, output)

for button in buttons:
    button.on_click(selection)
