from IPython.core.magic import register_line_magic, register_cell_magic
from IPython.display import display, HTML
from urllib.parse import urlparse
from tqdm import tqdm
import subprocess
import os
import sys
import re
import zipfile

@register_line_magic
def mktmp(line):
    subprocess.run(f"mkdir -p /tmp/models /tmp/Lora /tmp/ControlNet", shell=True)
    
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
        fc = f"curl -#OJL {auth} {args[0]} 2>&1"
    elif len(args) == 3:
        path, fn = args[1], args[2]
        os.makedirs(path, exist_ok=True)
        fc = f"mkdir -p {path} && cd {path} && curl -#JL {auth} {args[0]} -o {fn} 2>&1"
    elif '/' in args[1] or '~/ ' in args[1]:
        path = args[1]
        os.makedirs(path, exist_ok=True)
        fn = os.path.basename(urlparse(args[0]).path)
        fc = f"mkdir -p {path} && cd {path} && curl -#OJL {auth} {args[0]} 2>&1"
    else:
        fn = args[1]
        fc = f"curl -#JL {auth} {args[0]} -o {fn} 2>&1"
        
    try:
        process = subprocess.Popen(fc, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1, cwd=os.getcwd())
        progress_pattern = re.compile(r'(\d+\.\d+)%')
        accumulated_output = ""
        
        with tqdm(total=100, desc=f"Downloading {fn}", initial=0, bar_format="{desc} {percentage:3.0f}% ", file=sys.stdout) as pbar:
            for line in iter(process.stdout.readline, ''):
                if not line.startswith('  % Total') and not line.startswith('  % '):
                    match = progress_pattern.search(line)
                    if match:
                        progress = float(match.group(1))
                        pbar.update(progress - pbar.n)
                        pbar.refresh()
                        
                accumulated_output += line
            pbar.close()
        process.wait()
        
        if process.returncode != 0:
            if "curl: (23)" in accumulated_output:
                print("Error: File exists")
            else:
                print(f"Error: {accumulated_output}")
        else:
            print("")
                
    except KeyboardInterrupt:
        print("^ Canceled")
        
@register_cell_magic
def zipping(line, cell):
    lines = cell.strip().split('\n')

    input_path = None
    output_path = None

    for line in lines:
        parts = line.split('=')
        if len(parts) == 2:
            arg_name = parts[0].strip()
            arg_value = parts[1].strip().strip("'")

            if arg_name == 'input_folder':
                input_path = arg_value
            elif arg_name == 'output_folder':
                output_path = arg_value

    if not os.path.exists(input_path):
        print(f"Error: '{input_path}' does not exist.")
        return

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

        with tqdm(total=len(all_files), desc='zipping : ',
                bar_format='{desc}{bar} | {n_fmt}/{total_fmt} [ {elapsed}<{remaining}, {rate_fmt}{postfix} ]',
                ncols=100, file=sys.stdout) as pbar:
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
