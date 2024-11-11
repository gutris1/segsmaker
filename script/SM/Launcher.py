import subprocess, sys, os, time, shlex, json
from pathlib import Path

MARK = Path.home() / '.gutris1/marking.json'

config = json.load(MARK.open('r'))
tunnel = config.get('tunnel')
ui = config.get('ui')
cwd = Path.cwd()

def launch():
    os.environ['LD_PRELOAD'] = '/home/studio-lab-user/.conda/envs/default/lib/libtcmalloc_minimal.so.4'
    launcher = 'main.py' if ui == 'ComfyUI' else 'launch.py'
    cmd = f'/tmp/venv/bin/python3 {launcher} ' + ' '.join(sys.argv[1:])

    if ui in ['A1111', 'Forge', 'ReForge']:
        if tunnel == 'Pinggy':
            cwd = Path.cwd()
            timer = cwd / "asd" / "pinggytimer.txt"
            end_time = int(time.time()) + 3600
            os.system(f"echo -n {end_time} > {timer}")

    os.system(cmd)

def kohyass_launch():
    def denied_denied():
        for r, _, f in os.walk(cwd):
            for i in f:
                if i.endswith('.toml'):
                    toml = Path(r) / i
                    toml.chmod(0o755)

    denied_denied()
    
    gui_sh = cwd / 'gui.sh'
    gui_sh.chmod(0o755)

    os.environ['MPLBACKEND'] = 'gtk3agg'
    import matplotlib

    os.environ['PATH'] = '/tmp/venv-kohya/bin:' + os.environ['PATH']
    os.environ['LD_PRELOAD'] = '/home/studio-lab-user/.conda/envs/default/lib/libtcmalloc_minimal.so.4'
    os.environ['LD_LIBRARY_PATH'] = '/tmp/venv-kohya/lib:/home/studio-lab-user/.conda/envs/default/lib:' + os.environ.get('LD_LIBRARY_PATH', '')

    subprocess.run("bash ./gui.sh --headless", shell=True, check=True, stdout=sys.stdout, stderr=sys.stdout)

def sdtrainer_launch():
    os.environ['MPLBACKEND'] = 'gtk3agg'
    os.environ['LD_PRELOAD'] = '/home/studio-lab-user/.conda/envs/default/lib/libtcmalloc_minimal.so.4'
    import matplotlib

    cmd = f'/tmp/venv-sd-trainer/bin/python3 gui.py ' + ' '.join(sys.argv[1:])
    os.system(cmd)

def facefusion_launch():
    os.environ['MPLBACKEND'] = 'gtk3agg'
    import matplotlib

    os.environ.pop('LD_PRELOAD', None)
    os.environ.pop('LD_LIBRARY_PATH', None)

    os.environ['LD_PRELOAD'] = (
        '/home/studio-lab-user/.conda/envs/default/lib/libcublasLt.so.12:' +
        '/home/studio-lab-user/.conda/envs/default/lib/libcublas.so.12:' +
        '/home/studio-lab-user/.conda/envs/default/lib/libtcmalloc_minimal.so.4'
    )
    os.environ['LD_LIBRARY_PATH'] = '/home/studio-lab-user/.conda/envs/default/lib:' + os.environ.get('LD_LIBRARY_PATH', '')

    cmd = f"source activate default && /tmp/venv-fusion/bin/python3 facefusion.py run {' '.join(shlex.quote(arg) for arg in sys.argv[1:])}"
    webui = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=sys.stdout, text=True, shell=True, executable="/bin/bash")

    for line in webui.stdout:
        print(line, end='')

    webui.wait()

if __name__ == '__main__':
    try:
        if ui == 'FaceFusion':
            facefusion_launch()
        elif ui == 'SDTrainer':
            sdtrainer_launch()
        elif ui == 'KohyaSS':
            kohyass_launch()
        else:
            launch()
    except KeyboardInterrupt:
        pass
