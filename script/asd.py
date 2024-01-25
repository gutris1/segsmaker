from IPython.core.magic import register_line_magic, register_cell_magic
from IPython.display import display, HTML
from urllib.parse import urlparse
from tqdm import tqdm
import subprocess
import zipfile
import psutil
import shlex
import sys
import os
import re
    
@register_line_magic
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
@register_line_magic
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

        ketsuno_ana(fc, fn, use_auth="civitai.com" in urlll)

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
            desc=f"{fn.ljust(56)}",
            initial=0,
            bar_format="{desc} [{bar:20}] [{percentage:3.0f}%]",
            ascii="▷▶",
            file=sys.stdout) as pbar:

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
                print("^ Error: File exists. Add a custom naming after the URL or PATH to overwrite")
            elif "curl: (3)" in oppai:
                print("")
            else:
                print(f"^ Error: {oppai}")

        else:
            pass
        
    except UnicodeDecodeError:
        print("^ Error: Remove '?type=Model&format=SafeTensor&size=pruned&fp=fp16' from the civitai URL")
    
    except KeyboardInterrupt:
        print("^ Canceled")

@register_line_magic
def clone(line):
    file_path = os.path.expanduser(line.strip())

    if not os.path.exists(file_path):
        print(f"Error: File not found - {file_path}")
        return

    with open(file_path, 'r') as file:
        for git_command in map(str.strip, file):
            command_list = shlex.split(git_command)
            subprocess.run(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
@register_line_magic
def tempe(line):
    subprocess.run(
        f"mkdir -p /tmp/models /tmp/Lora /tmp/ControlNet",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL)

@register_line_magic
def delete(line):
    input_path = line.strip() if line else '/home/studio-lab-user'
    targets = [
        '/tmp/*',
        '/tmp',
        '/asd',
        '/ComfyUI',
        '/.cache/*',
        '/.config/*',
        '/.conda/*',
        '/.local/share/jupyter/runtime/*',
        '/.ipython/profile_default/startup/*']

    subprocess.run(
        f'rm -rf {" ".join([input_path + t for t in targets])}; '
        f'find {input_path} -type d -name ".ipynb_checkpoints" -exec rm -rf {{}} +; '
        f'find {input_path}/* -type f ! -name "*.ipynb" -exec rm -rf {{}} +; '
        f'find {input_path}/* -type d -empty -delete',
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL)

    print("Now please restart JupyterLab.")

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
            print(f"/{base_path:<20} {padding}{formatted_size}")

    du_process.close()

@register_line_magic
def pull(line):
    args = line.split()
    if len(args) != 3:
        return

    rp, dp, tf = args

    path = os.path.expanduser(dp)
    xxx = {'stdout': subprocess.PIPE, 'stderr': subprocess.PIPE, 'check': True}
    zzz = subprocess.run
    zzz(['git', 'clone', '-n', '--depth=1', '--filter=tree:0', rp], cwd=path, **xxx)
    rf = os.path.join(path, os.path.basename(rp.rstrip('.git')))
    zzz(['git', 'sparse-checkout', 'set', '--no-cone', tf], cwd=rf, **xxx)
    zzz(['git', 'checkout'], cwd=rf, **xxx)

    zipin = os.path.join(rf, 'ui', tf)
    zipout = os.path.join(path, f'{tf}.zip')
    
    with zipfile.ZipFile(zipout, 'w') as zipf:
        for root, dirs, files in os.walk(zipin):
            for file in files:
                zp = os.path.join(root, file)
                arcname = os.path.relpath(zp, zipin)
                zipf.write(zp, arcname=arcname)

    zzz(['unzip', '-o', zipout], cwd=path, **xxx)
    os.remove(zipout)
    zzz(['rm', '-rf', rf], cwd=path, **xxx)
    
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
