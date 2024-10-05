import os
os.environ['MPLBACKEND'] = 'gtk3agg'
import matplotlib, subprocess, sys, logging, json, re, shlex
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

def launch(logger, args):
    cmd = f"/tmp/venv-fusion/bin/python3 facefusion.py run {' '.join(shlex.quote(arg) for arg in args)}"
    webui = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=sys.stdout, text=True)

    local_url = False
    for line in webui.stdout:
        print(line, end='')
        logger.info(line.strip())
        if not local_url:
            if any(keyword in line for keyword in ['Running on local URL']):
                local_url = True
                for handler in logger.handlers:
                    logger.removeHandler(handler)
                break

    return webui

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
        try:
            if len(sys.argv) < 2:
                sys.exit("Missing NGROK Token")

            token = sys.argv[1]
            args = sys.argv[2:]
            port = 7860

            webui = launch(logger, args)

            url = ngrok_tunnel(port, token)
            if url:
                print(f'\n{ORG}▶{RST} NGROK {ORG}:{RST} {url}')

            webui.wait()
            ngrok.disconnect(url)

        except KeyboardInterrupt:
            pass
    else:
        args = sys.argv[1:]
        webui = launch(logger, args)
        webui.wait()

if __name__ == '__main__':
    if 'LD_PRELOAD' not in os.environ:
        os.environ['LD_PRELOAD'] = '/home/studio-lab-user/.conda/envs/default/lib/libtcmalloc_minimal.so.4'

    logger = logging_launch()
    try:
        load_config(logger)
    except KeyboardInterrupt:
        pass
