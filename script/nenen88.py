from IPython.core.magic import register_line_magic
from IPython.display import display, HTML
from urllib.parse import urlparse
from IPython import get_ipython
from pathlib import Path
from tqdm import tqdm
import subprocess
import requests
import zipfile
import shlex
import json
import sys
import re
import os
import io

MAGENTA = '\033[35m'
RED = '\033[31m'
CYAN = '\033[36m'
GREEN = '\033[38;5;35m'
YELLOW = '\033[33m'
BLUE = '\033[38;5;69m'
PURPLE = '\033[38;5;135m'
ORANGE = '\033[38;5;208m'
RESET = '\033[0m'

CD = os.chdir
SyS = get_ipython().system
iRON = os.environ

KAGGLE = 'KAGGLE_DATA_PROXY_TOKEN' in iRON

TOKET = ''
TOBRUT = ''

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
            msg = ''
        else:
            while i < len(args) - 1 and not re.match(r'^\{[^\{\}]+\}$', args[i + 1].lower()):
                i += 1
                msg += ' ' + args[i]

        if color == 'd':
            color = default_color
        elif color is None and i < len(args) - 1:
            if re.match(r'^\{[^\{\}]+\}$', args[i + 1].lower()):
                color = args[i + 1][1:-1]
                i += 1

        span_text = f'<span'
        if color:
            span_text += f" style='color:{color};'"
        span_text += f'>{msg}</span>'
        output.append(span_text)
        i += 1

    display(HTML(' '.join(output)))

def resizer(b, size=512):
    from PIL import Image
    i = Image.open(io.BytesIO(b))
    w, h = i.size
    s = (size, int(h * size / w)) if w > h else (int(w * size / h), size)
    o = io.BytesIO()
    i.resize(s, Image.LANCZOS).save(o, format='PNG')
    o.seek(0)
    return o

def civitai_headers():
    return {'User-Agent': 'CivitaiLink:Automatic1111'}

def civitai_preview(j, p, fn):
    v = j['modelVersions'][0] if 'modelVersions' in j else j
    images = v.get('images', [])
    name = fn or v.get('files', [{}])[0].get('name')
    path = Path(p) / f'{Path(name).stem}.preview.png'
    if path.exists(): return

    preview = next((img.get('url', '') for img in images if not img.get('url', '').lower().endswith(('.mp4', '.gif'))), None)
    if not preview: return

    r = requests.get(preview, headers=civitai_headers()).content
    resized = resizer(r)

    if KAGGLE:
        from melon00 import image_encryption
        image_encryption(resized, path)
    else:
        path.write_bytes(resized.read())

def civitai_infotags(j, p, fn):
    if 'modelVersions' in j:
        modelId = j.get('id')
        v = j['modelVersions'][0]
    else:
        v = j
        modelId = v.get('modelId')

    name = fn or v.get('files', [{}])[0].get('name')
    info = Path(p) / f'{Path(name).stem}.json'
    if info.exists(): return

    baseList = {
        'SD 1': 'SD1',
        'SD 1.5': 'SD1',
        'SD 2': 'SD2',
        'SD 3': 'SD3',
        'SDXL': 'SDXL',
        'Pony': 'SDXL',
        'Illustrious': 'SDXL',
    }

    data = {
        'activation text': ', '.join(v.get('trainedWords', [])),
        'sd version': next((s for k, s in baseList.items() if k in v['baseModel']), ''),
        'modelId': modelId,
        'modelVersionId': v.get('id'),
        'sha256': v.get('files', [{}])[0].get('hashes', {}).get('SHA256')
    }

    info.write_text(json.dumps(data, indent=4))

def civitai_earlyAccess(j):
    v = None

    if 'modelVersions' in j:
        v = next((v for v in j.get('modelVersions', []) if v.get('availability') == 'EarlyAccess'), None)
        modelId = j.get('id')
    elif j.get('earlyAccessEndsAt'):
        v = j
        modelId = v.get('modelId')

    if v:
        modelVersionId = v.get('id')
        page = f'https://civitai.com/models/{modelId}?modelVersionId={modelVersionId}'
        print(f'{page}\n-> The model is in early access and requires payment for downloading.')
        return True

    return False

@register_line_magic
def download(line):
    args = line.split()
    if not args:
        print('  missing URL, downloading nothing')
        return

    url = args[0]
    path = Path(url).expanduser()
    if url.endswith('.txt') and path.is_file():
        for line in path.read_text(encoding='utf-8').splitlines():
            netorare(line)
    else:
        netorare(line)

