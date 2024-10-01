from IPython.display import display, HTML, clear_output, Image
from IPython import get_ipython
from ipywidgets import widgets
from pathlib import Path
import subprocess, json, shlex

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

scripts = [
    f"curl -sLo {pantat} https://github.com/gutris1/segsmaker/raw/main/script/pantat88.py",
    f"curl -sLo {css} https://github.com/gutris1/segsmaker/raw/main/script/pantat88.css",
    f"curl -sLo {nenen} https://github.com/gutris1/segsmaker/raw/main/script/nenen88.py",
    f"curl -sLo {startup}/00-startup.py https://github.com/gutris1/segsmaker/raw/main/script/00-startup.py",
    f"curl -sLo {startup}/util.py https://github.com/gutris1/segsmaker/raw/main/script/util.py",
    f"curl -sLo {img} https://github.com/gutris1/segsmaker/raw/main/script/loading.png",
    f"curl -sLo {startup}/cupang.py https://github.com/gutris1/segsmaker/raw/main/script/cupang.py"
]

for items in scripts:
    subprocess.run(shlex.split(items), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

main_output = widgets.Output()

save_button = widgets.Button(description="Save")
save_button.add_class("save-button")

civitai_key_box = widgets.Text(placeholder='Enter Your Civitai API KEY Here', layout=widgets.Layout(width='350px'))
civitai_key_box.add_class("api-input")

input_widget = widgets.Box(
    [civitai_key_box, save_button], layout=widgets.Layout(
        width='500px',
        height='150px',
        display='flex',
        flex_flow='column',
        align_items='center',
        justify_content='space-around',
        padding='10px'))
input_widget.add_class("boxs")

def zrok_install():
    zrok = home / ".zrok/bin"
    if zrok.exists():
        return

    zrok.mkdir(parents=True, exist_ok=True)
    url = "https://github.com/openziti/zrok/releases/download/v0.4.32/zrok_0.4.32_linux_amd64.tar.gz"
    name = zrok / Path(url).name

    get_ipython().system(f"curl -sLo {name} {url}")
    get_ipython().system(f"tar -xzf {name} -C {zrok} --wildcards *zrok")
    get_ipython().system(f"rm -rf {home}/.cache/* {name}")

def conda_install():
    try:
        display(Image(filename=str(img)))

        cmd_list = [
            (f'rm -rf {home}/.condarc', None),
            ('conda install --repodata-fn repodata.json -qyc conda-forge conda', f'{BLUE} Installing Anaconda'),
            ('conda install --repodata-fn repodata.json -qyc conda-forge python=3.10.13', f'{CYAN} Installing Python 3.10.13'),
            ('conda install -qyc conda-forge glib gperftools openssh pv', f'{PURPLE} Installing Conda Packages'),
            ('pip install -q psutil aria2 gdown', f'{PINK} Installing Python Packages'),
            ('conda clean -qy --all', None),
            (f'rm -rf {home}/.cache/*', None)
        ]

        for cmd, msg in cmd_list:
            if msg is not None:
                print(msg)
            subprocess.run(shlex.split(cmd), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        zrok_install()

        clear_output()
        print(f"{GREEN} Done")

        get_ipython().kernel.do_shutdown(True)

    except KeyboardInterrupt:
        clear_output()
        print("^ Canceled")

def load_css():
    with open(css, "r") as file:
        panel = file.read()
        
    display(HTML(f"<style>{panel}</style>"))

def key_inject(api_key):
    target = [pantat, nenen]
    
    for line in target:
        with open(line, "r") as file:
            variable = file.read()
            
        value = variable.replace("YOUR_CIVITAI_API_KEY", f"{api_key}")
        with open(line, "w") as file:
            file.write(value)

def key_widget():
    def key_input(b):
        api_key = civitai_key_box.value.strip()

        with main_output:
            if not api_key:
                print("Please enter your CivitAI API KEY / CivitAI APIキーのおっぱいを入力してください。")
                return

            if len(api_key) < 32:
                print("API key must be at least 32 characters long / APIキーは少なくとも32オッパイの長さに達する必要があります。")
                return

            key_value = {"civitai-api-key": api_key}
            with open(key_file, "w") as file:
                json.dump(key_value, file, indent=4)

        key_inject(api_key)

        input_widget.close()
        main_output.clear_output()

        with main_output:
            conda_install()

    save_button.on_click(key_input)

def key_check():
    if key_file.exists():
        with open(key_file, "r") as file:
            value = json.load(file)

        api_key = value.get("civitai-api-key", "")
        key_inject(api_key)
        display(main_output)
        conda_install()

    else:
        display(input_widget, main_output)
        key_widget()

load_css()
key_check()
