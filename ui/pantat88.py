from IPython.core.magic import register_line_magic
from IPython.display import display, HTML
from urllib.parse import urlparse
import subprocess
import os

@register_line_magic
def say(line):
    args = line.split()
    msg = " ".join(args[:-1])
    color = args[-1]
    display(HTML(f"<span style='color:{color};'>{msg}</span>"))
    
@register_line_magic
def download(line):
    args = line.split()
    url, auth = args[0], "-H 'Authorization: Bearer d3bdbbd15377673b43f7ab4b224f2800'" if "civitai.com" in args[0] else ""
    
    if len(args) == 1:
        fn = os.path.basename(urlparse(args[0]).path)
        fc = f"curl -O -J -L {auth} {args[0]} > /dev/null"
    elif len(args) == 3:
        path, fn = args[1], args[2]
        os.makedirs(path, exist_ok=True)
        fc = f"mkdir -p {path} && cd {path} && curl -J -L {auth} {args[0]} -o {fn} > /dev/null"
    elif '/' in args[1] or '~/ ' in args[1]:
        path = args[1]
        os.makedirs(path, exist_ok=True)
        fn = os.path.basename(urlparse(args[0]).path)
        fc = f"mkdir -p {path} && cd {path} && curl -O -J -L {auth} {args[0]} > /dev/null"
    else:
        fn = args[1]
        fc = f"curl -J -L {auth} {args[0]} -o {fn} > /dev/null"
        
    print(f"Downloading: {fn}")
    
    try:
        result = subprocess.run(fc, shell=True, stderr=subprocess.PIPE, text=True, cwd=os.getcwd(), check=True)
        print("done")
    except subprocess.CalledProcessError as e:
        if "curl: (23)" in e.stderr:
            print("Error: File exists")
        else:
            print(e.stderr)
    except KeyboardInterrupt:
        print("^ Canceled")
        
