import subprocess, sys, os, time
from threading import Thread, Event
from pathlib import Path

R = '\033[0m'
O = '\033[38;5;208m'
T = f'{O}▶{R} PINGGY {O}:{R}'

if 'LD_PRELOAD' not in os.environ:
    os.environ['LD_PRELOAD'] = '/home/studio-lab-user/.conda/envs/default/lib/libtcmalloc_minimal.so.4'

event = Event()

def launch():
    with open('launch.txt', 'w') as log_file:
        webui = subprocess.Popen([
            '/tmp/venv/bin/python3',
            'launch.py'] + sys.argv[1:],
            stdout=subprocess.PIPE,
            stderr=sys.stdout,
            text=True)

        ssh = subprocess.Popen([
            'ssh',
            '-o',
            'StrictHostKeyChecking=no',
            '-p',
            '80',
            '-R0:localhost:7860',
            'a.pinggy.io'],
            stdout=open('pinggy.txt', 'w'),
            stderr=sys.stdout)

        local_url = False
        for line in webui.stdout:
            print(line, end='')
            if not local_url:
                log_file.write(line)
                log_file.flush()
                if 'Running on local URL' in line:
                    local_url = True

        webui.wait()
        ssh.terminate()

def pinggy():
    while not event.is_set():
        with open('launch.txt', 'r') as file:
            if any('Running on local URL' in line for line in file):
                break

    if event.is_set():
        return

    while not event.is_set():
        with open('pinggy.txt', 'r') as file:
            for line in file:
                if 'http:' in line and '.pinggy.link' in line:
                    url = line[line.find('http://'):line.find('.pinggy.link') + len('.pinggy.link')]
                    print(f'\n{T} {url}')
                    return

try:
    cwd = Path.cwd()
    timer = cwd / "asd" / "pinggytimer.txt"
    end_time = int(time.time()) + 3600

    os.system(f"echo -n {end_time} > {timer}")

    app = Thread(target=launch)
    url = Thread(target=pinggy)

    app.start()
    url.start()

    app.join()
    event.set()
    url.join()
except KeyboardInterrupt:
    pass
