from IPython.core.magic import register_line_magic, register_cell_magic
from IPython.display import display, HTML, clear_output, Image
from IPython import get_ipython
import ipywidgets as widgets
from pathlib import Path
from tqdm import tqdm
from nenen88 import say
import subprocess, time, zipfile, sys, os, json, psutil


home = Path.home()
src_src = home / '.gutris1'
css = src_src / "pantat88.css"
img = src_src / "loading.png"
startup = home / ".ipython/profile_default/startup"

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
def delete_everything(line):    
    main_output = widgets.Output()
    
    ask = widgets.Label("Delete Everything?")
    ask.add_class("del")

    yes = widgets.Button(description="Yes")
    yes.add_class("save-button")

    no = widgets.Button(description="No")
    no.add_class("save-button")

    button = widgets.HBox(
        [yes, no], layout=widgets.Layout(
            display='flex',
            flex_flow='row',
            align_items='center',
            justify_content='space-around',
            width='100%'))

    boxs = widgets.VBox(
        [ask, button], layout=widgets.Layout(
            width='450px',
            height='150px',
            display='flex',
            flex_flow='column',
            align_items='center',
            justify_content='space-around',
            padding='20px'))
    boxs.add_class("boxs")

    def load_css(css):
        with open(css, "r") as file:
            panel = file.read()

        display(HTML(f"<style>{panel}</style>"))

    def oh_no(b):
        boxs.close()
        main_output.clear_output()

    def oh_yes(b):
        with main_output:
            boxs.close()
            clear_output()

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
                main_output.clear_output(wait=True)
                say("Now, Please Restart JupyterLab")

    no.on_click(oh_no)
    yes.on_click(oh_yes)

    load_css(css)
    display(boxs, main_output)

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
    custom_name = None

    for line in lines:
        soup = line.split('=')

        if len(soup) == 2:
            arg_name = soup[0].strip()
            arg_value = soup[1].strip().strip("'")

            if arg_value.startswith('$'):
                var_name = arg_value[1:]
                if var_name in globals():
                    arg_value = str(globals()[var_name])
                else:
                    print(f"Error: '{var_name}' is not defined.")
                    return

            if arg_name == 'inputs':
                input_path = Path(arg_value)

            elif arg_name == 'outputs':
                output_path = Path(arg_value)

            elif arg_name == 'name':
                custom_name = arg_value

    if not input_path.exists():
        print(f"Error: '{input_path}' does not exist.")
        return

    if not output_path.exists():
        output_path.mkdir(parents=True, exist_ok=True)

    def zip_folder(
        input_path,
        output_path,
        max_size_mb=20,
        custom_name=None):

        all_files = []

        for file_path in input_path.rglob('*'):
            if file_path.is_file():
                all_files.append(file_path)

        zip_number = 1
        current_zip_size = 0

        if custom_name:
            current_zip_name = output_path / f"{custom_name}_{zip_number}.zip"
        else:
            current_zip_name = output_path / f"part_{zip_number}.zip"

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
                    file_size = file_path.stat().st_size

                    if current_zip_size + file_size > max_size_mb * 1024 * 1024:
                        current_zip.close()

                        zip_number += 1

                        if custom_name:
                            current_zip_name = output_path / f"{custom_name}_{zip_number}.zip"
                        else:
                            current_zip_name = output_path / f"part_{zip_number}.zip"

                        current_zip = zipfile.ZipFile(
                            current_zip_name,
                            'w',
                            compression=zipfile.ZIP_DEFLATED)

                        current_zip_size = 0

                    current_zip.write(
                        file_path,
                        file_path.relative_to(input_path))

                    current_zip_size += file_size
                    pbar.update(1)

    max_size_mb = 200
    zip_folder(input_path, output_path, max_size_mb, custom_name)

