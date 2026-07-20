TOKET = ''
TOBRUT = ''

from IPython.core.magic import register_line_magic
from IPython.display import display, HTML
from urllib.parse import urlparse, parse_qs
from IPython import get_ipython
from datetime import datetime
from pathlib import Path
from tqdm import tqdm
import subprocess
import threading
import requests
import zipfile
import shlex
import json
import time
import sys
import re
import os
import io

MAGENTA = '\033[35m'
RED = '\033[31m'
CYAN = '\033[36m'
GREEN = '\033[38;5;49m'
YELLOW = '\033[33m'
BLUE = '\033[38;5;69m'
PURPLE = '\033[38;5;177m'
ORANGE = '\033[38;5;208m'
RESET = '\033[0m'

CD = os.chdir
SyS = get_ipython().system
iRON = os.environ

KAGGLE = 'KAGGLE_DATA_PROXY_TOKEN' in iRON

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

class CIVITAI:
    DOMAINS = ('civitai.com', 'civitai.red',)

    BaseList = {
        'SD 1': 'SD1',
        'SD 1.5': 'SD1',
        'SD 2': 'SD2',
        'SD 3': 'SD3',
        'SDXL': 'SDXL',
        'Pony': 'SDXL',
        'Illustrious': 'SDXL',
        'Anima': 'Anima',
        'ZImageBase': 'ZImageBase',
        'ZImageTurbo': 'ZImageTurbo',
    }

    @classmethod
    def domain(c, url):
        try:
            h = urlparse(url).netloc.lower()
            return next((d for d in c.DOMAINS if d in h), None)

        except Exception:
            return None

    @staticmethod
    def headers():
        return {'User-Agent': 'CivitaiLink:Automatic1111'}

    @classmethod
    def get_json(c, api_url):
        try:
            r = requests.get(api_url, headers=c.headers(), timeout=15)
            if r.status_code != 200: return None

            return r.json()

        except Exception:
            return None

    @classmethod
    def from_url(c, url):
        url = url.split('?token=')[0]

        domain = c.domain(url)
        if not domain:
            return None

        query = parse_qs(urlparse(url).query)
        file_id = query.get('fileId', [None])[0]

        dl = f'{domain}/api/download/models/' in url

        if dl:
            version_id = url.split('models/')[1].split('/')[0].split('?')[0]
            api_url = f'https://{domain}/api/v1/model-versions/{version_id}'

        elif f'{domain}/models/' in url:
            version_id = query.get('modelVersionId', [None])[0]
            model_id = url.split('models/')[1].split('/')[0].split('?')[0]

            api_url = (
                f'https://{domain}/api/v1/model-versions/{version_id}'
                if version_id else
                f'https://{domain}/api/v1/models/{model_id}'
            )

        else:
            return None

        j = c.get_json(api_url)
        if not j: return None

        obj = c(j, version_id, file_id, domain)
        obj.direct_download = dl

        return obj

    def __init__(self, data, version_id=None, file_id=None, domain=None, sha256=None):
        self.data = data
        self.domain_name = domain
        self.version = self.whichVersion(version_id)

        self.direct_download = False
        self.selected_file = None

        self.resolve(file_id, sha256)

    def whichVersion(self, version_id=None):
        if 'modelVersions' not in self.data: return self.data
        if version_id: return next((mv for mv in self.data['modelVersions'] if str(mv.get('id')) == str(version_id)), self.data['modelVersions'][0])

        return self.data['modelVersions'][0]

    def resolve(self, file_id=None, sha256=None):
        sha256 = sha256 or self.get_sha256(file_id)

        if not sha256:
            self.selected_file = next((f for f in self.version.get('files', []) if f.get('downloadUrl')), None)
            return

        api = f'https://{self.domain_name}/api/v1/model-versions/by-hash/{sha256}'
        j = self.get_json(api)

        if not j: return

        self.data = j
        self.version = self.whichVersion(self.version_id)

        self.selected_file = next((f for f in self.version.get('files', []) if f.get('hashes', {}).get('SHA256', '').lower() == sha256.lower()), None)

    def get_sha256(self, file_id=None):
        if file_id: return next((f.get('hashes', {}).get('SHA256') for f in self.version.get('files', []) if str(f.get('id')) == str(file_id)), None)

        api = f'https://{self.domain_name}/api/v1/model-versions/mini/{self.version_id}'
        j = self.get_json(api)
        if j: return j.get('hashes', {}).get('SHA256')

        return None

    @property
    def exists(self):
        return self.file is not None

    @property
    def model_id(self):
        if 'modelVersions' in self.data: return self.data.get('id')

        return self.data.get('modelId')

    @property
    def version_id(self):
        return self.version.get('id')

    @property
    def file(self):
        return self.selected_file

    @property
    def filename(self):
        return (self.file.get('name') if self.file else None) or self.version.get('name')

    @property
    def sha256(self):
        return self.file.get('hashes', {}).get('SHA256') if self.file else None

    @property
    def download_url(self):
        return self.file.get('downloadUrl') if self.file else None

    @property
    def preview_url(self):
        return next((img.get('url', '') for img in self.version.get('images', []) if not img.get('url', '').lower().endswith(('.mp4', '.gif'))), None)

    @staticmethod
    def resizer(b, size=512):
        from PIL import Image

        i = Image.open(io.BytesIO(b))
        w, h = i.size
        s = ((size, int(h * size / w)) if w > h else (int(w * size / h), size))
        o = io.BytesIO()
        i.resize(s, Image.LANCZOS).save(o, format='PNG')
        o.seek(0)

        return o

    @property
    def activation_text(self):
        return ', '.join(self.version.get('trainedWords', []))

    @property
    def sd_version(self):
        base = self.version.get('baseModel', '')
        return next((s for k, s in self.BaseList.items() if k in base), '')

    @property
    def early_access(self):
        return self.version.get('availability') == 'EarlyAccess' or bool(self.version.get('earlyAccessEndsAt'))

    def early_access_info(self):
        if not self.early_access: return False

        page = f'https://{self.domain_name}/models/{self.model_id}?modelVersionId={self.version_id}'
        ends = self.version.get('earlyAccessEndsAt')
        if ends: ends = datetime.fromisoformat(ends.replace('Z', '+00:00')).strftime('%d %B %Y')

        print(f'{page}\n-> The model is in early access{f", ending at {ends}" if ends else ""}.')

        return True

    def model_json(self, folder, filename=None):
        name = filename or self.filename
        if not name: return

        info = Path(folder) / f'{Path(name).stem}.json'
        if info.exists(): return

        data = {
            'activation text': self.activation_text,
            'sd version': self.sd_version,
            'modelId': self.model_id,
            'modelVersionId': self.version_id,
            'sha256': self.sha256,
        }

        info.write_text(json.dumps(data, indent=4))

    def model_preview(self, folder, filename=None):
        name = filename or self.filename
        if not name: return

        preview = self.preview_url
        if not preview: return

        path = Path(folder) / f'{Path(name).stem}.preview.png'
        if path.exists(): return

        r = requests.get(preview, headers=self.headers()).content
        resized = self.resizer(r)

        if KAGGLE:
            from melon00 import image_encryption
            image_encryption(resized, path)
        else:
            path.write_bytes(resized.read())

    def extras(self, path, filename):
        def t():
            self.model_json(path, filename)
            self.model_preview(path, filename)

        threading.Thread(target=t, daemon=True).start()

