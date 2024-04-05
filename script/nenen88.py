from IPython.display import display, HTML
from urllib.parse import urlparse
from IPython import get_ipython
from pathlib import Path
from tqdm import tqdm
import subprocess
import zipfile
import select
import shlex
import errno
import pty
import sys
import os
import re

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
    
toket = "?token=YOUR_API_KEY"
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
    if '?' in url:
        url = url.split('?')[0]
    return url

def get_fn(url):
    fn_fn = urlparse(url)

    if "civitai.com" in fn_fn.netloc or "drive.google.com" in fn_fn.netloc:
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
            print(f"{'':>2}^ File already exists; download skipped. Append a custom name after the URL or PATH to overwrite.")
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

def tempe():
    subprocess.run(
        f"mkdir -p /tmp/models /tmp/Lora /tmp/ControlNet /tmp/svd /tmp/z123",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL)

def pull(line):
    args = line.split()
    if len(args) != 3:
        return

    repo, tarfold, despath = args

    path = os.path.expanduser(despath)
    xxx = {'stdout': subprocess.PIPE, 'stderr': subprocess.PIPE, 'check': True}
    zzz = subprocess.run
    zzz(['git', 'clone', '-n', '--depth=1', '--filter=tree:0', repo], cwd=path, **xxx)
    repofold = os.path.join(path, os.path.basename(repo.rstrip('.git')))
    zzz(['git', 'sparse-checkout', 'set', '--no-cone', tarfold], cwd=repofold, **xxx)
    zzz(['git', 'checkout'], cwd=repofold, **xxx)

    zipin = os.path.join(repofold, 'ui', tarfold)
    zipout = os.path.join(path, f'{tarfold}.zip')
    
    with zipfile.ZipFile(zipout, 'w') as zipf:
        for root, dirs, files in os.walk(zipin):
            for file in files:
                zp = os.path.join(root, file)
                arcname = os.path.relpath(zp, zipin)
                zipf.write(zp, arcname=arcname)

    zzz(['unzip', '-o', zipout], cwd=path, **xxx)
    os.remove(zipout)
    zzz(['rm', '-rf', repofold], cwd=path, **xxx)
