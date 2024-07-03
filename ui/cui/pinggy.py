import os, sys, subprocess, time
from threading import Thread
from pathlib import Path

R = '\033[0m'
O = '\033[38;5;208m'
T = f'{O}▶{R} PINGGY {O}:{R}'

if 'LD_PRELOAD' not in os.environ:
    os.environ['LD_PRELOAD'] = '/home/studio-lab-user/.conda/envs/default/lib/libtcmalloc_minimal.so.4'

def launch():
    webui = subprocess.Popen(['/tmp/venv/bin/python3', 'main.py'] + sys.argv[1:])
    ssh = subprocess.Popen([
        'ssh',
        '-o',
        'StrictHostKeyChecking=no',
        '-p',
        '80',
        '-R0:localhost:8188',
        'a.pinggy.io'],
        stdout=open('pinggy.txt', 'w'))

    webui.wait()
    ssh.terminate()

def pinggy():
    time.sleep(2)
    with open('pinggy.txt', 'r') as file:
        for line in file:
            if 'http:' in line and '.pinggy.link' in line:
                url = line[line.find('http:'):line.find('.pinggy.link') + len('.pinggy.link')]
                print(f'{T} {url}\n')
                return

app = Thread(target=launch)
url = Thread(target=pinggy)

app.start()
url.start()

app.join()
url.join()
