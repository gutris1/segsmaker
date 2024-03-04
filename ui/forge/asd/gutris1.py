from IPython.display import display, HTML
from urllib.parse import urlparse
from tqdm import tqdm
import subprocess
import shlex
import sys
import os
import re
    
def say(line):
    args = line.split()
    output = []
    theme = get_ipython().config.get('InteractiveShellApp', {}).get('theme', 'light')
    default_color = 'white' if theme == 'dark' else 'black'

    i = 0
    while i < len(args):
        msg = args[i]
        color = None

        if re.match(r'^\{[^\{\}]+\}$', args[i].lower()):
            color = args[i][1:-1]
            msg = ""

        while i < len(args) - 1 and not re.match(r'^\{[^\{\}]+\}$', args[i + 1].lower()):
            msg += " " + args[i + 1]
            i += 1

        if color == '{d}':
            color = default_color
            
        elif not color or '{d}':
            if i < len(args) - 1 and re.match(r'^\{[^\{\}]+\}$', args[i + 1].lower()):
                color = args[i + 1][1:-1]
                i += 1
                
            else:
                msg = line

        span_text = f"<span"
        if color:
            span_text += f" style='color:{color};'"

        span_text += f">{msg}</span>"
        output.append(span_text)
        i += 1

    display(HTML(" ".join(output)))

momoiro = "-H 'Authorization: Bearer 268143672c63a79e3fbf7fa8e9c72603'"
def download(line):
    args = line.split()
    url, auth = args[0], momoiro if "civitai.com" in args[0] else ""

    if len(args) == 1:
        if args[0].endswith('.txt'):
            with open(os.path.expanduser(args[0]), 'r') as file:
                for line in file:
                    netorare(line, auth)
        else:
            fn = os.path.basename(urlparse(args[0]).path)
            fc = f"curl -#OJL {auth} {args[0]} 2>&1"
            ketsuno_ana(fc, fn)

    elif len(args) == 3:
        path, fn = args[1], args[2]
        os.makedirs(path, exist_ok=True)
        fc = f"mkdir -p {path} && cd {path} && curl -#JL {auth} {url} -o {fn} 2>&1"
        ketsuno_ana(fc, fn)

    elif len(args) > 1 and ('/' in args[1] or '~/' in args[1]):
        path = args[1]
        os.makedirs(path, exist_ok=True)
        fn = os.path.basename(urlparse(args[0]).path)
        url = url.replace('\\', '')
        fc = f"mkdir -p {path} && cd {path} && curl -#OJL {auth} {url} -o {fn} 2>&1"
        ketsuno_ana(fc, fn)

    else:
        fn = args[1]
        fc = f"curl -#JL {auth} {args[0]} -o {fn} 2>&1"
        ketsuno_ana(fc, fn)

def netorare(line, auth):
    hitozuma = line.strip().split()

    if len(hitozuma) >= 1:
        urlll = hitozuma[0].replace('\\', '')
        path, fn = "", ""

        if len(hitozuma) >= 3:
            path, fn = hitozuma[1], hitozuma[2]
        elif len(hitozuma) >= 2 and ('/' in hitozuma[1] or '~/' in hitozuma[1]):
            path = hitozuma[1]
            fn = os.path.basename(urlparse(urlll).path)
        elif len(hitozuma) >= 2:
            fn = hitozuma[1]

        fn = fn or os.path.basename(urlparse(urlll).path)

        use_auth = "civitai.com" in urlll
        auth = momoiro if use_auth else ""

        if path and fn:
            os.makedirs(path, exist_ok=True)
            fc = f"mkdir -p {path} && cd {path} && curl -#JL {auth} {urlll} -o {fn} 2>&1"
            
        elif path:
            os.makedirs(path, exist_ok=True)
            fc = f"mkdir -p {path} && cd {path} && curl -#OJL {auth} {urlll} -o {fn} 2>&1"
            
        elif fn:
            fc = f"curl -#JL {auth} {urlll} -o {fn} 2>&1"
            
        else:
            fc = f"curl -#OJL {auth} {urlll} 2>&1"

        ketsuno_ana(fc, fn, use_auth=use_auth)

def ketsuno_ana(fc, fn, use_auth=False):
    try:
        auth = momoiro if use_auth else ""
        fc = f"{fc.replace('#OJL', '#OJL ' + auth)}"

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
        
    except UnicodeDecodeError:
        print(f"{'':>2}^ Error: Remove '?type=Model&format=SafeTensor&size=pruned&fp=fp16' from the civitai URL")
    
    except KeyboardInterrupt:
        print(f"{'':>2}^ Canceled")

def clone(line):
    file_path = os.path.expanduser(line.strip())

    if not os.path.exists(file_path):
        print(f"Error: File not found - {file_path}")
        return

    with open(file_path, 'r') as file:
        for git_command in map(str.strip, file):
            command_list = shlex.split(git_command)
            subprocess.run(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
def tempe(line):
    subprocess.run(
        f"mkdir -p /tmp/models /tmp/Lora /tmp/ControlNet",
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