from ipywidgets import widgets, Button, Text, VBox, Layout
from IPython.display import display, HTML, clear_output
from IPython import get_ipython
from pathlib import Path
import subprocess, json, shlex

xxx = "/home/studio-lab-user"
cp = f"{xxx}/.conda/pantat88.css"
sp = f"{xxx}/.ipython/profile_default/startup"
nsp = f"{sp}/nenen88.py"
fsp = f"{xxx}/.ipython/profile_default/startup/pantat88.py"
ewe = f"{xxx}/.your-civitai-api-key"
uwaaah = Path(ewe) / "api_key.json"

jalanan = [f"curl -sLo {fsp} https://github.com/gutris1/segsmaker/raw/main/script/pantat88.py",
           f"curl -sLo {xxx}/.condarc https://github.com/gutris1/segsmaker/raw/main/script/.condarc",
           f"curl -sLo {nsp} https://github.com/gutris1/segsmaker/raw/main/script/nenen88.py",
           f"curl -sLo {sp}/00-startup.py https://github.com/gutris1/segsmaker/raw/main/script/00-startup.py",
           f"curl -sLo {cp} https://github.com/gutris1/segsmaker/raw/main/script/pantat88.css"]

for janda in jalanan:
    subprocess.run(shlex.split(janda), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

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

garizzzz = """
    <div class="gradient-conda">.</div>
    """
garis1 = widgets.Output()

Path(cp).parent.mkdir(parents=True, exist_ok=True)
Path(fsp).parent.mkdir(parents=True, exist_ok=True)
Path(ewe).mkdir(parents=True, exist_ok=True)

def aaaaa(cp):
    with open(cp, "r") as file:
        ccpp = file.read()
        
    display(HTML(f"<style>{ccpp}</style>"))

def bbbbb(api_key):
    wc = [fsp, nsp]
    
    for itu in wc:
        with open(itu, "r") as anu:
            kenapa = anu.read()
            
        entah = kenapa.replace("?token=YOUR_API_KEY", f"?token={api_key}")
        with open(itu, "w") as hantu:
            hantu.write(entah)
            
def ccccc():    
    with garis1:
        display(HTML(garizzzz))
    
    kamar_kos = [
        ("conda install -y conda=24.5.0 glib gperftools openssh",
         "【 Installing Anaconda 】", "#42b02b"),
        ("conda update --all",
         "【 Installing Conda Packages 】", "yellow"),
        ("conda install -yc conda-forge python=3.10.13",
         "【 Installing Python 3.10.13 】", "#F50707"),
        ("conda clean -y --all",
         "【 Cleaning Conda 】", "cyan"),
        ("pip install torch==2.3.0+cu121 torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu121",
         "【 Installing Torch 】", "magenta"),
        ("pip install xformers==0.0.26.post1 triton psutil aria2 gdown",
         "【 Installing xformers 】", "orange")
    ]

    for aku, kamu, dia in kamar_kos:
        with susu:
            display(HTML(f"<span style='color:{dia};'>{kamu}</span>"))
        subprocess.run(shlex.split(aku), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
    with susu:
        susu.clear_output()
        garis1.clear_output()
        display(HTML('<span style="color: cyan;">【 Done 】</span>'))

    get_ipython().kernel.do_shutdown(True)

def ddddd():
    def eeeee(b):
        api_key = ink.value.strip()

        if not api_key:
            with susu:
                print("Please enter your CivitAI API KEY")
                print("CivitAI APIキーのおっぱいを入力してください。")
            return

        if len(api_key) < 32:
            with susu:
                print("API key must be at least 32 characters long")
                print("APIキーは少なくとも32オッパイの長さに達する必要があります。")
            return

        kagi = {"api_key": api_key}
        with open(uwaaah, "w") as file:
            json.dump(kagi, file)
            
        bbbbb(api_key)
        widgets.Widget.close(boxs)
        susu.clear_output()
        ccccc()
        
    sb.on_click(eeeee)
    
def fffff():
    if uwaaah.exists():
        with open(uwaaah, "r") as file:
            bau = json.load(file)
        api_key = bau.get("api_key", "")
        bbbbb(api_key)
        display(susu, garis1)
        ccccc()
        
    else:
        display(boxs, susu, garis1)
        ddddd()

aaaaa(cp)
fffff()
