from IPython.core.magic import register_line_magic, register_cell_magic
from IPython.display import display, HTML, clear_output, Image
from IPython import get_ipython
from pathlib import Path
from tqdm import tqdm
import subprocess, zipfile, sys, os, json, psutil


home = Path.home()
img = home / ".conda/loading.png"

@register_line_magic
def storage(line):
    get_ipython().system(f"rm -rf {home}/.cache/*")
    paths = [str(home), "/tmp"]

    def size1(size, dcml=1):
        if size == 0:
            return "0 KB"

        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                if unit in ['B', 'KB']:
                    return f"{size:.0f} {unit}"
                else:
                    return f"{size:.{dcml}f} {unit}"
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

    for path_str in paths:
        path = Path(path_str)

        usage = psutil.disk_usage(path)
        size_str = size1(usage.total, dcml=0)
        used_str = size1(usage.used, dcml=1)
        free_str = size1(usage.free, dcml=1)

        if path_str == str(home):
            storage_type = "Persistent Storage"
        elif path_str == "/tmp":
            storage_type = "Temporary Storage"

        display(HTML(f"{storage_type}"))

        print(f" Size = {size_str:>8}")
        print(f" Used = {used_str:>8} | {usage.percent:.1f}%")
        print(f" Free = {free_str:>8} | {100 - usage.percent:.1f}%")
        print()

    du_process = subprocess.Popen(['du', '-h', '-k', '--max-depth=1', str(home)], stdout=subprocess.PIPE)
    du_output = du_process.communicate()[0].decode()
    lines = du_output.split('\n')
    sub_paths = [Path(line.split('\t')[1]) for line in lines if line]
    sizes_kb = [int(line.split('\t')[0]) for line in lines if line]

    subdirectories = []

    for sub_path, size_kb in zip(sub_paths, sizes_kb):
        formatted_size = size2(size_kb)
        base_path = sub_path.name

        if base_path != 'studio-lab-user':
            subdirectories.append((base_path, formatted_size))

    if subdirectories:
        for base_path, formatted_size in subdirectories:
            padding = " " * max(0, 9 - len(formatted_size))
            print(f"/{base_path:<30} {padding}{formatted_size}")


@register_line_magic
def delete(line):
    display(Image(filename=str(img)))

    if 'LD_PRELOAD' in os.environ:
        del os.environ['LD_PRELOAD']
    
    folder_list = [
        'tmp/*',
        'tmp',
        'asd',
        'forge',
        'ComfyUI',
        '.cache/*',
        '.config/*',
        '.ssh',
        '.zrok',
        '.sagemaker',
        '.nv',
        '.conda',
        '.ipython/profile_default/startup'
    ]
    
    cmd_list = [
        f"rm -rf {' '.join([str(home / folder) for folder in folder_list])}",
    ]

    for deleting in cmd_list:
        get_ipython().system(deleting)

    is_nb = False
    try:
        nb_find = f"find {home} -type d -name '.*' -prune -o -type f -name '*.ipynb' -print"
        nb_files = subprocess.check_output(nb_find, shell=True, text=True, stderr=subprocess.DEVNULL).strip().split('\n')
        
        for nb_path in nb_files:
            if nb_path:
                nb_clear(nb_path)
                is_nb = True
                
    except subprocess.CalledProcessError:
        pass

    if is_nb:
        clear_output(wait=True)
        print("Now, Please Restart JupyterLab.")


def nb_clear(nb_path):
    try:
        with open(nb_path, 'r') as f:
            nb_contents = json.load(f)

        nb_contents['metadata'] = {
            "language_info": {
                "name": ""
            },
            "kernelspec": {
                "name": "",
                "display_name": ""
            }
        }
        
        with open(nb_path, 'w') as f:
            json.dump(nb_contents, f, indent=1, sort_keys=True)

    except:
        pass


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
