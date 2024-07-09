from ipywidgets import widgets
from IPython.display import display, HTML, clear_output, Image
from IPython import get_ipython
from pathlib import Path
import subprocess, json, shlex

home = Path.home()
css = home / ".conda/pantat88.css"
startup = home / ".ipython/profile_default/startup"
nenen = startup / "nenen88.py"
pantat = startup / "pantat88.py"
key_path = home / ".your-civitai-api-key"
key_file = key_path / "api_key.json"
img = home / ".conda/loading.png"

R = "\033[0m"
T = f"▶{R}"
BLUE = f"\033[38;5;33m{T}"
CYAN = f"\033[36m{T}"
PURPLE = f"\033[38;5;135m{T}"
PINK = f"\033[38;5;201m{T}"
RED = f"\033[31m{T}"
GREEN = f"\033[38;5;35m{T}"

Path(key_path).mkdir(parents=True, exist_ok=True)

scripts = [
    f"curl -sLo {pantat} https://github.com/gutris1/segsmaker/raw/main/script/pantat88.py",
    f"curl -sLo {css} https://github.com/gutris1/segsmaker/raw/main/script/pantat88.css",
    f"curl -sLo {nenen} https://github.com/gutris1/segsmaker/raw/main/script/nenen88.py",
    f"curl -sLo {startup}/00-startup.py https://github.com/gutris1/segsmaker/raw/main/script/00-startup.py",
    f"curl -sLo {startup}/util.py https://github.com/gutris1/segsmaker/raw/main/script/util.py",
    f"curl -sLo {startup}/py.py https://github.com/gutris1/segsmaker/raw/main/script/py.py",
    f"curl -sLo {img} https://github.com/gutris1/segsmaker/raw/main/script/loading.png"
]

for items in scripts:
    subprocess.run(shlex.split(items), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

main_output = widgets.Output()

save_button = widgets.Button(description="Save")
save_button.add_class("save-button")

input_box = widgets.Text(placeholder='Enter Your Civitai API KEY Here')
input_box.add_class("api-input")

input_widget = widgets.VBox([input_box, save_button],
                            layout=widgets.Layout(
                                width='450px',
                                height='150px',
                                display='flex',
                                flex_flow='column',
                                align_items='center',
                                justify_content='space-around',
                                padding='20px'))
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

        conda_list = [
            ("conda install -yc conda-forge conda", f"{BLUE} Installing Anaconda"),
            ("conda install -yc conda-forge glib gperftools openssh pv", f"{CYAN} Installing Conda Packages"),
            ("conda install -yc conda-forge python=3.10.13", f"{PURPLE} Installing Python 3.10.13"),
            ("pip install psutil aria2 gdown", f"{PINK} Installing Python Packages"),
            ("conda clean -y --all", f"{RED} Cleaning")
        ]

        for cmd, txts in conda_list:
            print(f'{txts}')
            subprocess.run(shlex.split(cmd), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        get_ipython().system('rm -rf /home/studio-lab-user/.cache/*')
        zrok_install()

        clear_output()
        print(f"{GREEN} Done")

        get_ipython().kernel.do_shutdown(True)

    except KeyboardInterrupt:
        clear_output()
        print("^ Canceled")

def load_css(css):
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
    def column(b):
        api_key = input_box.value.strip()

        with main_output:
            if not api_key:
                print("Please enter your CivitAI API KEY / CivitAI APIキーのおっぱいを入力してください。")
                return

            if len(api_key) < 32:
                print("API key must be at least 32 characters long / APIキーは少なくとも32オッパイの長さに達する必要があります。")
                return

            key_value = {"api_key": api_key}
            with open(key_file, "w") as file:
                json.dump(key_value, file)

        key_inject(api_key)

        input_widget.close()
        main_output.clear_output()

        with main_output:
            conda_install()

    save_button.on_click(column)

def key_check():
    if key_file.exists():
        with open(key_file, "r") as file:
            value = json.load(file)

        api_key = value.get("api_key", "")
        key_inject(api_key)
        display(main_output)
        conda_install()

    else:
        display(input_widget, main_output)
        key_widget()

load_css(css)
key_check()