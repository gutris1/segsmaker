import subprocess, sys, os, logging, time
from pathlib import Path

def logging_launch():
    log_file = Path('segsmaker.log')
    log_file.write_text('A1111 or Forge\n')
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="{message}", style="{"
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
    cwd = Path.cwd()
    timer = cwd / "asd" / "pinggytimer.txt"
    end_time = int(time.time()) + 3600
    os.system(f"echo -n {end_time} > {timer}")

    logger = logging_launch()
    try:
        launch(logger)
    except KeyboardInterrupt:
        pass
