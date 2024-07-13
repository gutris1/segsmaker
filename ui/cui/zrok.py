import os, sys, json, re, subprocess, time
from threading import Thread
from pathlib import Path

R = '\033[0m'
O = '\033[38;5;208m'
T = f'{O}▶{R} ZROK {O}:{R}'

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
    webui = subprocess.Popen(['/tmp/venv/bin/python3', 'main.py'] + sys.argv[2:])
    zrok.append(subprocess.Popen([
        "zrok",
        "share",
        "public",
        "localhost:8188",
        "--headless"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True))

    webui.wait()
    zrok[0].terminate()

def zrok_url(zrok):
    time.sleep(2)
    get_url = re.compile(r'https?://[^\s]*\.zrok\.io')
    
    for line in zrok[0].stdout:
        urls = get_url.findall(line)
        for url in urls:
            print(f"{T} {url}\n")
            break

        if 'ERROR' in line:
            print(f"\n{line}")
            return

if __name__ == "__main__":
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
        print('\nZROK killed.\n')
