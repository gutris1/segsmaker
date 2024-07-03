import os, sys

if 'LD_PRELOAD' not in os.environ:
    os.environ['LD_PRELOAD'] = '/home/studio-lab-user/.conda/envs/default/lib/libtcmalloc_minimal.so.4'

def launch(token, args):
    cmd = '/tmp/venv/bin/python3 launch.py ' + ' '.join(args) + f' --ngrok {token}'
    os.system(cmd)

if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            sys.exit(1)

        token = sys.argv[1]
        args = sys.argv[2:]

        launch(token, args)

    except KeyboardInterrupt:
        pass
