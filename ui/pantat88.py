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
        link, fn = args[0], args[1] if len(args) > 1 else None
        auth = f"-H 'Authorization: Bearer d3bdbbd15377673b43f7ab4b224f2800'"
        outopt = f"-o {fn}" if fn else "-O"
        fc = f"curl -J -L {auth} {link} {outopt}"

        result = subprocess.run(fc, shell=True, capture_output=True, text=True, cwd=os.getcwd())
        dfn = fn or os.path.basename(urlparse(link).path)

        display(HTML(f"<span>Downloading: {dfn}</span>"))
        if result.returncode == 0:
            print("done")
        elif result.stderr:
            print(result.stderr)
            
    else:  
        link, path, fn = args[0], args[1] if len(args) > 1 else None, args[2] if len(args) > 2 else None
        fn = os.path.basename(urlparse(link).path) if not path or not fn else fn
        full_path = os.path.join(os.getcwd(), path) if path else None
        
        if full_path and os.path.splitext(full_path)[1]:
            fn = os.path.basename(full_path)
            
        full_path = os.path.join(os.getcwd(), path) if path else None
        os.makedirs(full_path, exist_ok=True) if full_path else None
        fc = f"curl -Lo {os.path.join(full_path, fn)} {link}" if full_path else f"curl -Lo {fn} {link}"
        
        display(HTML(f"<span>Downloading: {fn}</span>"))
        result = subprocess.run(fc, shell=True, capture_output=True, text=True, cwd=os.getcwd())
        
        if result and result.returncode == 0:
            print("done")
        elif result:
            print(result.stderr)
            