@register_line_magic
def download(i):
    args = i.split()
    if not args:
        print('  missing URL, downloading nothing')
        return

    url = args[0]
    path = Path(url).expanduser()
    if url.endswith('.txt') and path.is_file():
        for l in path.read_text(encoding='utf-8').splitlines(): netorare(l)
    else: netorare(i)

def _url(url):
    return (
        CIVITAI.domain(url),
        'huggingface.co' in url,
        'github.com' in url or 'raw.githubusercontent.com' in url,
        'drive.google.com' in url,
    )

def netorare(line):
    fp, fn = None, None

    parts = line.strip().split()
    if not parts: return

    cwd = Path.cwd()
    path = lambda s: '/' in s or '~/' in s
    url = parts[0].replace('\\', '')

    civitai, huggingface, github, driveGoogle = _url(url)

    try:
        if len(parts) >= 3:
            a, b = parts[1], parts[2]

            aa = path(a)
            bb = path(b)

            if bb and not aa: p, f = b, a
            elif aa and not bb: p, f = a, b
            elif Path(b).suffix == '' and Path(a).suffix != '': p, f = b, a
            else: p, f = a, b

            fp = Path(p).expanduser()
            fn = f

            fp.mkdir(parents=True, exist_ok=True)
            CD(fp)

        elif len(parts) == 2:
            a = parts[1]

            if path(a):
                fp = Path(a).expanduser()
                fp.mkdir(parents=True, exist_ok=True)
                CD(fp)
                fn = (None if (civitai or driveGoogle) else Path(urlparse(url).path).name)
            else:
                fn = a
                fp = cwd

        else:
            fn = (None if (civitai or driveGoogle) else Path(urlparse(url).path).name)
            fp = cwd

        if civitai or huggingface or github: ariari(url, fp, fn)

        elif driveGoogle: gdrown(url, fp, fn)

        else:
            cp = (len(parts) == 2 and fp is not None)
            cmd = (
              f"curl -#{'OJL' if len(parts) == 1 or cp else 'JL'} '{url}'" +
              (f" -o '{fn}'" if fn is not None and not cp else '')
            )
            curlly(cmd, fn)

    finally:
        CD(cwd)

