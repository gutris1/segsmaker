from pathlib import Path
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

TCM = '/home/studio-lab-user/.conda/envs/default/lib/libtcmalloc_minimal.so.4'
VENVLIB = '/tmp/venv/lib'
VENVBIN = '/tmp/venv/bin'

def setENV():
    if ui in ['FaceFusion', 'SDTrainer']:
        import matplotlib
        iRON['MPLBACKEND'] = 'gtk3agg'

        if ui == 'FaceFusion':
            iRON.pop('LD_PRELOAD', None)
            iRON.pop('LD_LIBRARY_PATH', None)

            iRON['LD_PRELOAD'] = (
                '/home/studio-lab-user/.conda/envs/default/lib/libcublasLt.so.12:' +
                '/home/studio-lab-user/.conda/envs/default/lib/libcublas.so.12:' +
                '/home/studio-lab-user/.conda/envs/default/lib/libtcmalloc_minimal.so.4'
            )
            iRON['LD_LIBRARY_PATH'] = '/home/studio-lab-user/.conda/envs/default/lib:' + iRON.get('LD_LIBRARY_PATH', '')

        else:
            if 'LD_PRELOAD' not in iRON or TCM not in iRON.get('LD_PRELOAD', ''):
                iRON['LD_PRELOAD'] = TCM

    else:
        if 'LD_PRELOAD' not in iRON or TCM not in iRON.get('LD_PRELOAD', ''):
            iRON['LD_PRELOAD'] = TCM
        if 'LD_LIBRARY_PATH' not in iRON or VENVLIB not in iRON.get('LD_LIBRARY_PATH', ''):
            iRON['LD_LIBRARY_PATH'] = VENVLIB + ":" + iRON.get('LD_LIBRARY_PATH', '')
        if VENVBIN not in iRON.get("PATH", ''):
            iRON["PATH"] = VENVBIN + ":" + iRON.get("PATH", '')

        if ui == 'SwarmUI':
            iRON['SWARMPATH'] = str(cwd)
            iRON['SWARM_NO_VENV'] = 'true'

    iRON['PYTHONWARNINGS'] = 'ignore'

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

            if ui == 'Forge':
                FT = cwd / "FT.txt"
                if not FT.exists():
                    SyS('pip uninstall -qy transformers')
                    FT.write_text("blyat")

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

        whichUI = {
            'FaceFusion': facefusion_launch,
            'SDTrainer': sdtrainer_launch
        }

        whichUI.get(ui, Launch)()
    except KeyboardInterrupt:
        pass
