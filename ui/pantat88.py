from IPython.core.magic import register_line_magic
from IPython.display import HTML, display
import subprocess
import os
from urllib.parse import urlparse

@register_line_magic
def say(line):
    args = line.split()
    msg = " ".join(args[:-1])
    color = args[-1]
    display(HTML(f"<span style='color:{color};'>{msg}</span>"))
    
@register_line_magic
def download(line):
    args = line.split()

    if "civitai.com" in args[0]:
        url, fn = args[0], args[1] if len(args) > 1 else None
        auth = f"-H 'Authorization: Bearer d3bdbbd15377673b43f7ab4b224f2800'"
        outopt = f"-o {fn}" if fn else "-O"
        fc = f"curl -J -L {auth} {url} {outopt}"
        dfn = fn or os.path.basename(urlparse(url).path)
        
        display(HTML(f"<span>Downloading: {dfn}</span>"))
        result = subprocess.run(fc, shell=True, capture_output=True, text=True, cwd=os.getcwd())

        if result.returncode == 0:
            print("done")
        elif result.stderr:
            print(result.stderr)
            
    else:  
        url, path, fn = args[0], args[1] if len(args) > 1 else None, args[2] if len(args) > 2 else None
        fn = os.path.basename(urlparse(url).path) if not path or not fn else fn
        fp = os.path.join(os.getcwd(), path) if path else None
        
        if fp and os.path.splitext(fp)[1]:
            fn = os.path.basename(fp)
            
        fp = os.path.join(os.getcwd(), path) if path else None
        os.makedirs(fp, exist_ok=True) if fp else None
        fc = f"curl -Lo {os.path.join(fp, fn)} {url}" if fp else f"curl -Lo {fn} {url}"
        
        display(HTML(f"<span>Downloading: {fn}</span>"))
        result = subprocess.run(fc, shell=True, capture_output=True, text=True, cwd=os.getcwd())
        
        if result and result.returncode == 0:
            print("done")
        elif result:
            print(result.stderr)
            