def _resolve(url, fn):
    civitai, huggingface, github, _ = _url(url)

    if github:
        return (url.replace('/blob/', '/raw/'), None, fn)

    elif huggingface:
        url = url.split('?')[0]
        headers = {'User-Agent': 'Mozilla/5.0', **({'Authorization': f'Bearer {TOBRUT}'} if TOBRUT else {})}
        ext = {'.safetensors', '.pt', '.pth'}
        c = None

        if fn and Path(fn).suffix.lower() in ext:
            try:
                raw_url = re.sub(r'/(resolve|blob)/', '/raw/', url)
                res = requests.get(raw_url, headers=headers, timeout=15)
                t = re.search(r'oid sha256:([a-fA-F0-9]{64})', res.text)

                if t:
                    sha256 = t.group(1).lower()

                    for u in CIVITAI.DOMAINS:
                        try:
                            api_url = f'https://{u}/api/v1/model-versions/by-hash/{sha256}'

                            j = CIVITAI.get_json(api_url)
                            if not j: continue

                            r = next((f for f in j.get('files', []) if f.get('hashes', {}).get('SHA256', '').lower() == sha256), None)
                            if r: c = CIVITAI(j, domain=u, sha256=sha256); break

                        except Exception:
                            continue

            except Exception:
                pass

        url = url.replace('/blob/', '/resolve/')
        return (url, c, fn)

    elif civitai:
        c = CIVITAI.from_url(url)

        if not c:
            return (None, None, None)

        if c.early_access_info():
            return (None, None, None)

        return (c.download_url, c, fn or c.filename)

    return (url, None, fn)

def ariari(url, fp, fn):
    url, c, fn = _resolve(url, fn)
    if not url: return

    civitai, huggingface, *_ = _url(url)
    headers = {'User-Agent': (CIVITAI.headers()['User-Agent'] if civitai else 'Mozilla/5.0')}

    if TOKET and civitai and f'{civitai}/api/download/models/' in url:
        headers['Authorization'] = f'Bearer {TOKET}'

        try:
            r = requests.get(url, headers=headers, allow_redirects=True, stream=True, timeout=30)
            if r.url and r.url != url: url = r.url
            r.close()

        except Exception as e:
            print(f'  Preflight failed: {e}')
            print('  Falling back to aria2 with Authorization header.')

    cmd = [
        'aria2c',
        f"--header=User-Agent: {headers['User-Agent']}",
        *([f'--header=Authorization: Bearer {TOBRUT}'] if TOBRUT and huggingface else ()),
        '--allow-overwrite=true',
        '--console-log-level=error',
        '--stderr=true',
        '-c', '-x16', '-s16', '-k1M',
        *(['-o', fn] if fn else ()),
        url,
    ]

    try:
        if c: c.extras(fp, fn)

        for i in range(20 if huggingface else 1):
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            aria2_output, bl, error_code, error_line = '', False, [], []

            while True:
                lines = p.stderr.readline()
                if lines == '' and p.poll() is not None:
                    break

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

                        m = re.match(
                            r'\[#\w+\s+'
                            r'(?:(\d+(?:\.\d+)?\w+/\d+(?:\.\d+)?\w+))?'
                            r'\((\d+%)\)'
                            r'.*?DL:(\d+(?:\.\d+)?\w+)'
                            r'(?:.*?ETA:(\d+\w+))?',
                            prog
                        )

                        if m:
                            sizes, percent, speed, eta = m.groups()

                            percent = re.sub(r'(\d+)(%)', f'\\1{PURPLE}\\2{RESET}', percent)
                            parts = [f'{MAGENTA}({RESET}{percent}{MAGENTA}){RESET}']

                            if sizes:
                                current, total = sizes.split('/')
                                current = re.sub(r'(\d+(?:\.\d+)?)(\w+)', f'\\1{PURPLE}\\2{RESET}', current)
                                total = re.sub(r'(\d+(?:\.\d+)?)(\w+)', f'\\1{PURPLE}\\2{RESET}', total)
                                parts.append(f'{current}{CYAN}/{RESET}{total}')

                            speed = re.sub(r'(\d+(?:\.\d+)?)(\w+)', f'\\1{PURPLE}\\2{RESET}', speed)
                            parts.append(f'{CYAN}DL{RESET}:{speed}')

                            if eta:
                                parts.append(f'{CYAN}ETA{RESET}:{YELLOW}{eta}{RESET}')

                            body = ' '.join(parts)

                            print(f"\r{' '*300}\r  {RED}●{RESET} {fn} {body}", end='')
                            sys.stdout.flush()

                            bl = True
                            break

            p.wait()

            if not (huggingface and p.returncode and 'xet-bridge' in aria2_output and 'status=403' in aria2_output):
                print('\r' + ' ' * 80 + '\r', end=''); sys.stdout.flush(); break

            print(f'\r  retrying {fn or url} [{i+1}/20]', end=''); sys.stdout.flush(); time.sleep(1)

        if p.returncode:
            for line in error_code + error_line:
                print(f'  {line}')

        for lines in aria2_output.splitlines():
            if '|' in lines and 'OK' in lines:
                pipe = [p.strip() for p in lines.split('|')]

                if len(pipe) >= 4:
                    saved = re.sub(r'/', f'{ORANGE}/{RESET}', pipe[3])
                    print(f"\r{' '*300}\r  {GREEN}●{RESET} {saved}")
                    sys.stdout.flush()
                    bl = False

        if bl:
            print()

    except KeyboardInterrupt:
        print('\n  ^ Canceled')

