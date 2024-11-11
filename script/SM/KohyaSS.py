from IPython.display import display, clear_output, Image
from ipywidgets import widgets
from IPython import get_ipython
from pathlib import Path
import subprocess, time, os, shlex, json, shutil
from nenen88 import say, download, tempe

repo = f"git clone --recursive https://github.com/bmaltais/kohya_ss KohyaSS"

HOME = Path.home()
SRC = HOME / '.gutris1'
CSS = SRC / 'setup.css'
IMG = SRC / 'loading.png'
MARK = SRC / 'marking.py'

tmp = Path('/tmp')
vnv = tmp / 'venv-kohya'
WEBUI = HOME / 'KohyaSS'

os.chdir(HOME)

def tmp_cleaning():
    for item in tmp.iterdir():
        if item.is_dir() and item != vnv:
            shutil.rmtree(item)
        elif item.is_file() and item != vnv:
            item.unlink()

def req_list():
    return [
        f"rm -rf {HOME}/tmp {HOME}/.cache/*",
        f"ln -vs /tmp {HOME}/tmp"]

def webui_req():
    time.sleep(1)
    tmp_cleaning()
    os.chdir(WEBUI)

    req = req_list()
    for lines in req:
        subprocess.run(shlex.split(lines), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    scripts = [
        f"https://github.com/gutris1/segsmaker/raw/KSS/script/SM/venv.py {WEBUI}",
        f"https://github.com/gutris1/segsmaker/raw/KSS/script/SM/Launcher.py {WEBUI}",
        f"https://github.com/gutris1/segsmaker/raw/KSS/script/SM/segsmaker.py {WEBUI}"]

    for items in scripts:
        download(items)

    tempe()

def marking(path, fn, ui):
    txt = path / fn
    values = {
        'ui': ui,
        'launch_args1': '',
        'launch_args2': '',
        'zrok_token': '',
        'ngrok_token': '',
        'tunnel': ''
    }

    if not txt.exists():
        with open(txt, 'w') as file:
            json.dump(values, file, indent=4)

    with open(txt, 'r') as file:
        data = json.load(file)

    data.update({
        'ui': ui,
        'launch_args1': '',
        'launch_args2': '',
        'tunnel': ''
    })

    with open(txt, 'w') as file:
        json.dump(data, file, indent=4)

def webui_install():
    with loading:
        display(Image(filename=str(IMG)))

    with webui_setup:
        say("<b>【{red} Installing Kohya SS GUI{d} 】{red}</b>")
        get_ipython().system(f"{repo}")

        marking(SRC, 'marking.json', 'KohyaSS')
        webui_req()
        get_ipython().run_line_magic('run', f'{MARK}')

        with loading:
            loading.clear_output(wait=True)
            get_ipython().run_line_magic('run', f'{WEBUI}/venv.py')
            
            os.chdir(WEBUI)
            os.environ["PYTHONWARNINGS"] = "ignore"
            get_ipython().system('/tmp/venv-kohya/bin/pip install -e ./sd-scripts')

            os.chdir(HOME)
            say("<b>【{red} Done{d} 】{red}</b>")

loading = widgets.Output()
webui_setup = widgets.Output()

def check_webui(ui_name, path, mark):
    if path.exists():
        print(f'{ui_name} is installed, Uninstall first.')
        get_ipython().run_line_magic('run', f'{mark}')
        return True
    return False

def webui_widgets():
    if WEBUI.exists():
        git_dir = WEBUI / '.git'
        if git_dir.exists():
            os.chdir(WEBUI)
            commit_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip().decode('utf-8')

            get_ipython().system("git pull origin master")
            get_ipython().system("git fetch --tags")

        x = [
            f"https://github.com/gutris1/segsmaker/raw/KSS/script/SM/venv.py {WEBUI}",
            f"https://github.com/gutris1/segsmaker/raw/KSS/script/SM/Launcher.py {WEBUI}",
            f"https://github.com/gutris1/segsmaker/raw/KSS/script/SM/segsmaker.py {WEBUI}"
        ]
        
        print()
        for y in x:
            download(y)

    else:
        webui_list = [
            ('A1111', HOME / 'A1111'),
            ('Forge', HOME / 'Forge'),
            ('ComfyUI', HOME / 'ComfyUI'),
            ('ReForge', HOME / 'ReForge'),
            ('FaceFusion', HOME / 'FaceFusion'),
            ('SDTrainer', HOME / 'SDTrainer')
        ]
        
        for ui_name, path in webui_list:
            if check_webui(ui_name, path, MARK):
                return

        display(webui_setup, loading)
        webui_install()

clear_output()
webui_widgets()
