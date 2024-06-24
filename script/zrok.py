import os, subprocess, sys, json, re
from threading import Thread
from pathlib import Path

if 'LD_PRELOAD' not in os.environ:
    os.environ['LD_PRELOAD'] = '/home/studio-lab-user/.conda/envs/default/lib/libtcmalloc_minimal.so.4'

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

def launch(zrok):
    with open('launch.txt', 'w') as log_file:
        webui = subprocess.Popen([
            '/tmp/venv/bin/python3',
            'launch.py'] + sys.argv[2:],
            stdout=subprocess.PIPE,
            stderr=sys.stdout,
            text=True)

        zrok_process = subprocess.Popen([
            "zrok",
            "share",
            "public",
            "localhost:7860",
            "--headless"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True)

        zrok.append(zrok_process)

        local_url = False
        for line in webui.stdout:
            print(line, end='')
            if not local_url:
                log_file.write(line)
                log_file.flush()
                if 'Running on local URL' in line:
                    local_url = True

        webui.wait()
        zrok[0].terminate()

def zrok_url(zrok):
    zrok_io = re.compile(r'https?://[^\s]*\.zrok\.io')
    zrok_url = None

    while not zrok:
        pass

    for line in zrok[0].stdout:
        urls = zrok_io.findall(line)
        if urls:
            zrok_url = urls[0]
            break

    while True:
        with open('launch.txt', 'r') as file:
            if any('Running on local URL' in line for line in file):
                print(f'\n【ZROK】{zrok_url}')
                return

try:
    if len(sys.argv) < 2:
        sys.exit(1)

    token = sys.argv[1]
    zrok_enable(token)

    zrok = []
    app = Thread(target=launch, args=(zrok,))
    url = Thread(target=zrok_url, args=(zrok,))

    app.start()
    url.start()

    app.join()
    url.join()

except KeyboardInterrupt:
    pass
