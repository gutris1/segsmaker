import os, subprocess, sys, json, re
from threading import Thread, Event
from pathlib import Path

R = '\033[0m'
O = '\033[38;5;208m'
T = f'{O}▶{R} ZROK {O}:{R}'

if 'LD_PRELOAD' not in os.environ:
    os.environ['LD_PRELOAD'] = '/home/studio-lab-user/.conda/envs/default/lib/libtcmalloc_minimal.so.4'

event = Event()

def zrok_enable(token):
    zrok = Path('/home/studio-lab-user/.zrok')
    if not zrok.exists():
        print("ZROK is not installed.")
        return

    env = zrok / 'environment.json'
    if env.exists():
        with open(env, 'r') as f:
            value = json.load(f)
            zrok_token = value.get('zrok_token')

        if zrok_token == token:
            pass
        else:
            os.system('zrok disable')
            os.system(f'zrok enable {token}')
    else:
        os.system(f'zrok enable {token}')

def launch():
    with open('launch.txt', 'w') as log_file:
        webui = subprocess.Popen([
            '/tmp/venv/bin/python3',
            'launch.py'] + sys.argv[2:],
            stdout=subprocess.PIPE,
            stderr=sys.stdout,
            text=True)

        zrok = subprocess.Popen([
            "zrok",
            "share",
            "public",
            "localhost:7860",
            "--headless"],
            stdout=open('zrok.txt', 'w'),
            stderr=subprocess.STDOUT)

        local_url = False
        for line in webui.stdout:
            print(line, end='')
            if not local_url:
                log_file.write(line)
                log_file.flush()
                if 'Running on local URL' in line:
                    local_url = True

        webui.wait()
        zrok.terminate()

def zrok_url():
    error = False

    while not event.is_set():
        with open('launch.txt', 'r') as file:
            if any('Running on local URL' in line for line in file):
                break

    if event.is_set():
        return

    while not event.is_set():
        with open('zrok.txt', 'r') as file:
            for line in file:
                if 'https:' in line and '.zrok.io' in line:
                    url = line[line.find('https://'):line.find('.zrok.io') + len('.zrok.io')]
                    print(f'\n{T} {url}')
                    return

                elif 'ERROR' in line:
                    error = True
                    print(f"\n{line}")
                    return
        if error:
            break 

try:
    if len(sys.argv) < 2:
        sys.exit(1)

    token = sys.argv[1]
    zrok_enable(token)

    app = Thread(target=launch)
    url = Thread(target=zrok_url)

    app.start()
    url.start()

    app.join()
    event.set()
    url.join()

except KeyboardInterrupt:
    print('\nZROK killed.\n')
