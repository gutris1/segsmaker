from pathlib import Path
from IPython.display import display, HTML
from IPython import get_ipython
import ipywidgets as widgets

home = Path.home()
src = home / '.gutris1'
css = src / "xxx.css"

src.mkdir(parents=True, exist_ok=True)
get_ipython().system(f"curl -sLo {css} https://github.com/gutris1/segsmaker/raw/XYZ/script/xxx/xxx.css")

def load_css(css_path):
    with open(css_path, "r") as file:
        css_content = file.read()

    display(HTML(f"<style>{css_content}</style>"))

output = widgets.Output()

button1 = widgets.Button(description='A1111')
button1.add_class("buttons")
button2 = widgets.Button(description='Forge')
button2.add_class("buttons")
button3 = widgets.Button(description='ComfyUI')
button3.add_class("buttons")

panel = widgets.HBox(
    [button1, button2, button3],
    layout=widgets.Layout(
        width='500px',
        height='100%',
        display='flex',
        flex_flow='row',
        align_items='center',
        justify_content='space-between',
        padding='20px'))

panel.add_class("main-panel")

def selection(b):
    with output:
        panel.close()

        if b.description == 'A1111':
            print('A')
        elif b.description == 'Forge':
            print('F')
        elif b.description == 'ComfyUI':
            print('C')

load_css(css)
display(output, panel)

button1.on_click(selection)
button2.on_click(selection)
button3.on_click(selection)
