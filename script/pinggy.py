from multiprocessing import Process
from pathlib import Path
import sys, time, os

if 'LD_PRELOAD' not in os.environ:
    os.environ['LD_PRELOAD'] = '/home/studio-lab-user/.conda/envs/default/lib/libtcmalloc_minimal.so.4'

tmp = ["/tmp/ckpt", "/tmp/lora", "/tmp/controlnet", "/tmp/svd", "/tmp/z123"]
for path in tmp:
    Path(path).mkdir(parents=True, exist_ok=True)

def launch():
    os.system(f'/tmp/venv/bin/python3 launch.py {" ".join(sys.argv[1:])} &'
              f'ssh -o StrictHostKeyChecking=no -p 80 -R0:localhost:7860 a.pinggy.io > log.txt')

def pinggy():
    time.sleep(2)
    with open('log.txt', 'r') as file:
        for line in file:
            if 'http:' in line and '.pinggy.link' in line:
                url = line[line.find('http:'):line.find('.pinggy.link') + len('.pinggy.link')]
                print(f'\n[pinggy] {url}\n')
                return

p_app = Process(target=launch)
p_url = Process(target=pinggy)

p_app.start()
p_url.start()

p_app.join()
p_url.join()
