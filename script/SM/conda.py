from IPython.display import display, HTML, clear_output, Image
from IPython import get_ipython
from ipywidgets import widgets
from pathlib import Path
import subprocess
import json

home = Path.home()
src = home / ".gutris1"
css = src / "pantat88.css"
startup = home / ".ipython/profile_default/startup"
nenen = startup / "nenen88.py"
pantat = startup / "pantat88.py"
key_file = src / "api-key.json"
img = src / "loading.png"

R = "\033[0m"
T = f"▶{R}"
BLUE = f"\033[38;5;33m{T}"
CYAN = f"\033[36m{T}"
PURPLE = f"\033[38;5;135m{T}"
PINK = f"\033[38;5;201m{T}"
RED = f"\033[31m{T}"
GREEN = f"\033[38;5;35m{T}"

Path(src).mkdir(parents=True, exist_ok=True)

SyS = get_ipython().system

main_output = widgets.Output()

save_button = widgets.Button(description="Save")
save_button.add_class("save-button")

civitai_key_box = widgets.Text(placeholder='Enter Your Civitai API Key Here', layout=widgets.Layout(width='350px'))
civitai_key_box.add_class("api-input")

hf_token_box = widgets.Text(placeholder='Huggingface READ Token (optional)', layout=widgets.Layout(width='350px'))
hf_token_box.add_class("api-input")

input_widget = widgets.Box(
    [civitai_key_box, hf_token_box, save_button], 
    layout=widgets.Layout(
        width='500px',
        height='200px',
        display='flex',
        flex_flow='column',
        align_items='center',
        justify_content='space-around',
        padding='10px'
    )
)
input_widget.add_class("boxs")

def CondaInstall():
    try:
        display(Image(filename=str(img)))

        cmd_list = [
            (f'rm -rf {home}/.condarc', None),
            ('conda config --remove-key channels', None),
            ('conda install --repodata-fn repodata.json -qy conda curl', f'{BLUE} Installing Anaconda'),
            ('conda install --repodata-fn repodata.json -qy python=3.10', f'{CYAN} Installing Python 3.10'),
            ('conda install -qy glib gperftools openssh pv gputil', f'{PURPLE} Installing Conda Packages'),
            ('pip install -q psutil aria2 gdown', f'{PINK} Installing Python Packages'),
            ('conda clean -qy --all', None),
            (f'rm -rf {home}/.cache/* {home}/.condarc', None)
        ]

        for cmd, msg in cmd_list:
            if msg is not None:
                print(msg)
            SyS(f'{cmd} > /dev/null 2>&1')

        clear_output()
        print(f"{GREEN} Done")

        get_ipython().kernel.do_shutdown(True)

    except KeyboardInterrupt:
        clear_output()
        print("^ Canceled")

def LoadCSS(): 
    display(HTML(f"<style>{open(css).read()}</style>"))

def KeyInject(civitai_key, hf_token):
    for sc in [
        f'curl -sLo {pantat} https://github.com/gutris1/segsmaker/raw/main/script/SM/pantat88.py',
        f'curl -sLo {nenen} https://github.com/gutris1/segsmaker/raw/main/script/SM/nenen88.py'
    ]:
        SyS(f'{sc} > /dev/null 2>&1')

    target = [pantat, nenen]

    for line in target:
        with open(line, 'r') as file:
            v = file.read()

        v = v.replace('toket = ""', f'toket = "{civitai_key}"')
        v = v.replace('tobrut = ""', f'tobrut = "{hf_token}"')

        with open(line, "w") as file:
            file.write(v)

def KeyWidget(civitai_key='', hf_token=''):
    civitai_key_box.value = civitai_key
    hf_token_box.value = hf_token

    def KeyInputs(b):
        civitai_key = civitai_key_box.value.strip()
        hf_token = hf_token_box.value.strip()

        with main_output:
            if not civitai_key:
                print("Please enter your Civitai API Key")
                return

            if len(civitai_key) < 32:
                print("API key must be at least 32 characters long")
                return

            civitai_key_value = {"civitai-api-key": civitai_key}
            hf_token_value = {"huggingface-read-token": hf_token}

            secrets = {**civitai_key_value, **hf_token_value}
            with open(key_file, "w") as file:
                json.dump(secrets, file, indent=4)

        KeyInject(civitai_key, hf_token)

        input_widget.close()
        main_output.clear_output()

        p = subprocess.run(["conda", "--version"], capture_output=True, text=True, check=True)
        cv = p.stdout.strip().split()[1]
        mv = int(cv.split('.')[0])
        
        with main_output:
            if mv < 24:
                CondaInstall()
            else:
                print(f"{GREEN} Done")
                get_ipython().kernel.do_shutdown(True)

    save_button.on_click(KeyInputs)

def KeyCheck():
    if key_file.exists():
        with open(key_file, "r") as file:
            value = json.load(file)

        civitai_key = value.get("civitai-api-key", "")
        hf_token = value.get("huggingface-read-token", "")

        if not civitai_key or not hf_token:
            display(input_widget, main_output)
            KeyWidget(civitai_key, hf_token)
        else:
            KeyInject(civitai_key, hf_token)
            display(main_output)
            CondaInstall()
    else:
        display(input_widget, main_output)
        KeyWidget()

def Scripts():
    for scr in [
        f'curl -sLo {css} https://github.com/gutris1/segsmaker/raw/main/script/SM/pantat88.css',
        f'curl -sLo {startup}/00-startup.py https://github.com/gutris1/segsmaker/raw/main/script/SM/00-startup.py',
        f'curl -sLo {startup}/util.py https://github.com/gutris1/segsmaker/raw/main/script/SM/util.py',
        f'curl -sLo {img} https://github.com/gutris1/segsmaker/raw/main/script/SM/loading.png',
        f'curl -sLo {startup}/cupang.py https://github.com/gutris1/segsmaker/raw/main/script/SM/cupang.py'
    ]:
        SyS(f'{scr} > /dev/null 2>&1')

Scripts()
LoadCSS()
KeyCheck()
