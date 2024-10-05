import subprocess, sys, logging, json, re, shlex, os, threading
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

def read_output(stream, logger, url_event):
    for line in iter(stream.readline, ''):
        print(line, end='')
        logger.info(line.strip())
        if 'To see the GUI go to:' in line:
            url_event.set()
            for handler in logger.handlers:
                logger.removeHandler(handler)

    stream.close()

def launch(logger, args):
    cmd = f"/tmp/venv/bin/python3 main.py {' '.join(shlex.quote(arg) for arg in args)}"
    webui = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    url_event = threading.Event()
    std_out = threading.Thread(target=read_output, args=(webui.stdout, logger, url_event))
    std_err = threading.Thread(target=read_output, args=(webui.stderr, logger, url_event))

    std_out.start()
    std_err.start()

    return webui, std_out, std_err, url_event

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

    if tunnel == 'NGROK':
        token = config.get('ngrok_token', '').strip()

        if not token:
            sys.exit("Missing NGROK Token")

        args = sys.argv[1:]
        port = 8188

        webui, std_out, std_err, url_event = launch(logger, args)

        url_event.wait()
        url = ngrok_tunnel(port, token)
        print(f'\n{ORG}▶{RST} NGROK {ORG}:{RST} {url}')

        webui.wait()
        ngrok.disconnect(url)

        std_out.join()
        std_err.join()

    else:
        args = sys.argv[1:]
        webui, std_out, std_err, _ = launch(logger, args)
        webui.wait()
        std_out.join()
        std_err.join()

if __name__ == '__main__':
    if 'LD_PRELOAD' not in os.environ:
        os.environ['LD_PRELOAD'] = '/home/studio-lab-user/.conda/envs/default/lib/libtcmalloc_minimal.so.4'

    logger = logging_launch()
    try:
        load_config(logger)
    except KeyboardInterrupt:
        pass