def get_fn(url):
    if any(x in url for x in ['civitai.com', 'drive.google.com']):
        return None
    return Path(urlparse(url).path).name

def strip_(url, fn):
    j = None

    if 'github.com' in url: url = url.replace('/blob/', '/raw/')

    elif 'huggingface.co' in url:
        url = url.split('?')[0]
        h = {'User-Agent': 'Mozilla/5.0', **({'Authorization': f'Bearer {TOBRUT}'} if TOBRUT else {})}
        ext = ['.safetensors', '.pt', '.pth']

        if fn and Path(fn).suffix.lower() in ext:
            response = requests.get(re.sub(r'/(resolve|blob)/', '/raw/', url), headers=h)
            t = re.search(r'oid sha256:([a-fA-F0-9]{64})', response.text)
            if t:
                sha256 = t.group(1)
                api_url = f'https://civitai.com/api/v1/model-versions/by-hash/{sha256}'
                j = requests.get(api_url, headers=civitai_headers()).json()
                r = next((f for f in j.get('files', []) if f.get('hashes', {}).get('SHA256', '').lower() == sha256.lower()), None)
                if not r: j = None

        url = url.replace('/blob/', '/resolve/')

    elif 'civitai.com' in url:
        input_url = url
        url = url.split('?token=')[0] if '?token=' in url else url

        if 'civitai.com/api/download/models/' in url:
            use_input = True
            versionId = url.split('models/')[1].split('/')[0].split('?')[0]
            api_url = f'https://civitai.com/api/v1/model-versions/{versionId}'

        elif 'civitai.com/models/' in url:
            use_input = False
            modelId = url.split('models/')[1].split('/')[0].split('?')[0]
            versionId = url.split('?modelVersionId=')[1] if '?modelVersionId=' in url else None

            if versionId: api_url = f'https://civitai.com/api/v1/model-versions/{versionId}'
            else: api_url = f'https://civitai.com/api/v1/models/{modelId}'

        j = requests.get(api_url, headers=civitai_headers()).json()

        msg = civitai_earlyAccess(j)
        if msg: return None, None

        url = input_url if use_input else (j.get('modelVersions', [{}])[0] if 'modelVersions' in j else j).get('downloadUrl')
        if not url: print(f'Unable to find download URL for\n-> {input_url}\n'); return None, None

        url = url.replace('?type=', f'?token={TOKET}&type=') if '?type=' in url else f'{url}?token={TOKET}'

    return url, j

def netorare(line):
    parts = line.strip().split()
    if not parts: return

    fp, fn = None, None
    cwd = Path.cwd()
    url = parts[0].replace('\\', '')

    CHG = any(domain in url for domain in ['civitai.com', 'huggingface.co', 'github.com'])
    DriveGoogle = 'drive.google.com' in url

    path = lambda s: '/' in s or '~/' in s

    try:
        if len(parts) >= 3:
            arg1, arg2 = parts[1], parts[2]
            path_arg, file_arg = (arg2, arg1) if path(arg2) and not path(arg1) else \
                                 (arg1, arg2) if path(arg1) and not path(arg2) else \
                                 (arg2, arg1) if Path(arg2).suffix == '' and Path(arg1).suffix != '' else \
                                 (arg1, arg2)

            fp, fn = Path(path_arg).expanduser(), file_arg
            fp.mkdir(parents=True, exist_ok=True)
            CD(fp)

        elif len(parts) == 2:
            arg = parts[1]
            if path(arg):
                fp = Path(arg).expanduser()
                fp.mkdir(parents=True, exist_ok=True)
                CD(fp)
                fn = get_fn(url) if CHG else Path(urlparse(url).path).name
            else:
                fn = arg
                fp = cwd
        else:
            fn = get_fn(url) if CHG else Path(urlparse(url).path).name
            fp = cwd

        if CHG: ariari(url, fp, fn)
        elif DriveGoogle: gdrown(url, fp, fn)
        else:
            path_only = len(parts) == 2 and fp is not None
            cmd = f"curl -#{'OJL' if len(parts) == 1 or path_only else 'JL'} '{url}'" + (f" -o '{fn}'" if fn is not None and not path_only else "")
            curlly(cmd, fn)
    finally:
        CD(cwd)

