from IPython.display import display, HTML, clear_output
from IPython import get_ipython
from ipywidgets import widgets
from pathlib import Path

src_cn = Path(__file__).parent
css_cn = src_cn / "controlnet.css"
cn15 = src_cn / "cn-15.py"
cnxl = src_cn / "cn-xl.py"
img = Path.home() / ".gutris1/loading.png"

def load_css():
    with open(css_cn, "r") as file:
        cn = file.read()

    display(HTML(f"<style>{cn}</style>"))

def controlnet(btn):
    cn_panel.close()
    clear_output()

    with output:
        if btn == 'btn-cn-15':
            get_ipython().run_line_magic('run', f'{cn15}')
        elif btn == 'btn-cn-xl':
            get_ipython().run_line_magic('run', f'{cnxl}')

options = ['btn-cn-15', 'btn-cn-xl']
buttons = []

for btn in options:
    button = widgets.Button(description='')
    button.add_class(btn.lower())
    button.on_click(lambda x, btn=btn: controlnet(btn))
    buttons.append(button)

output = widgets.Output()

cn_panel = widgets.HBox(
    buttons, layout=widgets.Layout(
        width='460px',
        height='405px'))
cn_panel.add_class('cn-panel')

def controlnet_widgets():
    x = [
        f"curl -sLo {cn15} https://github.com/gutris1/segsmaker/raw/main/script/SM/cn-15.py",
        f"curl -sLo {cnxl} https://github.com/gutris1/segsmaker/raw/main/script/SM/cn-xl.py",
        f"curl -sLo {css_cn} https://github.com/gutris1/segsmaker/raw/main/script/SM/controlnet.css"]
    for y in x:
        get_ipython().system(y)

    load_css()
    display(cn_panel, output)

controlnet_widgets()
