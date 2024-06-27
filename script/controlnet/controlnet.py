from IPython.display import display, HTML, clear_output
from ipywidgets import widgets, Layout, Output
from pathlib import Path
from IPython import get_ipython

home = Path.home()
img = home / ".conda/loading.png"
css = home / ".conda/pantat88.css"
webui = Path(__file__).parent.parent

cn15 = webui / "asd/cn-1_5.py"
cnxl = webui / "asd/cn-xl.py"

button1 = widgets.Button(description='SD 1.5')
button2 = widgets.Button(description='SDXL')

output = Output()

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
        css_content = file.read()
    display(HTML(f"<style>{css_content}</style>"))

def controlnet(b):
    with output:
        panel.close()
        output.clear_output()

        if b.description == 'SD 1.5':
            get_ipython().magic(f"run {cn15}")
        else:
            get_ipython().magic(f"run {cnxl}")

load_css(css)
display(panel, output)
button1.on_click(controlnet)
button2.on_click(controlnet)
