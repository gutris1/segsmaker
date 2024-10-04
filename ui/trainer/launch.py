import os
os.environ['MPLBACKEND'] = 'gtk3agg'
import matplotlib, subprocess, sys, logging, time, json
from pathlib import Path
from threading import Timer
from queue import Queue
from pyngrok import ngrok

SRC = Path.home() / '.gutris1'
MARK = SRC / 'marking.json'

def logging_launch():
    log_file = Path('segsmaker.log')
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="{message}", style="{",
        filemode='a'
    )
    return logging.getLogger()

def launch(logger):
    webui = subprocess.Popen(['/tmp/venv/bin/python3', 'facefusion.py', 'run'],
                             stdout=subprocess.PIPE, stderr=sys.stdout, text=True)

    local_url = False
    for line in webui.stdout:
        print(line, end='')
        logger.info(line.strip())
        if not local_url:
            if 'Running on local URL' in line:
                local_url = True
                for handler in logger.handlers[:]:
                    handler.flush()
                    handler.close()
                    logger.removeHandler(handler)
    webui.wait()

def load_config():
    config = json.load(MARK.open('r')) if MARK.exists() else {}
    tunnel = config.get('tunnel')

    if tunnel == 'NGROK':
        def ngrok_tunnel(port, queue, auth_token):
            ngrok.set_auth_token(auth_token)
            url = ngrok.connect(port)
            queue.put(url)

        try:
            if len(sys.argv) < 2:
                sys.exit(1)

            token = sys.argv[1]
            
            ngrok_queue = Queue()
            ngrok_thread = Timer(2, ngrok_tunnel, args=(7860, ngrok_queue, token))
            ngrok_thread.start()
            ngrok_thread.join()
            print(ngrok_queue.get())
            print('wait for the local URL')
            os.system(f"/tmp/venv/bin/python3 facefusion.py run")
        except KeyboardInterrupt:
            pass
    else:
        launch(logger)

if __name__ == '__main__':
    if 'LD_PRELOAD' not in os.environ:
        os.environ['LD_PRELOAD'] = '/home/studio-lab-user/.conda/envs/default/lib/libtcmalloc_minimal.so.4'

    logger = logging_launch()
    try:
        load_config()
    except KeyboardInterrupt:
        pass
