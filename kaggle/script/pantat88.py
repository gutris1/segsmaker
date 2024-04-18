from IPython.core.magic import register_line_magic, register_cell_magic
from IPython.display import display, HTML
from urllib.parse import urlparse
from pathlib import Path
from tqdm import tqdm
import subprocess
import zipfile
import psutil
import select
import shlex
import errno
import json
import pty
import sys
import os
import re

xxx = "/kaggle/working"
zzz = "/kaggle/working/asd"
fff = "/kaggle/venv/bin/python3"

@register_line_magic
def say(line):
    args = re.findall(r'\{[^\{\}]+\}|[^\s\{\}]+', line)
    output = []
    theme = get_ipython().config.get('InteractiveShellApp', {}).get('theme', 'light')
    default_color = 'white' if theme == 'dark' else 'black'

    i = 0
    while i < len(args):
        msg = args[i]
        color = None

        if re.match(r'^\{[^\{\}]+\}$', msg.lower()):
            color = msg[1:-1]
            msg = ""
        else:
            while i < len(args) - 1 and not re.match(r'^\{[^\{\}]+\}$', args[i + 1].lower()):
                i += 1
                msg += " " + args[i]

        if color == 'd':
            color = default_color
        elif color is None and i < len(args) - 1:
            if re.match(r'^\{[^\{\}]+\}$', args[i + 1].lower()):
                color = args[i + 1][1:-1]
                i += 1

        span_text = f"<span"
        if color:
            span_text += f" style='color:{color};'"
        span_text += f">{msg}</span>"
        output.append(span_text)
        i += 1

    display(HTML(" ".join(output)))
    
toket = ""
@register_line_magic
def download(line):
    args = line.split()
    url = args[0]

    if url.endswith('.txt'):
        with open(os.path.expanduser(url), 'r') as file:
            for line in file:
                netorare(line)
    else:
        netorare(line)
        
def strip_(url):
    if any(domain in url for domain in ["civitai.com", "huggingface.co"]):
        if '?' in url:
            url = url.split('?')[0]
            
    return url

def get_fn(url):
    fn_fn = urlparse(url)

    if any(domain in fn_fn.netloc for domain in ["civitai.com", "drive.google.com"]):
        return None
    
    else:
        fn = Path(fn_fn.path).name
        return fn
    
def netorare(line):
    hitozuma = line.strip().split()
    url = hitozuma[0].replace('\\', '')
    civ = any(domain in url for domain in ["civitai.com", "huggingface.co", "github.com"])
    togel = "drive.google.com" in url
    path, fn = "", ""
    susu = "mkdir -p {path} && cd {path} &&"
    url = strip_(url)

    if 'huggingface.co' in url and '/blob/' in url:
        url = url.replace('/blob/', '/resolve/')

    aria2c = "aria2c --header='User-Agent: Mozilla/5.0' --allow-overwrite=true --console-log-level=error --summary-interval=1 -c -x16 -s16 -k1M -j5"
        
    if len(hitozuma) >= 3:
        path, fn = os.path.expanduser(hitozuma[1]), hitozuma[2]
        os.makedirs(path, exist_ok=True)
        if civ:
            fc = f"{susu.format(path=path)} {aria2c} '{url}{toket if 'civitai.com' in url else ''}' -o '{fn}'"
            ketsuno_ana(fc, fn)
        elif togel:
            gdrown(url, path, fn)
        else:
            fc = f"{susu.format(path=path)} curl -#JL '{url}' -o '{fn}' 2>&1"
            ketsuno_ana(fc, fn)
        
    elif len(hitozuma) >= 2 and ('/' in hitozuma[1] or '~/' in hitozuma[1]):
        path = os.path.expanduser(hitozuma[1])
        os.makedirs(path, exist_ok=True)
        if civ:
            fn = get_fn(url)
            fc = f"{susu.format(path=path)} {aria2c} '{url}{toket if 'civitai.com' in url else ''}'"
            if 'civitai.com' not in url:
                fc += f" -o '{fn}'"
            ketsuno_ana(fc, fn)
        elif togel:
            gdrown(url, path)
        else:
            fn = os.path.basename(urlparse(url).path)
            fc = f"{susu.format(path=path)} curl -#OJL '{url}' 2>&1"
            ketsuno_ana(fc, fn)
            
    elif len(hitozuma) >= 2:
        fn = hitozuma[1]
        if civ:
            fc = f"{aria2c} '{url}{toket if 'civitai.com' in url else ''}' -o '{fn}'"
            ketsuno_ana(fc, fn)
        elif togel:
            gdrown(url, None, fn)
        else:
            fc = f"curl -#JL '{url}' -o '{fn}' 2>&1"
            ketsuno_ana(fc, fn)
    else:
        if civ:
            fn = get_fn(url)
            fc = f"{aria2c} '{url}{toket if 'civitai.com' in url else ''}'"
            if 'civitai.com' not in url:
                fc += f" -o '{fn}'"
            ketsuno_ana(fc, fn)
        elif togel:
            gdrown(url)
        else:
            fn = os.path.basename(urlparse(url).path)
            fc = f"curl -#OJL '{url}' 2>&1"
            ketsuno_ana(fc, fn)
    
