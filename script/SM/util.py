from IPython.core.magic import register_line_magic, register_cell_magic
from IPython.display import display, HTML, clear_output, Image
from IPython import get_ipython
import ipywidgets as widgets
from pathlib import Path
from nenen88 import say
from tqdm import tqdm
import subprocess
import zipfile
import psutil
import time
import json
import sys
import os

SyS = get_ipython().system

home = Path.home()
src = home / '.gutris1'
css = src / 'segsmaker.css'
img = src / 'loading.png'
startup = home / '.ipython/profile_default/startup'

@register_line_magic
def storage(line):
    U = ['B', 'KB', 'MB', 'GB', 'TB']
    P = [str(home), '/tmp']

    SyS(f'rm -rf {home}/.cache/*')

    def size1(s, d=1):
        if s == 0: return '0'

        for u in U:
            if s < 1024.0:
                if u in ['B', 'K']: return f'{s:.0f} {u}'
                else: return f'{s:.{d}f} {u}'
            s /= 1024.0

    def size2(s):
        if s == 0: return '0'

        b = 1024
        sb = s * b

        for u in U:
            if sb < b:
                if u in ['B', 'K']: return f'{sb:.0f} {u}'
                else: return f'{sb:.1f} {u}'
            sb /= b

    def listing(r, p):
        if r == str(home): return '/' + str(Path(p).relative_to(home))
        else: return '/' + str(Path(p).relative_to('/tmp'))

    g = {}

    for r in P:
        du = subprocess.check_output(['du', '-k', '--max-depth=1', r], stderr=subprocess.DEVNULL).decode()

        e = []

        for l in du.split('\n'):
            if not l.strip(): continue

            try:
                sb, p = l.split('\t')
                s = int(sb)
            except ValueError: continue

            if p == r: continue

            name = listing(r, p)
            e.append((name, s))

        g[r] = e

    a = []
    for r in P: a.extend(g.get(r, []))

    m = (max((len(p) for p, _ in a), default=0) + 4)

    for r in P:
        if r == '/tmp': print()

        usage = psutil.disk_usage(Path(r))

        t = 'Persistent Storage' if r == str(home) else 'Temporary Storage'
        display(HTML(f'<b>{t}</b>'))

        free_disk = size1(usage.free, d=1)
        total_disk = size1(usage.total, d=0)

        print(f'{free_disk} free of {total_disk}')
        print()

        e = g.get(r, [])

        e.sort(key=lambda x: (0 if Path(x[0]).name.startswith('.') else 1, Path(x[0]).name.lower()))
        for p, s in e:
            l = size2(s)
            print(f'{p:<{m}} {l:>10}')