def ariari(url, fp, fn):
    url, j = strip_(url, fn)
    if not url: return

    if 'civitai.com' in url: ua = civitai_headers()['User-Agent']
    else: ua = 'Mozilla/5.0'

    cmd = [
        'aria2c', f'--header=User-Agent: {ua}', '--allow-overwrite=true',
        '--console-log-level=error', '--stderr=true', '-c', '-x16', '-s16', '-k1M', '-j5'
    ]

    if TOBRUT and 'huggingface.co' in url: cmd.append(f'--header=Authorization: Bearer {TOBRUT}')

    if fn: cmd += ['-o', fn]
    cmd.append(url)

    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        aria2_output, break_line, error_code, error_line = '', False, [], []

        while True:
            lines = p.stderr.readline()
            if lines == '' and p.poll() is not None: break

            if lines:
                aria2_output += lines

                for prog in lines.splitlines():
                    if 'errorCode' in prog or 'Exception' in prog:
                        error_code.append(prog)
                    if '|' in prog and 'error_line' in prog:
                        prog = re.sub(r'(\|\s*)(error_line)(\s*\|)', f'\\1{RED}\\2{RESET}\\3', prog)
                        first, _, last = prog.rpartition('|')
                        last = re.sub(r'/', f'{CYAN}/{RESET}', last)
                        prog = f'{first}|{last}'
                        error_line.append(prog)

                    if re.match(r'\[#\w{6}\s.*\]', prog):
                        prog = re.sub(r'\[', MAGENTA + '【' + RESET, prog)
                        prog = re.sub(r'\]', MAGENTA + '】' + RESET, prog)
                        prog = re.sub(r'(#)(\w+)', f'{CYAN}\\1{RESET}{GREEN}\\2{RESET}', prog)
                        prog = re.sub(r'(\d+(\.\d+)?)(\w+)(/)(\d+(\.\d+)?)(\w+)', f"\\1{PURPLE}\\3{RESET}{MAGENTA}\\4{RESET}\\5{PURPLE}\\7{RESET}", prog)
                        prog = re.sub(r'(\()(\d+%)(\))', f'{MAGENTA}\\1{RESET}\\2{MAGENTA}\\3{RESET}', prog)
                        prog = re.sub(r'(CN)(:)(\d+)', f"{CYAN}\\1{RESET}\\2{ORANGE}\\3{RESET}", prog)
                        prog = re.sub(r'(DL)(:)(\d+(\.\d+)?)(\w+)', f"{CYAN}\\1{RESET}\\2\\3{PURPLE}\\5{RESET}", prog)
                        prog = re.sub(r'(ETA)(:)(\d+\w+)', f"{CYAN}\\1{RESET}\\2{YELLOW}\\3{RESET}", prog)

                        lines = prog.splitlines()
                        for line in lines:
                            print(f"\r{' '*300}\r {line}", end='')
                            sys.stdout.flush()

                        break_line = True
                        break

        error = error_code + error_line
        for lines in error: print(f'  {lines}')

        break_line and print()

        stripe = aria2_output.find('======+====+===========')
        if stripe != -1:
            for lines in aria2_output[stripe:].splitlines():
                if '|' in lines and 'OK' in lines:
                    lines = re.sub(r'(\|\s*)(OK)(\s*\|)', f'\\1{GREEN}\\2{RESET}\\3', lines)
                    first, _, last = lines.rpartition('|')
                    last = re.sub(r'/', f'{ORANGE}/{RESET}', last)
                    lines = f'{first}|{last}'
                    print(f'  {lines}')

        if j:
            civitai_infotags(j, fp, fn)
            civitai_preview(j, fp, fn)

        p.wait()

    except KeyboardInterrupt:
        print(f'\n{"":>2}^ Canceled')

def curlly(cmd, fn):
    try:
        p = subprocess.Popen(
            shlex.split(cmd), cwd=str(Path.cwd()),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, bufsize=1
        )

        prog = re.compile(r'(\d+\.\d+)%')
        curl_output = ''

        with tqdm(
            total=100, desc=f'{fn.ljust(58):>{58 + 2}}', initial=0,
            bar_format='{desc} 【{bar:20}】【{percentage:3.0f}%】',
            ascii='▷▶', file=sys.stdout
        ) as pbar:
            for line in iter(p.stderr.readline, ''):
                if line.strip():
                    match = prog.search(line)
                    if match:
                        progress = float(match.group(1))
                        pbar.update(progress - pbar.n)
                        pbar.refresh()

                curl_output += line
            pbar.close()
        p.wait()

        if p.returncode != 0:
            if 'curl: (23)' in curl_output:
                print(
                    f"{'':>2}^ File already exists; download skipped. "
                    "Append a custom name after the URL or PATH to overwrite."
                )
            elif 'curl: (3)' in curl_output:
                print('')
            else:
                print(f"{'':>2}^ Error: {curl_output}")
        else:
            pass

    except KeyboardInterrupt:
        print(f"{'':>2}^ Canceled")

