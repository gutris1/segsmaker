import subprocess, sys, os, time, shlex, json
from pathlib import Path

MARK = Path.home() / '.gutris1/marking.json'

config = json.load(MARK.open('r'))
tunnel = config.get('tunnel')
ui = config.get('ui')
cwd = Path.cwd()

os.environ['PYTHONWARNINGS'] = 'ignore'

def Launch():
    os.environ['PATH'] = '/tmp/venv/bin:' + os.environ['PATH']
    os.environ['LD_PRELOAD'] = '/home/studio-lab-user/.conda/envs/default/lib/libtcmalloc_minimal.so.4'

    if ui == 'SwarmUI':
        os.environ['LD_LIBRARY_PATH'] = '/tmp/venv/lib:/home/studio-lab-user/.conda/envs/default/lib:' + os.environ.get('LD_LIBRARY_PATH', '')
        os.environ['SWARMPATH'] = str(cwd)
        os.environ['SWARM_NO_VENV'] = 'true'

        os.system('pip install -q rembg')
        os.system('git pull -q')

        cmd = 'bash ./launch-linux.sh ' + ' '.join(sys.argv[1:])
    
    else:
        launcher = 'main.py' if ui == 'ComfyUI' else 'launch.py'

        if ui in ['A1111', 'Forge', 'ReForge']:
            if tunnel == 'Pinggy':
                timer = cwd / "asd" / "pinggytimer.txt"
                end_time = int(time.time()) + 3600
                os.system(f"echo -n {end_time} > {timer}")

        cmd = f'python3 {launcher} ' + ' '.join(sys.argv[1:])

    os.system(cmd)


def sdtrainer_launch():
    os.environ['MPLBACKEND'] = 'gtk3agg'
    os.environ['LD_PRELOAD'] = '/home/studio-lab-user/.conda/envs/default/lib/libtcmalloc_minimal.so.4'
    import matplotlib

    cmd = '/tmp/venv-sd-trainer/bin/python3 gui.py ' + ' '.join(sys.argv[1:])
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
        else:
            Launch()
    except KeyboardInterrupt:
        pass