@register_line_magic
def delete_everything(line):    
    main_output = widgets.Output()
    ask = widgets.Label('Delete?')
    yes = widgets.Button(description='Yes')
    no = widgets.Button(description='No')

    button = widgets.HBox(
        [no, yes],
        layout=widgets.Layout(
            display='flex',
            flex_flow='row',
            align_items='center',
            top='35px',
            justify_content='space-around',
            width='100%'
        )
    )

    boxs = widgets.VBox(
        [ask, button],
        layout=widgets.Layout(
            width='450px',
            height='150px',
            display='flex',
            flex_flow='column',
            align_items='center',
            justify_content='space-around',
            padding='10px'
        )
    )

    ask.add_class('del')
    yes.add_class('save-button')
    no.add_class('save-button')
    boxs.add_class('boxs')

    def load_css(css):
        display(HTML(f'<style>{Path(css).read_text()}</style>'))

    def oh_no(b):
        boxs.close()
        main_output.clear_output()

    def oh_yes(b):
        with main_output:
            boxs.close()
            clear_output()

            display(Image(filename=str(img)))

            if 'LD_PRELOAD' in os.environ: del os.environ['LD_PRELOAD']

            folder_list = [
                'A1111', 'Forge', 'ReForge', 'ReForge-old', 'Forge-Classic', 'Forge-Neo', 'ComfyUI', 'SwarmUI',
                'tmp/*', 'tmp', '.cache/*', '.config/*', '.ssh', '.zrok', '.ngrok', '.sagemaker',
                '.conda/*', '.conda', '.ipython/profile_default/startup/*'
            ]

            cmd_list = [f"rm -rf {' '.join([str(home / folder) for folder in folder_list])}"]

            for deleting in cmd_list: SyS(deleting)

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
                say('Restart JupyterLab Now!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

    no.on_click(oh_no)
    yes.on_click(oh_yes)

    load_css(css)
    display(boxs, main_output)

def nb_clear(nb_path):
    try:
        nb_file = Path(nb_path)
        nb_contents = json.loads(nb_file.read_text())

        nb_contents['metadata'] = {
            'language_info': {'name': ''},
            'kernelspec': {'name': '', 'display_name': ''}
        }

        nb_file.write_text(json.dumps(nb_contents, indent=1, sort_keys=True))

    except Exception:
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
            arg_value = soup[1].strip().strip('"')

            if '$HOME' in arg_value or '$home' in arg_value:
                arg_value = arg_value.replace('$HOME', str(Path.home())).replace('$home', str(Path.home()))

            if arg_value.startswith('$'):
                var_name = arg_value[1:]
                if var_name in globals():
                    arg_value = str(globals()[var_name])
                else:
                    print(f'[ERROR]: {var_name} is not defined.')
                    return

            if arg_name == 'inputs':
                input_path = Path(arg_value)

            elif arg_name == 'outputs':
                output_path = Path(arg_value)

            elif arg_name == 'name':
                custom_name = arg_value

    if not input_path.exists():
        print(f'[ERROR]: {input_path} does not exist.')
        return

    if not output_path.exists():
        output_path.mkdir(parents=True, exist_ok=True)

    def zip_folder(
        input_path,
        output_path,
        max_size_mb=20,
        custom_name=None):

        all_files = []

        skip_extensions = {
            '.safetensors', '.ckpt',
            '.pt', '.pth',
            '.h5', '.pickle', '.pkl', '.bin',
            '.zip', '.tar.gz', '.tar.lz4', '.py'
        }

        for file_path in input_path.rglob('*'):
            if file_path.is_file():
                if file_path.suffix.lower() not in skip_extensions:
                    all_files.append(file_path)
                else:
                    print(f'{file_path.name} skipped')

        zip_number = 1
        current_zip_size = 0

        if custom_name:
            current_zip_name = output_path / f'{custom_name}_{zip_number}.zip'
        else:
            current_zip_name = output_path / f'part_{zip_number}.zip'

        with tqdm(
            total=len(all_files),
            desc='zipping : ',
            bar_format='{desc}[{bar:26}] [{n_fmt}/{total_fmt}]',
            ascii='▷▶',
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
                            current_zip_name = output_path / f'{custom_name}_{zip_number}.zip'
                        else:
                            current_zip_name = output_path / f'part_{zip_number}.zip'

                        current_zip = zipfile.ZipFile(
                            current_zip_name,
                            'w',
                            compression=zipfile.ZIP_DEFLATED
                        )

                        current_zip_size = 0

                    current_zip.write(
                        file_path,
                        file_path.relative_to(input_path)
                    )

                    current_zip_size += file_size
                    pbar.update(1)

    max_size_mb = 200
    zip_folder(input_path, output_path, max_size_mb, custom_name)

@register_line_magic
def change_api_key(line):
    nenen = startup / 'nenen88.py'
    key_file = src / 'api-key.json'

    output = widgets.Output()

    title = widgets.HTML("<h4>Change API Key</h4>")

    current_civitai = widgets.Text(placeholder='', disabled=True)
    new_civitai = widgets.Text(placeholder='New Civitai API KEY')
    civitai_box = widgets.VBox([current_civitai, new_civitai])

    current_hf = widgets.Text(placeholder='', disabled=True)
    new_hf = widgets.Text(placeholder='New Huggingface READ Token (optional)')
    hf_box = widgets.VBox([current_hf, new_hf])

    save_button = widgets.Button(description='Save')
    cancel_button = widgets.Button(description='Cancel')
    button_box = widgets.HBox([cancel_button, save_button])

    key_box = widgets.VBox([civitai_box, hf_box])
    change_key_box = widgets.VBox([title, key_box, button_box])

    for w, c in [
        (title, 'change-key-title'),
        (change_key_box, 'change-key-box'),
        (save_button, 'save-change-key'),
        (cancel_button, 'cancel-change-key'),
        (key_box, 'key-box'),
        (button_box, 'button-box'),
        (civitai_box, 'civitai-box'),
        (current_civitai, 'current-civitai'),
        (new_civitai, 'new-civitai'),
        (hf_box, 'hf-box'),
        (current_hf, 'current-hf'),
        (new_hf, 'new-hf'),
    ]: w.add_class(c)

    def load_css(css):
        display(HTML(f'<style>{Path(css).read_text()}</style>'))

    def key_inject(civitai_key, hf_token):
        SyS(f'curl -sLo {nenen} https://github.com/gutris1/segsmaker/raw/main/script/nenen88.py')

        p = Path(nenen)
        v = p.read_text()
        v = v.replace("TOKET = ''", f"TOKET = '{civitai_key}'")
        v = v.replace("TOBRUT = ''", f"TOBRUT = '{hf_token}'")
        p.write_text(v)

    def key_widget(current_civitai_key='', current_hf_key=''):
        current_civitai.value = current_civitai_key
        current_hf.value = current_hf_key

        def save_key(b):
            with output:
                output.clear_output(wait=True)
        
                civitai_key = new_civitai.value.strip() or current_civitai.value.strip()
                hf_token = new_hf.value.strip() or current_hf.value.strip()

                new_civitai.value = civitai_key
                new_hf.value = hf_token

                if not civitai_key:
                    print('Please enter your CivitAI API Key')
                    return
        
                if len(civitai_key) < 32:
                    print('API key must be at least 32 characters long')
                    return
        
                secrets = {
                    'civitai-api-key': civitai_key,
                    'huggingface-read-token': hf_token
                }
        
                Path(key_file).write_text(json.dumps(secrets, indent=4))
        
            with output:
                change_key_box.close()
                output.clear_output(wait=True)
                say('Saving...')
                key_inject(civitai_key, hf_token)
        
                output.clear_output(wait=True)
                get_ipython().kernel.do_shutdown(True)
                time.sleep(2)
                say('Kernel restarting...')
        
                output.clear_output(wait=True)
                time.sleep(3)
                say('Done')

        def cancel_key(b):
            new_civitai.value = ''
            new_hf.value = ''

            with output:
                change_key_box.close()
                output.clear_output(wait=True)
                say('^ Canceled')

        save_button.on_click(save_key)
        cancel_button.on_click(cancel_key)

    JS = """
    (() => {
      setTimeout(() => {
        document.querySelectorAll('.new-civitai input, .new-hf input').forEach(el => el.spellcheck = false);

        const box = document.querySelector('.change-key-box');
        box && box.classList.add('loaded');
      }, 1000);
    })();
    """

    def key_check():
        if key_file.exists():
            load_css(css)

            v = json.loads(key_file.read_text())
            civitai_key = v.get('civitai-api-key', '')
            hf_token = v.get('huggingface-read-token', '')

            key_widget(civitai_key, hf_token)

            display(HTML(f'<script>{JS}</script>'))
            display(change_key_box, output)

        else:
            say('API Key does not exist')

    key_check()

@register_line_magic
def zrok_register(line):
    zrok = {
        'bin': home / '.zrok2/zrok2',
        'version': home / '.zrok2/v2.0.4',
        'url': 'https://github.com/openziti/zrok/releases/download/v2.0.4/zrok_2.0.4_linux_amd64.tar.gz'
    }

    def load_css(css):
        display(HTML(f'<style>{Path(css).read_text()}</style>'))

    def zrok_install():
        binPath = zrok['bin']
        p = binPath.parent

        p.mkdir(parents=True, exist_ok=True)
        if binPath.exists(): binPath.unlink()

        n = Path(zrok['url']).name

        for cmd in [
            f'curl -sLo {p}/{n} {zrok["url"]}',
            f'tar -xzf {p}/{n} -C {p}',
            f'rm -f {p}/{n}'
        ]:
            SyS(cmd)

        for f in p.glob('v*'):
            f.unlink(missing_ok=True)

        zrok['version'].touch()
        if binPath.exists(): binPath.chmod(0o755)

    def register(b):
        import pexpect

        zrok_box.close()
        email = email_box.value

        R = '\033[0m'
        O = '\033[38;5;208m'
        E = f'{O}{email}{R}'

        with output:
            if not email:
                print('No email address entered.')
                return

            print('Submitting...')
            clear_output(wait=True)

            zrok_txt.touch()

            child = pexpect.spawn('bash')
            child.sendline(f'{zrok["bin"]} invite | tee {zrok_txt}')
            child.expect('enter and confirm your email address...')

            for _ in range(2):
                time.sleep(1)
                child.sendline(email)
                time.sleep(1)
                child.send(chr(9))

            child.sendline('\r\n')
            time.sleep(2)
            child.close()

            print(f'Invitation sent to {E}\n Be sure to check your SPAM folder if you do not receive the invitation email.')
            zrok_txt.unlink(missing_ok=True)

    def cancel(b):
        zrok_box.close()

    JS = """
    (() => {
      const baseUrl = JSON.parse(document.querySelector("#jupyter-config-data").textContent).baseUrl;
      document.documentElement.style.setProperty(
        "--segsmaker-bg",
        `url(${location.origin}${baseUrl}files/.gutris1/bg.jpg)`
      );

      setTimeout(() => {
        const box = document.querySelector('.zrok-box'),
        email = document.querySelector('.zrok-email input');

        box && box.classList.add('loaded');
        email && (email.spellcheck = false);
      }, 1000);
    })();
    """

    if not zrok['version'].exists(): zrok_install()

    zrok_cmd = zrok['bin'].with_name('zrok invite')
    zrok_txt = zrok['bin'].parent / 'zrok_log.txt'

    output = widgets.Output()

    email_box = widgets.Text(placeholder='Enter Your Valid Email Address')

    register_button = widgets.Button(description='Register')
    cancel_button = widgets.Button(description='Cancel')

    buttons_box = widgets.HBox([cancel_button, register_button])
    zrok_box = widgets.VBox([email_box, buttons_box])

    for w, c in [
        (zrok_box, 'zrok-box'),
        (email_box, 'zrok-email'),
        (buttons_box, 'zrok-buttons-box'),
        (register_button, 'zrok-button'),
        (cancel_button, 'zrok-button')
    ]: w.add_class(c)

    load_css(css)
    display(HTML(f'<script>{JS}</script>'))
    display(zrok_box, output)

    register_button.on_click(register)
    cancel_button.on_click(cancel)

    SyS('pip install -q pexpect')