def gdrown(url, path=None, fn=None):
    asdasd = "drive.google.com/drive/folders" in url
    susu = "mkdir -p {path} && cd {path} &&"
    
    if path and fn:
        aduuhh = os.path.expanduser(path)
        os.makedirs(aduuhh, exist_ok=True)
        awawaw = os.path.join(aduuhh, fn)
        fc = f"gdown --fuzzy {url} -O {awawaw}" + (" --folder" if asdasd else "")
        
    elif path:
        fc = f"{susu.format(path=path)} gdown --fuzzy '{url}'" + (" --folder" if asdasd else "")

    elif fn:
        fc = f"gdown --fuzzy {url} -O {fn}" + (" --folder" if asdasd else "")
        
    else:
        fc = f"gdown --fuzzy {url}" + (" --folder" if asdasd else "")

    weww, woww = pty.openpty()
    proc = subprocess.Popen(fc, stdout=woww, stderr=woww, close_fds=True, shell=True)
    os.close(woww)

    try:
        while True:
            r, _, _ = select.select([weww], [], [], 0.1)
            if r:
                six = os.read(weww, 1024).decode()
                print(six, end='')
            if proc.poll() is not None:
                all_that_remains = os.read(weww, 2048).decode()
                if all_that_remains:
                    print(all_that_remains, end='')
                break
    except OSError as e:
        pass
    finally:
        os.close(weww)

