import subprocess, sys, os, time, shlex, json
from pathlib import Path

MARK = Path.home() / '.gutris1/marking.json'
    
def launch():
    config = json.load(MARK.open('r'))
    tunnel = config.get('tunnel')

    cmd = '/tmp/venv/bin/python3 launch.py ' + ' '.join(sys.argv[1:])

    if tunnel == 'Pinggy':
        cwd = Path.cwd()
        timer = cwd / "asd" / "pinggytimer.txt"
        end_time = int(time.time()) + 3600
        os.system(f"echo -n {end_time} > {timer}")

    if tunnel == 'NGROK':
        token = config.get('ngrok_token', '').strip()
        if not token:
            sys.exit("Missing NGROK Token")

        cmd += f' --ngrok {token}'

    os.system(cmd)

if __name__ == '__main__':
    if 'LD_PRELOAD' not in os.environ:
        os.environ['LD_PRELOAD'] = '/home/studio-lab-user/.conda/envs/default/lib/libtcmalloc_minimal.so.4'

    try:
        launch()
    except KeyboardInterrupt:
        pass
