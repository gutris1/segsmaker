from IPython.core.magic import register_line_magic
from IPython.display import display, HTML
from urllib.parse import urlparse
import subprocess
import os
import sys
import zipfile
from tqdm import tqdm

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
        fc = f"curl -O -J -L {auth} {args[0]}"
    elif len(args) == 3:
        path, fn = args[1], args[2]
        os.makedirs(path, exist_ok=True)
        fc = f"mkdir -p {path} && cd {path} && curl -J -L {auth} {args[0]} -o {fn}"
    elif '/' in args[1] or '~/ ' in args[1]:
        path = args[1]
        os.makedirs(path, exist_ok=True)
        fn = os.path.basename(urlparse(args[0]).path)
        fc = f"mkdir -p {path} && cd {path} && curl -O -J -L {auth} {args[0]}"
    else:
        fn = args[1]
        fc = f"curl -J -L {auth} {args[0]} -o {fn}"
        
    print(f"Downloading: {fn}")
    
    try:
        result = subprocess.run(fc, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=os.getcwd(), check=True)
        print("done")
    except subprocess.CalledProcessError as e:
        if "curl: (23)" in e.stderr:
            print("Error: File exists")
        else:
            print(e.stderr)
    except KeyboardInterrupt:
        print("^ Canceled")

@register_line_magic
def zipper(line):
    
    def zip_folder(input_path, output_path, max_size_mb=20):
        
        os.makedirs(output_path, exist_ok=True)
        all_files = []
        for root, dirs, files in os.walk(input_path):
            for file in files:
                file_path = os.path.join(root, file)
                all_files.append(file_path)
                
        zip_number = 1
        current_zip_size = 0
        current_zip_name = os.path.join(output_path, f"part_{zip_number}.zip")
        
        with tqdm(total=len(all_files), desc='zipping : ', bar_format='{desc}{n_fmt}/{total_fmt} {bar} | {percentage:3.0f}% [ {elapsed}<{remaining}, {rate_fmt}{postfix} ]', ncols=100, file=sys.stdout) as pbar:
            with zipfile.ZipFile(current_zip_name, 'w', compression=zipfile.ZIP_DEFLATED) as current_zip:
                for file_path in all_files:
                    file_size = os.path.getsize(file_path)
                    
                    if current_zip_size + file_size > max_size_mb * 1024 * 1024:
                        current_zip.close()
                        zip_number += 1
                        current_zip_name = os.path.join(output_path, f"part_{zip_number}.zip")
                        current_zip = zipfile.ZipFile(current_zip_name, 'w', compression=zipfile.ZIP_DEFLATED)
                        current_zip_size = 0
                        
                    current_zip.write(file_path, os.path.relpath(file_path, input_path))
                    current_zip_size += file_size
                    pbar.update(1)

    max_size_mb = 200
    zip_folder(input_path, output_path, max_size_mb)
