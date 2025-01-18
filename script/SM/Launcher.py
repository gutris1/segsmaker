from pathlib import Path
import matplotlib
import subprocess
import shlex
import json
import time
import sys
import os

MARK = Path.home() / '.gutris1/marking.json'
config = json.load(MARK.open('r'))
tunnel = config.get('tunnel')
ui = config.get('ui')
cwd = Path.cwd()

iRON = os.environ
SyS = os.system

def setENV():
    iRON['PYTHONWARNINGS'] = 'ignore'

    def setVAR(var, new, value):
        current_value = iRON.get(var, '')
        if new not in current_value:
            iRON[var] = new + (':' + current_value if current_value else '')

    if ui == 'SDTrainer':
        iRON['MPLBACKEND'] = 'gtk3agg'
        setVAR('LD_PRELOAD', '/home/studio-lab-user/.conda/envs/default/lib/libtcmalloc_minimal.so.4', 'LD_PRELOAD')

    elif ui == 'FaceFusion':
        iRON['MPLBACKEND'] = 'gtk3agg'
        iRON.pop('LD_PRELOAD', None)
        iRON.pop('LD_LIBRARY_PATH', None)
        iRON['LD_PRELOAD'] = '/home/studio-lab-user/.conda/envs/default/lib/libcublasLt.so.12:' + \
                                  '/home/studio-lab-user/.conda/envs/default/lib/libcublas.so.12:' + \
                                  '/home/studio-lab-user/.conda/envs/default/lib/libtcmalloc_minimal.so.4'
        iRON['LD_LIBRARY_PATH'] = '/home/studio-lab-user/.conda/envs/default/lib'

    elif ui == 'SwarmUI':
        setVAR('PATH', '/tmp/venv/bin', '/tmp/venv/bin')
        setVAR('LD_LIBRARY_PATH', '/tmp/venv/lib:/home/studio-lab-user/.conda/envs/default/lib', 'LD_LIBRARY_PATH')
        iRON['SWARMPATH'] = str(cwd)
        iRON['SWARM_NO_VENV'] = 'true'

    else:
        setVAR('PATH', '/tmp/venv/bin', '/tmp/venv/bin')
        setVAR('LD_PRELOAD', '/home/studio-lab-user/.conda/envs/default/lib/libtcmalloc_minimal.so.4', 'LD_PRELOAD')

def Launch():
    launcher = 'main.py' if ui == 'ComfyUI' else 'launch.py'

    if ui == 'SwarmUI':
        SyS('pip install -q rembg')
        SyS('git pull -q')
        cmd = 'bash ./launch-linux.sh ' + ' '.join(sys.argv[1:])
    else:
        if ui in ['A1111', 'Forge', 'ReForge']:
            timer = cwd / "asd/pinggytimer.txt"
            end_time = int(time.time()) + 3600
            SyS(f"echo -n {end_time} > {timer}")
        cmd = f'python3 {launcher} ' + ' '.join(sys.argv[1:])
    SyS(cmd)

def sdtrainer_launch():
    cmd = '/tmp/venv-sd-trainer/bin/python3 gui.py ' + ' '.join(sys.argv[1:])
    SyS(cmd)

def facefusion_launch():
    cmd = f"source activate default && /tmp/venv-fusion/bin/python3 facefusion.py run {' '.join(shlex.quote(arg) for arg in sys.argv[1:])}"
    webui = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=sys.stdout, text=True, shell=True, executable="/bin/bash")

    for line in webui.stdout:
        print(line, end='')

    webui.wait()

if __name__ == '__main__':
    try:
        setENV()

        if ui == 'FaceFusion':
            facefusion_launch()
        elif ui == 'SDTrainer':
            sdtrainer_launch()
        else:
            Launch()
    except KeyboardInterrupt:
        pass
