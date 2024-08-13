import subprocess, sys, os, logging
from pathlib import Path

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
    if 'LD_PRELOAD' not in os.environ:
        os.environ['LD_PRELOAD'] = '/home/studio-lab-user/.conda/envs/default/lib/libtcmalloc_minimal.so.4'

    webui = subprocess.Popen(['/tmp/venv/bin/python3', 'launch.py'] + sys.argv[1:],
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

if __name__ == '__main__':
    logger = logging_launch()
    try:
        launch(logger)
    except KeyboardInterrupt:
        pass
