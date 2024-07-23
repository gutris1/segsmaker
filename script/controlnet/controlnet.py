from IPython.display import display, HTML, clear_output
from ipywidgets import widgets, Layout, Output
from pathlib import Path
from IPython import get_ipython

img = Path.home() / ".conda/loading.png"
src_cn = Path(__file__).parent
css_cn = src_cn / "cn.css"

cn15 = src_cn / "cn-15.py"
cnxl = src_cn / "cn-xl.py"

x = [
    f"curl -sLo {cn15} https://github.com/gutris1/segsmaker/raw/main/script/controlnet/cn-15.py",
    f"curl -sLo {cnxl} https://github.com/gutris1/segsmaker/raw/main/script/controlnet/cn-xl.py",
    f"curl -sLo {css_cn} https://github.com/gutris1/segsmaker/raw/main/script/controlnet/cn.css"]
for y in x:
    get_ipython().system(y)

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
        width='600px',
        height='400px'))
cn_panel.add_class('cn-panel')

load_css()
display(cn_panel, output)
