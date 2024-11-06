from IPython import get_ipython
from pathlib import Path
from nenen88 import tempe, say, download
from KANDANG import HOMEPATH, TEMPPATH, VENVPATH, BASEPATH
import subprocess, os, shlex, errno

HOME = Path(HOMEPATH)
tmp = Path(TEMPPATH)
vnv = Path(VENVPATH)

url = 'https://huggingface.co/pantat88/back_up/resolve/main/venv-torch241-cu121.tar.lz4'
fn = Path(url).name

need_space = 14 * 1024**3

def check_venv(folder):
    du = get_ipython().getoutput(f'du -s -b {folder}')
    return int(du[0].split()[0]) if du else 0

def check_tmp(path):
    stats = os.statvfs(path)
    return stats.f_frsize * stats.f_bavail

def listing(directory):
    return [(Path(root) / file, (Path(root) / file).stat().st_size) 
            for root, _, files in os.walk(directory) for file in files]

def removing(directory, req_space):
    files = listing(directory)
    files.sort(key=lambda x: x[1], reverse=True)
    freed_space = 0

    for file_path, size in files:
        if freed_space >= req_space:
            break

        print(f'Removing {file_path}')
        get_ipython().system(f'rm -rf {file_path}')
        freed_space += size

    return freed_space

def she_bang():
    vnv_bin = vnv / 'bin'
    old_shebang = b'#!/home/studio-lab-user/tmp/venv/bin/python3\n'
    new_shebang = f"#!{vnv}/bin/python3\n"
    
    for script in vnv_bin.glob('*'):
        if script.is_file():
            try:
                with open(script, 'r+b') as file:
                    lines = file.readlines()
                    if lines and lines[0] == old_shebang:
                        lines[0] = new_shebang.encode('utf-8')
                        file.seek(0)
                        file.writelines(lines)
                        file.truncate()

            except OSError as e:
                if e.errno == 26:
                    pass

def venv_install():
    while True:
        if vnv.exists():
            size = check_venv(vnv)
            if size > 7 * 1024**3:
                return
            get_ipython().system(f'rm -rf {vnv}/* {vnv}')

        free_space = check_tmp(tmp)
        req_space = need_space - free_space

        if req_space > 0:
            print(f'Need space {req_space / 1024**3:.1f} GB for venv')
            req_space -= removing(tmp / 'ckpt', req_space)
            if req_space > 0:
                req_space -= removing(tmp / 'lora', req_space)
            if req_space > 0:
                req_space -= removing(tmp / 'controlnet', req_space)

        os.chdir(BASEPATH)
        say('<br>【{red} Installing VENV{d} 】{red}')
        download(url)

        if BASEPATH == '/content':
            z = ["apt -y install python3.10-venv", "apt -y install lz4"]
            for b in z:
                subprocess.run(shlex.split(b), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
        get_ipython().system(f'pv {fn} | lz4 -d | tar xf -')
        Path(fn).unlink()

        get_ipython().system(f'rm -rf {vnv}/bin/pip*')
        get_ipython().system(f'rm -rf {vnv}/bin/python*')
        get_ipython().system(f'python3 -m venv {vnv}')
        get_ipython().system(f'{vnv}/bin/python3 -m pip install -q -U --force-reinstall pip')

        if BASEPATH == '/content':
            get_ipython().system(f'{vnv}/bin/pip3 install -q ipykernel')

tempe()
venv_install()
she_bang()
os.chdir(HOME)
