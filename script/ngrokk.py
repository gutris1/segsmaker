import os, subprocess, sys

if 'LD_PRELOAD' not in os.environ:
    os.environ['LD_PRELOAD'] = '/home/studio-lab-user/.conda/envs/default/lib/libtcmalloc_minimal.so.4'

def launch(token, args):
    cmd = ['/tmp/venv/bin/python3', 'launch.py'] + args + ['--ngrok', token]
    subprocess.run(cmd)

def main():
    try:
        if len(sys.argv) < 2:
            sys.exit(1)

        token = sys.argv[1]
        args = sys.argv[2:]

        launch(token, args)

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()