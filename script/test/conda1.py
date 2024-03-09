from ipywidgets import widgets, Button, Text, VBox, Layout
from IPython.display import display, HTML, clear_output
from IPython import get_ipython
import subprocess
import json
import os

xxx = "/home/studio-lab-user"
cp = f"{xxx}/.conda/pantat88.css"
sp = f"{xxx}/.ipython/profile_default/startup/pantat88.py"
ewe = f"{xxx}/.your-civitai-api-key"
uwaaah = os.path.join(ewe, "api_key.json")

jalanan = [f'curl -sLo {sp} https://github.com/gutris1/segsmaker/raw/main/script/pantat88.py',
           f'curl -sLo {xxx}/.ipython/profile_default/startup/nenen88.py https://github.com/gutris1/segsmaker/raw/main/script/nenen88.py',
           f'curl -sLo {xxx}/.ipython/profile_default/startup/00-startup.py https://github.com/gutris1/segsmaker/raw/main/script/00-startup.py',
           f'curl -sLo {cp} https://github.com/gutris1/segsmaker/raw/main/script/pantat88.css']

for janda in jalanan:
    subprocess.run(janda, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

susu = widgets.Output()
sb = widgets.Button(description="Save")
sb.add_class("save-button")

ink = widgets.Text(placeholder='enter your civitai API KEY here')
ink.add_class("api-input")

boxs = VBox([ink, sb], layout=Layout(
    width='450px',
    height='150px',
    display='flex',
    flex_flow='column',
    align_items='center',
    justify_content='space-around',
    padding='20px'))
boxs.add_class("boxs")

os.makedirs(os.path.dirname(cp), exist_ok=True)
os.makedirs(os.path.dirname(sp), exist_ok=True)
os.makedirs(ewe, exist_ok=True)

def bbbbb(css_path):
    with open(css_path, "r") as file:
        css_content = file.read()
        
    display(HTML(f"<style>{css_content}</style>"))

def ccccc(api_key):
    with open(sp, "r") as file:
        lalalala = file.read()
        
    hantu = lalalala.replace("?token=YOUR_API_KEY", f"?token={api_key}")
    with open(sp, "w") as file:
        file.write(hantu)

def ddddd():
    def ass(cmd, cod, rainbow):
        with susu:
            display(HTML(f"<span style='color:{rainbow};'>{cod}</span>"))
            subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    ass('conda install -y conda glib psutil gperftools aria2 gdown',
        '【 Installing Conda 】', 'cyan')
    ass('conda install -y -n base python=3.10.12',
        '【 Installing Python 3.10 】', '#D48900')
    ass('conda clean -y --all',
        '【 Cleaning Conda 】', '#66ff00')
    ass('pip install torch==2.1.2+cu121 torchvision==0.16.2+cu121 torchaudio==2.1.2 --extra-index-url https://download.pytorch.org/whl/cu121',
        '【 Installing Torch 】', 'magenta')
    ass('pip install xformers==0.0.23.post1 triton==2.1.0',
        '【 Installing xformers 】', 'orange')

    with susu:
        display(HTML('<span style="color: cyan;">【 Done 】</span>'))
        
    susu.clear_output(wait=True)
    get_ipython().kernel.do_shutdown(True)
    
def eeeee():
    def fffff(b):
        
        api_key = ink.value.strip()

        if not api_key:
            with susu:
                display(HTML('<span style="color: red;">Please enter your CivitAI API KEY</span>'))
            return

        if len(api_key) < 32:
            with susu:
                display(HTML('<span style="color: red;">API key must be at least 32 characters long</span>'))
            return

        kagi = {"api_key": api_key}
        with open(uwaaah, "w") as file:
            json.dump(kagi, file)
        
        ccccc(api_key)
        widgets.Widget.close(boxs)
        
        with susu:
            clear_output(wait=True)
            
        ddddd()
        
    sb.on_click(fffff)

def ggggg():
    if os.path.exists(uwaaah):
        with open(uwaaah, "r") as file:
            bau = json.load(file)
        api_key = bau.get("api_key", "")
        
        with susu:
            clear_output(wait=True)
            
        ccccc(api_key)
        display(susu)
        ddddd()
        
    else:
        bbbbb(cp)
        display(boxs)
        display(susu)
        eeeee()
        
ggggg()
