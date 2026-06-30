from IPython.display import display, HTML, clear_output, Image
from IPython import get_ipython
from ipywidgets import widgets
from pathlib import Path
import subprocess
import shlex
import json

SyS = get_ipython().system

R = '\033[0m'
T = f'▶{R}'
BLUE = f'\033[38;5;33m{T}'
CYAN = f'\033[36m{T}'
PURPLE = f'\033[38;5;135m{T}'
PINK = f'\033[38;5;201m{T}'
RED = f'\033[31m{T}'
GREEN = f'\033[38;5;35m{T}'

HOME = Path.home()
SRC = HOME / '.gutris1'
CSS = SRC / 'segsmaker.css'
startup = HOME / '.ipython/profile_default/startup'
nenen = startup / 'nenen88.py'
api_key = SRC / 'api-key.json'
IMG = SRC / 'loading.png'

SRC.mkdir(parents=True, exist_ok=True)

def load_css(): 
    display(HTML(f'<style>{open(CSS).read()}</style>'))

def restart_kernel():
    display(HTML("""
    <script>
    (() => {
      const i = setInterval(() => {
        const b = document.querySelector('dialog[aria-label*="It will restart automatically"] button');
        if (b) clearInterval(i), b.click();
      }, 200);
    })();
    </script>
    """))

    get_ipython().kernel.do_shutdown(True)

def install_conda():
    cv = int(subprocess.run(['conda', '--version'], capture_output=True, text=True, check=True).stdout.split()[1].split('.')[0])

    if cv < 26:
        try:
            with loading:
                output.clear_output(wait=True)
                display(Image(filename=str(IMG)))
    
            with output:
                cmd_list = [
                    (f'rm -rf {HOME}/.condarc', None),
                    ('conda config --add channels conda-forge', None),
                    ('conda install -qy mamba', f'{BLUE} Installing Anaconda'),
                    ('mamba install -y conda', None),
                    ('mamba install -y python=3.10.13', f'{CYAN} Installing Python 3.10'),
                    ('mamba install -y glib gperftools compilers openssh pv gputil curl', f'{PURPLE} Installing Conda Packages'),
                    ('pip install psutil aria2 gdown Pillow pyyaml pickleshare', f'{PINK} Installing Python Packages'),
                    ('conda clean -qy --all', None)
                ]
    
                for cmd, msg in cmd_list:
                    if msg is not None: print(msg)
                    subprocess.run(shlex.split(cmd), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
                SyS(f'rm -rf {HOME}/.cache/* {HOME}/.condarc')
    
                with output:
                    output.clear_output(wait=True)
    
                with loading:
                    loading.clear_output(wait=True)
                    print(f'{GREEN} Done')
    
                restart_kernel()
    
        except KeyboardInterrupt:
            clear_output()
            print('^ Canceled')

    else:
        with output:
            print(f'{GREEN} Done')
            restart_kernel()

def key_inject(civitai_key, hf_token):
    SyS(f'curl -sLo {nenen} {G}/script/nenen88.py')

    p = Path(nenen)
    v = p.read_text()
    v = v.replace("TOKET = ''", f"TOKET = '{civitai_key}'")
    v = v.replace("TOBRUT = ''", f"TOBRUT = '{hf_token}'")
    p.write_text(v)

def key_widget(civitai_key='', hf_token=''):
    civitai_box.value = civitai_key
    hf_box.value = hf_token

    def save_key(b):
        civitai_key = civitai_box.value.strip()
        hf_token = hf_box.value.strip()

        with output:
            if not civitai_key:
                print('Please enter your Civitai API Key')
                return

            if len(civitai_key) < 32:
                print('API key must be at least 32 characters long')
                return

            api_key.write_text(json.dumps({
                'civitai-api-key': civitai_key,
                'huggingface-read-token': hf_token,
            }, indent=4))

        key_inject(civitai_key, hf_token)

        conda_widget.close()
        output.clear_output()

        install_conda()

    save_button.on_click(save_key)

def display_widget(civitai_key='', hf_token=''):
    load_css()
    display(HTML(f'<script>{JS}</script>'))
    display(conda_widget, output, loading)
    key_widget(civitai_key, hf_token)

def key_check():
    if not api_key.exists():
        display_widget()
        return

    v = json.loads(api_key.read_text())
    civitai_key = v.get('civitai-api-key', '')
    hf_token = v.get('huggingface-read-token', '')

    if not civitai_key or not hf_token:
        display_widget(civitai_key, hf_token)
        return

    key_inject(civitai_key, hf_token)
    display(output, loading)
    install_conda()

def misc():
    for s in [
        f'{SRC}/bg.jpg https://i.imgur.com/5Mkdrpw.jpeg',
        f'{IMG} {G}/script/loading.png',
        f'{startup} {G}/script/cupang.py',

        f'{startup} {G}/script/SM/00-startup.py',
        f'{startup} {G}/script/SM/util.py',
        f'{CSS} {G}/script/SM/segsmaker.css'
    ]: SyS(f'curl -sLo {s}')

G = 'https://raw.githubusercontent.com/gutris1/segsmaker/main'

JS = """
(() => {
  const baseUrl = JSON.parse(document.querySelector("#jupyter-config-data").textContent).baseUrl;
  document.documentElement.style.setProperty(
    "--segsmaker-bg",
    `url(${location.origin}${baseUrl}files/.gutris1/bg.jpg)`
  );

  setTimeout(() => {
    const tokens = document.querySelectorAll('.conda-api-input input');
    tokens.forEach(el => el.spellcheck = false);
  }, 100);
})();
"""

output = widgets.Output()
loading = widgets.Output()

civitai_box = widgets.Text(placeholder='Civitai API Key')
hf_box = widgets.Text(placeholder='Huggingface READ Token (optional)')
token_box = widgets.VBox([civitai_box, hf_box])

save_button = widgets.Button(description='Save')

conda_widget = widgets.Box([token_box, save_button])

for w, c in [
    (conda_widget, 'conda-widget'),
    (token_box, 'conda-token-box'),
    (civitai_box, 'conda-api-input conda-civitai-box'),
    (hf_box, 'conda-api-input conda-hf-box'),
    (save_button, 'conda-save-button'),
]:
    for i in c.split(): w.add_class(i)

misc()
key_check()
