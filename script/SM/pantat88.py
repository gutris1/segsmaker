from IPython.core.magic import register_line_magic
from IPython.display import display, HTML
from urllib.parse import urlparse
from IPython import get_ipython
from pathlib import Path
from tqdm import tqdm
import subprocess, zipfile, sys, os, re, shlex, requests

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
tobrut = ""
@register_line_magic
def download(line):
    args = line.split()

    if not args:
        print("  missing URL, downloading nothing")
        return

    url = args[0]

    if url.endswith('.txt') and Path(url).expanduser().is_file():
        with open(Path(url).expanduser(), 'r') as file:
            for line in file:
                netorare(line)
    else:
        netorare(line)


def strip_(url):
    if "civitai.com" in url:
        if '?token=' in url:
            url = url.split('?token=')[0]
        if '?type=' in url:
            url = url.replace('?type=', f'?token={toket}&type=')
        else:
            url = f"{url}?token={toket}"

        if "civitai.com/models/" in url:
            if '?modelVersionId=' in url:
                version_id = url.split('?modelVersionId=')[1]
                response = requests.get(f"https://civitai.com/api/v1/model-versions/{version_id}")
            else:
                model_id = url.split('/models/')[1].split('/')[0]
                response = requests.get(f"https://civitai.com/api/v1/models/{model_id}")

            data = response.json()
            download_url = data["downloadUrl"] if "downloadUrl" in data else data["modelVersions"][0]["downloadUrl"]
            return f"{download_url}?token={toket}"

    elif "huggingface.co" in url:
        if '/blob/' in url:
            url = url.replace('/blob/', '/resolve/')
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
    chg = any(domain in url for domain in ["civitai.com", "huggingface.co", "github.com"])
    dg = "drive.google.com" in url
    path, fn = "", ""
    url = strip_(url)
    _dir = Path.cwd()

    aria2c = (
        "aria2c --header='User-Agent: Mozilla/5.0' "
        "--allow-overwrite=true --console-log-level=error --stderr=true "
        "-c -x16 -s16 -k1M -j5"
    )

    if tobrut and "huggingface.co" in url:
        aria2c += f" --header='Authorization: Bearer {tobrut}'"

    try:
        if len(hitozuma) >= 3:
            path, fn = Path(hitozuma[1]).expanduser(), hitozuma[2]
            path.mkdir(parents=True, exist_ok=True)
            os.chdir(path)
            if chg:
                fc = f"{aria2c} '{url}' -o '{fn}'"
                ketsuno_ana(fc, fn)
            elif dg:
                gdrown(url, path, fn)
            else:
                fc = f"curl -#JL '{url}' -o '{fn}'"
                ketsuno_ana(fc, fn)
            
        elif len(hitozuma) >= 2:
            if '/' in hitozuma[1] or '~/' in hitozuma[1]:
                path = Path(hitozuma[1]).expanduser()
                path.mkdir(parents=True, exist_ok=True)
                os.chdir(path)
                if chg:
                    fn = get_fn(url)
                    fc = f"{aria2c} '{url}'"
                    if 'civitai.com' not in url:
                        fc += f" -o '{fn}'"
                    ketsuno_ana(fc, fn)
                elif dg:
                    gdrown(url, path)
                else:
                    fn = Path(urlparse(url).path).name
                    fc = f"curl -#OJL '{url}'"
                    ketsuno_ana(fc, fn)
            else:
                fn = hitozuma[1]
                if chg:
                    fc = f"{aria2c} '{url}' -o '{fn}'"
                    ketsuno_ana(fc, fn)
                elif dg:
                    gdrown(url, None, fn)
                else:
                    fc = f"curl -#JL '{url}' -o '{fn}'"
                    ketsuno_ana(fc, fn)

        else:
            if chg:
                fn = get_fn(url)
                fc = f"{aria2c} '{url}'"
                if 'civitai.com' not in url:
                    fc += f" -o '{fn}'"
                ketsuno_ana(fc, fn)
            elif dg:
                gdrown(url)
            else:
                fn = Path(urlparse(url).path).name
                fc = f"curl -#OJL '{url}'"
                ketsuno_ana(fc, fn)
    finally:
        os.chdir(_dir)


