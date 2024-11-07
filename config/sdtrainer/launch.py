import os
os.environ['MPLBACKEND'] = 'gtk3agg'
import matplotlib, subprocess, sys, logging, json, re, shlex, threading
from pathlib import Path
from pyngrok import ngrok

SRC = Path.home() / '.gutris1'
MARK = SRC / 'marking.json'
RST = '\033[0m'
ORG = '\033[38;5;208m'

def logging_launch():
    log_file = Path('segsmaker.log')
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="{message}", style="{",
        filemode='a'
    )
    return logging.getLogger()

def read_stderr(webui, logger, url_event):
    while True:
        line = webui.stderr.readline()
        if line:
            print(line, end='')
            logger.info(line.strip())

            if any(keyword in line for keyword in ['http://127.0.0.1:6006/']):
                url_event.set()
                for handler in logger.handlers:
                    logger.removeHandler(handler)

        else:
            if webui.poll() is not None:
                break

def launch(logger, args):
    cmd = f"/tmp/venv-sd-trainer/bin/python3 gui.py {' '.join(shlex.quote(arg) for arg in args)}"
    webui = subprocess.Popen(shlex.split(cmd), stdout=sys.stdout, stderr=subprocess.PIPE, text=True)

    url_event = threading.Event()
    std_err = threading.Thread(target=read_stderr, args=(webui, logger, url_event))
    std_err.start()

    return webui, std_err, url_event

def ngrok_tunnel(port, auth_token):
    ngrok.set_auth_token(auth_token)
    url = ngrok.connect(port)

    match = re.search(r'"(https?://[^"]+)"', str(url))
    if match:
        return match.group(1)
    return None

def load_config(logger):
    config = json.load(MARK.open('r')) if MARK.exists() else {}
    tunnel = config.get('tunnel')

    args = sys.argv[1:]

    if tunnel == 'NGROK':
        token = config.get('ngrok_token', '').strip()
        if not token:
            sys.exit("Missing NGROK Token")

        port = 28000
        webui, std_err, url_event = launch(logger, args)
        url_event.wait()
        url = ngrok_tunnel(port, token)
        print(f'\n{ORG}▶{RST} NGROK {ORG}:{RST} {url}')

        webui.wait()
        ngrok.disconnect(url)

        std_err.join()

    else:
        webui, std_err, _ = launch(logger, args)
        webui.wait()
        std_err.join()

if __name__ == '__main__':
    if 'LD_PRELOAD' not in os.environ:
        os.environ['LD_PRELOAD'] = '/home/studio-lab-user/.conda/envs/default/lib/libtcmalloc_minimal.so.4'

    logger = logging_launch()

    try:
        load_config(logger)
    except KeyboardInterrupt:
        pass