def curlly(cmd, fn):
    try:
        p = subprocess.Popen(shlex.split(cmd), cwd=str(Path.cwd()), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)

        prog = re.compile(r'(\d+\.\d+)%')
        curl_output = ''

        with tqdm(total=100, desc=f'{fn.ljust(58):>{58 + 2}}', initial=0, bar_format='{desc} 【{bar:20}】【{percentage:3.0f}%】', ascii='▷▶', file=sys.stdout) as pbar:
            for o in iter(p.stderr.readline, ''):
                if o.strip():
                    res = prog.search(o)
                    if res: progress = float(res.group(1)); pbar.update(progress - pbar.n); pbar.refresh()
                curl_output += o
            pbar.close()
        p.wait()

        if p.returncode != 0:
            if 'curl: (23)' in curl_output: print('  ^ File already exists; download skipped. Append a custom name after the URL or PATH to overwrite.')
            elif 'curl: (3)' in curl_output: print('')
            else: print(f'  ^ Error: {curl_output}')
        else:
            pass

    except KeyboardInterrupt:
        print(f'  ^ Canceled')

def gdrown(url, fp=None, fn=None):
    folder = 'drive.google.com/drive/folders' in url
    cmd = ['gdown', '--fuzzy']

    if folder: cmd.append('--folder')
    cmd.append(url)

    name = fn or None
    saved = None

    if fp:
        fp = Path(fp).expanduser()
        fp.mkdir(parents=True, exist_ok=True)

        if fn:
            fn = fp / fn
            cmd += ['-O', str(fn)]

        cwd = str(fp)

    else:
        cwd = None

        if fn: cmd += ['-O', fn]

    try:
        p = subprocess.Popen(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        bl = False

        while True:
            prog = p.stdout.readline()

            if prog == '' and p.poll() is not None: break
            if not prog: continue

            prog = prog.strip()
            if not prog: continue

            if prog.startswith('To: '):
                try:
                    saved = prog[4:].strip()
                    name = Path(saved).name
                except: pass
                continue

            if '%' in prog and '/' in prog:
                prog = re.sub(r'(\d+)(%)', f'\\1{PURPLE}\\2{RESET}', prog)
                prog = re.sub(r'(\d+(?:\.\d+)?[KMG]B/s)', f'{CYAN}\\1{RESET}', prog)
                print(f"\r{' '*300}\r  {RED}●{RESET} {name} {prog}", end='')

                sys.stdout.flush()
                bl = True

            else:
                skip = (
                    'Downloading...' in prog or
                    'From (original):' in prog or
                    'From (redirected):' in prog
                )

                if skip: continue
                if bl: print()

                print(f'  {GREEN}●{RESET} {prog}')
                bl = False

        p.wait()

        if saved:
            saved = re.sub(r'/', f'{ORANGE}/{RESET}', saved)
            print(f"\r{' '*300}\r  {GREEN}●{RESET} {saved}")

    except KeyboardInterrupt:
        try: p.terminate()
        except: pass
        print('\n  ^ Canceled')

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
    print('\n')

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
    l = [
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

    for f in l: (Path('/tmp') / f).mkdir(parents=True, exist_ok=True)
