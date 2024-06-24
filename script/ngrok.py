import os, sys

def launch(token):
    if 'LD_PRELOAD' not in os.environ:
        os.environ['LD_PRELOAD'] = '/home/studio-lab-user/.conda/envs/default/lib/libtcmalloc_minimal.so.4'

    os.system(f"/tmp/venv/bin/python3 launch.py --ngrok {token} " + " ".join(sys.argv[2:]))

try:
    if len(sys.argv) < 2:
        sys.exit(1)
    
    token = sys.argv[1]
    launch(token)

except KeyboardInterrupt:
    pass