def gdrown(url, fp=None, fn=None):
    is_folder = 'drive.google.com/drive/folders' in url
    cmd = f'gdown --fuzzy {url}'

    if fp:
        fp = Path(fp).expanduser()
        fp.mkdir(parents=True, exist_ok=True)
        if fn:
            fn = fp / fn
            cmd += f' -O {fn}'
        cwd = str(fp)
    else:
        cwd = None

    if fn and not fp: cmd += f' -O {fn}'
    if is_folder: cmd += ' --folder'

    SyS(f'cd {cwd} && {cmd}' if cwd else cmd)

@register_line_magic
def clone(i):
    p = Path(i).expanduser()

    def proc(line):
        return line.strip()[len('git clone '):].strip() if line.strip().startswith('git clone') else line.strip()

    if p.suffix == '.txt' and p.is_file():
        cmds = [f'git clone {proc(line)}' for line in p.read_text().splitlines()]
    elif isinstance(i, str):
        cmds = [f'git clone {proc(i)}']
    else:
        cmds = [f'git clone {proc(l)}' for l in i]

    for cmd in cmds:
        cmd = cmd.strip()
        if not cmd:
            continue

        cmd_list = shlex.split(cmd)
        url = next((repo for repo in cmd_list if re.match(r'https?://', repo)), None)

        p = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        while True:
            output = p.stdout.readline()
            if not output and p.poll() is not None:
                break

            if output := output.strip():
                if 'fatal' in output:
                    print(f'  {output}')
                elif output.startswith('Cloning into'):
                    repo_name = "/".join(output.split("'")[1].split("/")[-3:])
                    print(f'  {repo_name} ▶ {url}')

        p.wait()

@register_line_magic
def pull(line):
    inputs = line.split()
    if len(inputs) < 3: return

    subs = subprocess.run
    repo, tarfold, despath = inputs[:3]
    branch = inputs[3] if len(inputs) == 4 else None

    print(
        f"\n{'':>2}{'pull':<4} : {tarfold}",
        f"\n{'':>2}{'from':<4} : {repo}",
        f"\n{'':>2}{'into':<4} : {despath}",
        end=''
    )

    if branch: print(f"\n{'':>2}{'branch':<4} : {branch}")
    print()

    fp = Path(despath).expanduser()
    opts = {'stdout': subprocess.PIPE, 'stderr': subprocess.PIPE, 'check': True}
    cmd1 = f'git clone -n --depth=1 --filter=tree:0'
    if branch: cmd1 += f' --branch {branch}'
    cmd1 += f' {repo}'
    subs(shlex.split(cmd1), cwd=str(fp), **opts)

    repofold = fp / Path(repo).name.rstrip('.git')

    cmd2 = f'git sparse-checkout set --no-cone {tarfold}'
    subs(shlex.split(cmd2), cwd=str(repofold), **opts)

    cmd3 = 'git checkout'
    subs(shlex.split(cmd3), cwd=str(repofold), **opts)

    zipin = repofold / 'config' / tarfold
    zipout = fp / f'{tarfold}.zip'
    with zipfile.ZipFile(str(zipout), 'w') as zipf:
        for root in zipin.rglob('*'):
            if root.is_file():
                arcname = str(root.relative_to(zipin))
                zipf.write(str(root), arcname=arcname)

    cmd4 = f'unzip -o {str(zipout)}'
    subs(shlex.split(cmd4), cwd=str(fp), **opts)
    zipout.unlink()

    cmd5 = f'rm -rf {str(repofold)}'
    subs(shlex.split(cmd5), cwd=str(fp), **opts)

@register_line_magic
def tempe(line=''):
    try:
        from KANDANG import TEMPPATH
        TMP = Path(TEMPPATH)
    except ImportError:
        TMP = Path('/tmp')

    DIRS = [
        'ckpt',
        'lora',
        'controlnet',
        'svd',
        'z123',
        'clip',
        'clip_vision',
        'diffusers',
        'diffusion_models',
        'text_encoders',
        'unet'
    ]

    for SUB in DIRS: Path(f'{TMP}/{SUB}').mkdir(parents=True, exist_ok=True)