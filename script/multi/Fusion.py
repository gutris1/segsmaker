from IPython.display import display, HTML, clear_output, Image
from ipywidgets import widgets
from IPython import get_ipython
from pathlib import Path
import subprocess, time, os, shlex, json, shutil
from nenen88 import pull, say, download, clone, tempe

repo = f"git clone https://github.com/enricogolfieri/facefusion-open facefusion"

HOME = Path.home()
SRC = HOME / '.gutris1'
CSS = SRC / 'setup.css'
IMG = SRC / 'loading.png'
MARK = SRC / 'marking.py'
setup = HOME / '.conda/setup.py'

tmp = Path('/tmp')
vnv = tmp / 'venv'

WEBUI = HOME / 'facefusion'

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

def venv_install():
    url = 'https://huggingface.co/pantat88/back_up/resolve/main/venv-fusion.tar.lz4'
    fn = Path(url).name

    def check_venv(folder):
        du = get_ipython().getoutput(f'du -s -b {folder}')
        return int(du[0].split()[0]) if du else 0

    while True:
        if vnv.exists():
            size = check_venv(vnv)
            if size < 7 * 1024**3:
                return
            get_ipython().system(f'rm -rf {vnv}/* {vnv}')

        os.chdir(tmp)

        say("<br><b>【{red} Installing VENV{d} 】{red}</b>")
        download(url)

        get_ipython().system(f'pv {fn} | lz4 -d | tar xf -')
        Path(fn).unlink()

        get_ipython().system(f'rm -rf {vnv / "bin" / "pip*"}')
        get_ipython().system(f'rm -rf {vnv / "bin" / "python*"}')
        get_ipython().system(f'python3 -m venv {vnv}')
        get_ipython().system(f'{vnv / "bin" / "python3"} -m pip install -q --upgrade --force-reinstall pip')

def req_list():
    return [
        f"rm -rf {home}/tmp {home}/.cache/*",
        f"ln -vs /tmp {home}/tmp"]

def scr_clone():
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

    with sd_setup:
        say("<b>【{red} Installing Face Fusion{d} 】{red}</b>")
        get_ipython().system(f"{repo}")

        check_ffmpeg()

        marking(SRC, 'marking.json', 'FaceFusion')
        scr_clone()
        get_ipython().run_line_magic('run', f'{MARK}')

        venv_install()
        os.chdir(HOME)

        with loading:
            loading.clear_output(wait=True)
            say("<b>【{red} Done{d} 】{red}</b>")

loading = widgets.Output()
sd_setup = widgets.Output()

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

        venv_install()

    else:
        if check_webui('A1111', HOME / 'asd', MARK):
            return
        elif check_webui('Forge', HOME / 'forge', MARK):
            return
        elif check_webui('ComfyUI', HOME / 'ComfyUI', MARK):
            return

        display(sd_setup, loading)
        webui_install()

webui_widgets()