def gdrown(url, path=None, fn=None):
    is_folder = "drive.google.com/drive/folders" in url
    cmd = "gdown --fuzzy " + url

    if path:
        path = str(Path(path).expanduser())
        os.makedirs(path, exist_ok=True)
        cwd = path
        if fn:
            fn = str(Path(path) / fn)
            cmd += " -O " + fn
    else:
        cwd = None

    if fn and not path:
        cmd += " -O " + fn

    if is_folder:
        cmd += " --folder"

    if cwd:
        get_ipython().system(f"cd {cwd} && {cmd}")
    else:
        get_ipython().system(f"{cmd}")


def ariari(fc, fn):
    try:
        qqqqq = subprocess.Popen(
            shlex.split(fc),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        result = ""
        br = False

        code = []
        err = []

        MAGENTA = "\033[35m"
        RED = "\033[31m"
        CYAN = "\033[36m"
        GREEN = "\033[38;5;35m"
        YELLOW = "\033[33m"
        BLUE = "\033[38;5;69m"
        PURPLE = "\033[38;5;135m"
        RESET = "\033[0m"

        while True:
            lines = qqqqq.stderr.readline()
            if lines == '' and qqqqq.poll() is not None:
                break

            if lines:
                result += lines

                for outputs in lines.splitlines():
                    if 'errorCode' in outputs or 'Exception' in outputs:
                        code.append(outputs)
                    if '|' in outputs and 'ERR' in outputs:
                        outputs = re.sub(r'(\|\s*)(ERR)(\s*\|)', f'\\1{RED}\\2{RESET}\\3', outputs)
                        err.append(outputs)

                    if re.match(r'\[#\w{6}\s.*\]', outputs):
                        outputs = re.sub(r'\[', MAGENTA + '【' + RESET, outputs)
                        outputs = re.sub(r'\]', MAGENTA + '】' + RESET, outputs)
                        outputs = re.sub(r'(#)(\w+)', f'\\1{GREEN}\\2{RESET}', outputs)
                        outputs = re.sub(r'(\(\d+%\))', f'{CYAN}\\1{RESET}', outputs)
                        outputs = re.sub(r'(CN:)(\d+)', f"\\1{BLUE}\\2{RESET}", outputs)
                        outputs = re.sub(r'(DL:)(\d+\w+)', f"\\1{PURPLE}\\2{RESET}", outputs)
                        outputs = re.sub(r'(ETA:)(\d+\w+)', f"\\1{YELLOW}\\2{RESET}", outputs)
                        lines = outputs.splitlines()
                        for line in lines:
                            print(f"\r{' '*180}\r {line}", end="")
                            sys.stdout.flush()
                        br = True
                        break

        error = code + err
        for lines in error:
            print(f"  {lines}")

        if br:
            print()

        stripe = result.find("======+====+===========")
        if stripe != -1:
            for lines in result[stripe:].splitlines():
                if '|' in lines and 'OK' in lines:
                    lines = re.sub(r'(\|\s*)(OK)(\s*\|)', f'\\1{GREEN}\\2{RESET}\\3', lines)
                    print(f"  {lines}")

        qqqqq.wait()

    except KeyboardInterrupt:
        print(f"\n{'':>2}^ Canceled")


def curlly(fc, fn):
    try:
        zura = subprocess.Popen(
            shlex.split(fc),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            cwd=str(Path.cwd())
        )

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

            for line in iter(zura.stderr.readline, ''):
                if line.strip():
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
                print(
                    f"{'':>2}^ File already exists; download skipped. "
                    "Append a custom name after the URL or PATH to overwrite."
                )
            elif "curl: (3)" in oppai:
                print("")
            else:
                print(f"{'':>2}^ Error: {oppai}")
        else:
            pass

    except KeyboardInterrupt:
        print(f"{'':>2}^ Canceled")


def ketsuno_ana(fc, fn):
    if "aria2c" in fc:
        ariari(fc, fn)
    else:
        curlly(fc, fn)

        
@register_line_magic
def clone(line):
    path = Path(line).expanduser()

    if line.endswith('.txt') and path.is_file():
        with open(path, 'r') as file:
            lines = [line.strip() for line in file]
    else:
        lines = line if isinstance(line, list) else [line]

    cloning(lines)

def cloning(lines):
    for line in lines:
        line = line.strip()
        if not line:
            continue

        cmd = shlex.split(line)
        url = None
        for repo in cmd:
            if re.match(r'https?://', repo):
                url = repo
                break

        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        while True:
            output = proc.stdout.readline()
            if not output and proc.poll() is not None:
                break

            if output:
                output = output.strip()
                if "fatal" in output:
                    print(f"{'':>2}{output}")

                elif output.startswith("Cloning into"):
                    lines = output.split("'")[1]
                    names = "/".join(lines.split("/")[-3:])
                    print(f"{'':>2}{names} => {url}")

        proc.wait()


@register_line_magic
def pull(line):
    inputs = line.split()
    if len(inputs) != 3:
        return

    repo, tarfold, despath = inputs

    print(
    f"\n{'':>2}{'pull':<4} : {tarfold}",
    f"\n{'':>2}{'from':<4} : {repo}",
    f"\n{'':>2}{'into':<4} : {despath}\n")

    path = Path(despath).expanduser()
    opts = {'stdout': subprocess.PIPE, 'stderr': subprocess.PIPE, 'check': True}
    subs = subprocess.run
    cmd1 = f'git clone -n --depth=1 --filter=tree:0 {repo}'
    subs(shlex.split(cmd1), cwd=str(path), **opts)
    repofold = path / Path(repo).name.rstrip('.git')
    cmd2 = f'git sparse-checkout set --no-cone {tarfold}'
    subs(shlex.split(cmd2), cwd=str(repofold), **opts)
    cmd3 = 'git checkout'
    subs(shlex.split(cmd3), cwd=str(repofold), **opts)

    zipin = repofold / 'config' / tarfold
    zipout = path / f'{tarfold}.zip'
    
    with zipfile.ZipFile(str(zipout), 'w') as zipf:
        for root in zipin.rglob('*'):
            if root.is_file():
                arcname = str(root.relative_to(zipin))
                zipf.write(str(root), arcname=arcname)

    cmd4 = f'unzip -o {str(zipout)}'
    subs(shlex.split(cmd4), cwd=str(path), **opts)
    zipout.unlink()
    cmd5 = f'rm -rf {str(repofold)}'
    subs(shlex.split(cmd5), cwd=str(path), **opts)


@register_line_magic
def tempe(line):
    BASEPATH = None
    ENV = None

    env_list = {
        'Colab': ('/content', 'COLAB_JUPYTER_TRANSPORT'),
        'Kaggle': ('/kaggle', 'KAGGLE_DATA_PROXY_TOKEN'),
        'SageMaker': ('/home/studio-lab-user', 'SAGEMAKER_INTERNAL_IMAGE_URI')
    }

    for env_name, (path, env_var) in env_list.items():
        if os.getenv(env_var):
            BASEPATH = path
            ENV = env_name
            break

    if ENV in ('Colab', 'Kaggle'):
        tmplist = [
            f"{BASEPATH}/temp/ckpt",
            f"{BASEPATH}/temp/lora",
            f"{BASEPATH}/temp/controlnet",
            f"{BASEPATH}/temp/svd",
            f"{BASEPATH}/temp/z123",
            f"{BASEPATH}/temp/clip"
        ]

    else:
        tmplist = [
            "/tmp/ckpt",
            "/tmp/lora",
            "/tmp/controlnet",
            "/tmp/svd",
            "/tmp/z123",
            "/tmp/clip"
        ]

    for paths in tmplist:
        Path(paths).mkdir(parents=True, exist_ok=True)
