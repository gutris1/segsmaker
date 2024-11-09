import subprocess, sys, os, time, shlex, json
from pathlib import Path

MARK = Path.home() / '.gutris1/marking.json'

config = json.load(MARK.open('r'))
tunnel = config.get('tunnel')
ui = config.get('ui')

def launch():
    launcher = 'main.py' if ui == 'ComfyUI' else 'launch.py'
    cmd = f'/tmp/venv/bin/python3 {launcher} ' + ' '.join(sys.argv[1:])

    if ui in ['A1111', 'Forge', 'ReForge']:
        if tunnel == 'Pinggy':
            cwd = Path.cwd()
            timer = cwd / "asd" / "pinggytimer.txt"
            end_time = int(time.time()) + 3600
            os.system(f"echo -n {end_time} > {timer}")

    os.system(cmd)

if __name__ == '__main__':
    if 'LD_PRELOAD' not in os.environ:
        os.environ['LD_PRELOAD'] = '/home/studio-lab-user/.conda/envs/default/lib/libtcmalloc_minimal.so.4'

    try:
        launch()
    except KeyboardInterrupt:
        pass