def ariari(fc, fn):
    qqqqq = subprocess.Popen(fc, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    malam = ""
    ayu_putri_kurniawan = False
    
    while True:
        petualangan = qqqqq.stdout.readline()
        if petualangan == '' and qqqqq.poll() is not None:
            break
            
        if petualangan:
            malam += petualangan
            
            for minggu in petualangan.splitlines():
                if 'errorCode' in minggu:
                    print("  " + minggu)
                    
                if re.match(r'\[#\w{6}\s.*\]', minggu):
                    sys.stdout.write("\r" + " "*80 + "\r")
                    sys.stdout.write(f"  {minggu}")
                    sys.stdout.flush()
                    ayu_putri_kurniawan = True
                    break

    if ayu_putri_kurniawan:
        print()

    kemarin = malam.find("======+====+===========")
    if kemarin != -1:
        for tidur in malam[kemarin:].splitlines():
            if "|" in tidur:
                print(f"  {tidur}")

    qqqqq.wait()

def curlly(fc, fn):  
    zura = subprocess.Popen(
        fc,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        cwd=os.getcwd())

    progress_pattern = re.compile(r'(\d+\.\d+)%')
    oppai = ""

    with tqdm(
        total=100,
        desc=f"{fn.ljust(58):>{58 + 2}}",
        initial=0,
        bar_format="{desc} 【{bar:20}】【{percentage:3.0f}%】",
        ascii="▷▶",
        file=sys.stdout
    ) as pbar:

        for line in iter(zura.stdout.readline, ''):
            if not line.startswith('  % Total') and not line.startswith('  % '):
                match = progress_pattern.search(line)
                if match:
                    progress = float(match.group(1))
                    pbar.update(progress - pbar.n)
                    pbar.refresh()

            oppai += line

        pbar.close()

    zura.wait()

    if zura.returncode != 0:
        if "curl: (23)" in oppai:
            print(f"{'':>2}^ Error: File exists. Add a custom naming after the URL or PATH to overwrite")
        elif "curl: (3)" in oppai:
            print("")
        else:
            print(f"{'':>2}^ Error: {oppai}")
    else:
        pass
    
def ketsuno_ana(fc, fn):
    try:
        if "aria2c" in fc:
            ariari(fc, fn)

        else:
            curlly(fc, fn)

    except KeyboardInterrupt:
        print(f"{'':>2}^ Canceled")
        
@register_line_magic
def clone(line):
    milkita = os.path.expanduser(line.strip())

    if not os.path.exists(milkita):
        print(f"Error: File not found - {milkita}")
        return

    with open(milkita, 'r') as file:
        for gita in map(str.strip, file):
            fc = shlex.split(gita)
            
            aaahhh = subprocess.Popen(fc, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

            while True:
                ikuuhh = aaahhh.stdout.readline()
                if not ikuuhh and aaahhh.poll() is not None:
                    break
                if ikuuhh:
                    ikuuhh = ikuuhh.strip()
                    if ikuuhh.startswith("Cloning into"):
                        print("  " + ikuuhh)

            aaahhh.wait()
            
@register_line_magic
def tempe(line):
    subprocess.run(
        f"mkdir -p /kaggle/temp/checkpoint /kaggle/temp/lora /kaggle/temp/controlnet /kaggle/temp/output /kaggle/temp/svd /kaggle/temp/z123",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL)

@register_line_magic
def delete(line):

    if 'LD_PRELOAD' in os.environ:
        del os.environ['LD_PRELOAD']
        
    indel = line.strip() if line else '/home/studio-lab-user'
    delist = [
        '/tmp/*',
        '/tmp',
        '/asd',
        '/ComfyUI',
        '/.cache/*',
        '/.config/*',
        '/.conda/*',
        '/.local/share/jupyter/runtime/*',
        '/.ipython/profile_default/*']

    subprocess.run(
        f'rm -rf {" ".join([indel + t for t in delist])}; '
        f'find {indel} -type d -name ".ipynb_checkpoints" -exec rm -rf {{}} +; ',
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL)

    nbfound = False
    try:
        findnb = f'find {indel} -type d -name ".*" -prune -o -type f -name "*.ipynb" -print'
        nbfiles = subprocess.check_output(findnb, shell=True, text=True).strip().split('\n')
        
        for nbpath in nbfiles:
            if nbpath:
                nbclear(nbpath)
                nbfound = True
                
    except subprocess.CalledProcessError:
        pass

    if nbfound:
        print("Now, Please Restart JupyterLab.")

def nbclear(nbpath):
    try:
        with open(nbpath, 'r') as f:
            nbcontent = json.load(f)

        nbcontent['metadata'] = {
            "language_info": {
                "name": ""
            },
            "kernelspec": {
                "name": "",
                "display_name": ""
            }
        }
        
        with open(nbpath, 'w') as f:
            json.dump(nbcontent, f, indent=1, sort_keys=True)

    except:
        pass

@register_line_magic
def storage(path):
    def size1(size):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"

            size /= 1024.0

    def size2(size_in_kb):
        if size_in_kb == 0:
            return "0 KB"

        base = 1024
        size_in_bytes = size_in_kb * base
        
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_in_bytes < base:
                if unit in ['B', 'KB']:
                    return f"{size_in_bytes:.0f} {unit}"
                else:
                    return f"{size_in_bytes:.1f} {unit}"
                    
            size_in_bytes /= base

    usage = psutil.disk_usage(path)
    size_str = size1(usage.total)
    used_str = size1(usage.used)
    free_str = size1(usage.free)

    used_percentage = f"{usage.percent:.1f}%".ljust(6)
    free_percentage = f"{100 - usage.percent:.1f}%".ljust(6)

    print(f"Size = {size_str:>8}")
    print(f"Used = {used_str:>8} | {used_percentage}")
    print(f"Free = {free_str:>8} | {free_percentage}")
    print()

    du_process = os.popen(f'du -h -k --max-depth=1 {path}')
    du_output = du_process.read()
    lines = du_output.split('\n')
    paths = [line.split('\t')[1] for line in lines if line]
    sizes_kb = [int(line.split('\t')[0]) for line in lines if line]

    for path, size_kb in zip(paths, sizes_kb):
        formatted_size = size2(size_kb)
        base_path = path.split(os.path.sep)[-1]

        if base_path != 'studio-lab-user':
            padding = " " * max(0, 9 - len(formatted_size))
            print(f"/{base_path:<25} {padding}{formatted_size}")

    du_process.close()

@register_line_magic
def pull(line):
    args = line.split()
    if len(args) != 3:
        return

    repo, tarfold, despath = args

    path = os.path.expanduser(despath)
    prok = {'stdout': subprocess.PIPE, 'stderr': subprocess.PIPE, 'check': True}
    kont = subprocess.run
    kont(['git', 'clone', '-n', '--depth=1', '--filter=tree:0', repo], cwd=path, **prok)
    repofold = os.path.join(path, os.path.basename(repo.rstrip('.git')))
    kont(['git', 'sparse-checkout', 'set', '--no-cone', tarfold], cwd=repofold, **prok)
    kont(['git', 'checkout'], cwd=repofold, **prok)

    zipin = os.path.join(repofold, 'kaggle', tarfold)
    zipout = os.path.join(path, f'{tarfold}.zip')
    
    with zipfile.ZipFile(zipout, 'w') as zipf:
        for root, dirs, files in os.walk(zipin):
            for file in files:
                zp = os.path.join(root, file)
                arcname = os.path.relpath(zp, zipin)
                zipf.write(zp, arcname=arcname)

    kont(['unzip', '-o', zipout], cwd=path, **prok)
    os.remove(zipout)
    kont(['rm', '-rf', repofold], cwd=path, **prok)
    
@register_cell_magic
def zipping(line, cell):
    lines = cell.strip().split('\n')

    input_path = None
    output_path = None

    for line in lines:
        soup = line.split('=')
        
        if len(soup) == 2:
            arg_name = soup[0].strip()
            arg_value = soup[1].strip().strip("'")

            if arg_name == 'input_folder':
                input_path = arg_value
                
            elif arg_name == 'output_folder':
                output_path = arg_value

    if not os.path.exists(input_path):
        print(f"Error: '{input_path}' does not exist.")
        return

    def zip_folder(
        input_path,
        output_path,
        max_size_mb=20):
        
        os.makedirs(
            output_path,
            exist_ok=True)
        
        all_files = []
        
        for root, dirs, files in os.walk(input_path):
            
            for file in files:
                file_path = os.path.join(root, file)
                all_files.append(file_path)

        zip_number = 1
        current_zip_size = 0
        current_zip_name = os.path.join(
            output_path,
            f"part_{zip_number}.zip")

        with tqdm(
            total=len(all_files),
            desc='zipping : ',
            bar_format='{desc}[{bar:26}] [{n_fmt}/{total_fmt}]',
            ascii="▷▶",
            file=sys.stdout) as pbar:
            
            with zipfile.ZipFile(
                current_zip_name,
                'w',
                compression=zipfile.ZIP_DEFLATED) as current_zip:
                
                for file_path in all_files:
                    file_size = os.path.getsize(file_path)

                    if current_zip_size + file_size > max_size_mb * 1024 * 1024:
                        current_zip.close()
                        
                        zip_number += 1
                        
                        current_zip_name = os.path.join(
                            output_path,
                            f"part_{zip_number}.zip")
                        
                        current_zip = zipfile.ZipFile(
                            current_zip_name,
                            'w',
                            compression=zipfile.ZIP_DEFLATED)
                        
                        current_zip_size = 0

                    current_zip.write(
                        file_path,
                        os.path.relpath(
                            file_path,
                            input_path))
                    
                    current_zip_size += file_size
                    pbar.update(1)

    max_size_mb = 200
    zip_folder(input_path, output_path, max_size_mb)
