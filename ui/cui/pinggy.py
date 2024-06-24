import os, sys, subprocess, time
from threading import Thread
from pathlib import Path

if 'LD_PRELOAD' not in os.environ:
    os.environ['LD_PRELOAD'] = '/home/studio-lab-user/.conda/envs/default/lib/libtcmalloc_minimal.so.4'

os.system("find /home/studio-lab-user/ComfyUI -type d -name .ipynb_checkpoints -exec rm -rf {} +")

def launch():
    webui = subprocess.Popen(['/tmp/venv/bin/python3', 'main.py'] + sys.argv[1:])
    ssh = subprocess.Popen(['ssh', '-o', 'StrictHostKeyChecking=no', '-p', '80', '-R0:localhost:8188', 'a.pinggy.io'],
                           stdout=open('log.txt', 'w'))

    webui.wait()
    ssh.terminate()

def pinggy():
    time.sleep(2)
    with open('log.txt', 'r') as file:
        for line in file:
            if 'http:' in line and '.pinggy.link' in line:
                url = line[line.find('http:'):line.find('.pinggy.link') + len('.pinggy.link')]
                print(f'\n【PINGGY】{url}\n')
                return

app = Thread(target=launch)
url = Thread(target=pinggy)

app.start()
url.start()

app.join()
url.join()
