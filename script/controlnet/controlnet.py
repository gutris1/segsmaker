from IPython.display import display, HTML, clear_output
from ipywidgets import widgets, Layout, Output
from pathlib import Path
from IPython import get_ipython

img = Path.home() / ".conda/loading.png"
css = Path.home() / ".conda/pantat88.css"
webui = Path(__file__).parent.parent

cn15 = webui / "asd/cn-1_5.py"
cnxl = webui / "asd/cn-xl.py"

x = [
    f"curl -sLo {cn15} https://github.com/gutris1/segsmaker/raw/main/script/controlnet/cn-1_5.py",
    f"curl -sLo {cnxl} https://github.com/gutris1/segsmaker/raw/main/script/controlnet/cn-xl.py",
    f"curl -sLo {webui}/asd/cn.css https://github.com/gutris1/segsmaker/raw/main/script/controlnet/cn.css"]

output = Output()

button1 = widgets.Button(description='SD 1.5')
button2 = widgets.Button(description='SD XL')

panel = widgets.HBox([button1, button2],
                     layout=Layout(
                         width='300px',
                         height='100px',
                         display='flex',
                         flex_flow='row',
                         align_items='center',
                         justify_content='space-between',
                         padding='20px'))

button1.add_class("save-button")
button2.add_class("save-button")
panel.add_class("boxs")

def load_css(css):
    with open(css, "r") as file:
        content = file.read()

    display(HTML(f"<style>{content}</style>"))

def controlnet(b):
    panel.close()
    clear_output()

    with output:
        if b.description == 'SD 1.5':
            get_ipython().run_line_magic('run', f'{cn15}')

        elif b.description == 'SD XL':
            get_ipython().run_line_magic('run', f'{cnxl}')

load_css(css)
display(panel, output)
button1.on_click(controlnet)
button2.on_click(controlnet)

for y in x:
    get_ipython().system(y)