import sys, os, time
from pathlib import Path

def pinggy():
    cwd = Path.cwd()
    timer = cwd / "asd" / "pinggytimer.txt"
    end_time = int(time.time()) + 3600

    if 'LD_PRELOAD' not in os.environ:
        os.environ['LD_PRELOAD'] = '/home/studio-lab-user/.conda/envs/default/lib/libtcmalloc_minimal.so.4'

    os.system(f"echo -n {end_time} > {timer}")
    os.system(f"/tmp/venv/bin/python3 launch.py {' '.join(sys.argv[1:])}")

if __name__ == "__main__":
    pinggy()