@register_line_magic
def change_key(line):
    nenen = startup / "nenen88.py"
    pantat = startup / "pantat88.py"
    key_file = src_src / "api-key.json"

    main_output = widgets.Output()
    save_button = widgets.Button(description="Save")
    save_button.add_class("save")

    cancel_button = widgets.Button(description="Cancel")
    cancel_button.add_class("cancel")

    new_key = widgets.Text(placeholder='Enter Your New Civitai API KEY')
    new_key.add_class("key-input")

    current_key = widgets.Text(placeholder='', disabled=True)
    current_key.add_class("current-key")

    buttons = widgets.HBox([save_button, cancel_button],
                           layout=widgets.Layout(
                               width='400px',
                               display='flex',
                               flex_flow='row',
                               align_items='center',
                               justify_content='space-around',
                               padding='0px'))

    input_widget = widgets.VBox([current_key, new_key, buttons],
                                layout=widgets.Layout(
                                    width='400px',
                                    height='200px',
                                    display='flex',
                                    flex_flow='column',
                                    align_items='center',
                                    justify_content='space-around',
                                    padding='20px'))
    input_widget.add_class("input-widget")

    def load_css(css):
        with open(css, "r") as file:
            panel = file.read()

        display(HTML(f"<style>{panel}</style>"))

    def key_inject(api_key):
        x = [
            f"curl -sLo {pantat} https://github.com/gutris1/segsmaker/raw/main/script/pantat88.py",
            f"curl -sLo {nenen} https://github.com/gutris1/segsmaker/raw/main/script/nenen88.py"
        ]

        for y in x:
            get_ipython().system(y)

        target = [pantat, nenen]

        for line in target:
            with open(line, "r") as file:
                variable = file.read()

            value = variable.replace("YOUR_CIVITAI_API_KEY", f"{api_key}")
            with open(line, "w") as file:
                file.write(value)

    def key_widget(current_key_value=''):
        current_key.value = current_key_value

        def save_key(b):
            api_key = new_key.value.strip()

            with main_output:
                if not api_key:
                    print("Please enter your CivitAI API KEY / CivitAI APIキーのおっぱいを入力してください。")
                    return

                if len(api_key) < 32:
                    print("API key must be at least 32 characters long / APIキーは少なくとも32オッパイの長さに達する必要があります。")
                    return

                key_value = {"civitai-api-key": api_key}
                with open(key_file, "w") as file:
                    json.dump(key_value, file, indent=4)

            with main_output:
                input_widget.close()
                main_output.clear_output(wait=True)
                say("Saving...")
                key_inject(api_key)

                main_output.clear_output(wait=True)
                get_ipython().kernel.do_shutdown(True)
                time.sleep(2)
                say("Kernel restarting...")

                main_output.clear_output(wait=True)
                time.sleep(3)
                say("Done")

        def cancel_key(b):
            new_key.value = ''

            with main_output:
                input_widget.close()
                main_output.clear_output(wait=True)
                say("^ Canceled")

        save_button.on_click(save_key)
        cancel_button.on_click(cancel_key)

    def key_check():
        if key_file.exists():
            with open(key_file, "r") as file:
                value = json.load(file)

            api_key = value.get("civitai-api-key", "")
            key_widget(api_key)
            display(input_widget, main_output)
        else:
            say("API Key File does not exist")

    load_css(css)
    key_check()

zrok_bin = home / '.zrok/bin'
zrok_cmd = zrok_bin / 'zrok invite'
zrok_txt = zrok_bin / 'zrok_log.txt'

@register_line_magic
def zrok_register(line):
    zrok_output = widgets.Output()

    register_button = widgets.Button(description="Register", layout=widgets.Layout(left= '-45%'))
    register_button.add_class("zrok-btn")

    exit_button = widgets.Button(description="Exit", layout=widgets.Layout(left= '45%'))
    exit_button.add_class("zrok-btn")

    email_input = widgets.Text(placeholder='Enter Your Valid Email Address', layout=widgets.Layout(width= '75%'))
    email_input.add_class("email-input")

    zrok_button = widgets.HBox([register_button, exit_button], layout=widgets.Layout(
        display='flex',
        flex_flow='row',
        justify_content='space-between'))

    zrok_widget = widgets.VBox([email_input, zrok_button], layout=widgets.Layout(
        height='160px',
        width= '550px',
        display='flex',
        flex_flow='column',
        align_items='center',
        justify_content='space-around',
        padding='20px'))
    zrok_widget.add_class("zrok-widget")

    def zrok_install():    
        if zrok_bin.exists():
            return

        zrok_bin.mkdir(parents=True, exist_ok=True)
        zrok_url = "https://github.com/openziti/zrok/releases/download/v0.4.32/zrok_0.4.32_linux_amd64.tar.gz"
        zrok_tar = zrok_bin / Path(zrok_url).name

        get_ipython().system(f"curl -sLo {zrok_tar} {zrok_url}")
        get_ipython().system(f"tar -xzf {zrok_tar} -C {zrok_bin} --wildcards *zrok")
        get_ipython().system(f"rm -rf {home}/.cache/* {zrok_tar}")

    def load_css(css):
        with open(css, "r") as file:
            zrok_panel = file.read()

        display(HTML(f"<style>{zrok_panel}</style>"))

    def register(b):
        import pexpect

        zrok_widget.close()
        email = email_input.value

        R = '\033[0m'
        O = '\033[38;5;208m'
        E = f'{O}{email}{R}'

        with zrok_output:
            if not email:
                print('No email address entered.')
                return

            print('Submitting...')
            clear_output(wait=True)

            zrok_txt.touch()

            child = pexpect.spawn('bash')
            child.sendline(f'{zrok_cmd} | tee {zrok_txt}')
            child.expect('enter and confirm your email address...')

            for _ in range(2):
                time.sleep(1)
                child.sendline(email)
                time.sleep(1)
                child.send(chr(9))

            child.sendline('\r\n')
            time.sleep(2)
            child.close()

            print(f'Invitation sent to {E}\n'
                  f'Be sure to check your SPAM folder if you do not receive the invitation email.')

            zrok_txt.unlink()

    def exit(b):
        zrok_widget.close()

    load_css(css)
    display(zrok_widget, zrok_output)

    register_button.on_click(register)
    exit_button.on_click(exit)
    
    zrok_install()
    get_ipython().system('pip install -q pexpect')
