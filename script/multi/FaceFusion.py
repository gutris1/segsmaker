from IPython.display import display, clear_output, Image
from ipywidgets import widgets
from IPython import get_ipython
from pathlib import Path
import subprocess, time, os, shlex, json, shutil
from nenen88 import say, download, tempe

repo = f"git clone https://github.com/enricogolfieri/facefusion-open FaceFusion"

HOME = Path.home()
SRC = HOME / '.gutris1'
CSS = SRC / 'setup.css'
IMG = SRC / 'loading.png'
MARK = SRC / 'marking.py'

tmp = Path('/tmp')
vnv = tmp / 'venv-fusion'
WEBUI = HOME / 'FaceFusion'

os.chdir(HOME)

def check_ffmpeg():
    installed = get_ipython().getoutput('conda list ffmpeg')
    if not any('ffmpeg' in line for line in installed):
        cmd_list = [
            ('conda install -qyc conda-forge ffmpeg', '\ninstalling ffmpeg...'),
            ('conda clean -qy --all', None)
        ]

        for cmd, msg in cmd_list:
            if msg is not None:
                print(msg)
            subprocess.run(shlex.split(cmd), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

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
        f"https://github.com/gutris1/segsmaker/raw/main/ui/ff/launch.py {WEBUI}",
        f"https://github.com/gutris1/segsmaker/raw/main/script/venv.py {WEBUI}",
        f"https://github.com/gutris1/segsmaker/raw/main/script/multi/segsmaker.py {WEBUI}"]

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
        say("<b>【{red} Installing Face Fusion{d} 】{red}</b>")
        get_ipython().system(f"{repo}")

        check_ffmpeg()

        marking(SRC, 'marking.json', 'FaceFusion')
        webui_req()
        get_ipython().run_line_magic('run', f'{MARK}')

        with loading:
            loading.clear_output(wait=True)
            get_ipython().run_line_magic('run', f'{WEBUI}/venv.py')
            os.chdir(HOME)
            loading.clear_output(wait=True)
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
            f"https://github.com/gutris1/segsmaker/raw/main/ui/ff/launch.py {WEBUI}",
            f"https://github.com/gutris1/segsmaker/raw/main/script/venv.py {WEBUI}",
            f"https://github.com/gutris1/segsmaker/raw/main/script/multi/segsmaker.py {WEBUI}"
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
            ('SDTrainer', HOME / 'SDTrainer')
        ]
        
        for ui_name, path in webui_list:
            if check_webui(ui_name, path, MARK):
                return

        display(webui_setup, loading)
        webui_install()

clear_output()
webui_widgets()
