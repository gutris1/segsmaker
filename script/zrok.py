import os, sys, json
from pathlib import Path

def zrok_enable(token):
    zrok = Path('/home/studio-lab-user/.zrok')
    if not zrok.exists():
        print("ZROK is not installed.")
        return

    env = zrok / 'environment.json'
    if env.exists():
        with open(env, 'r') as f:
            value = json.load(f)
            zrok_token = value.get('zrok_token')

        if zrok_token == token:
            pass
        else:
            os.system('zrok disable')
            os.system(f'zrok enable {token}')
    else:
        os.system(f'zrok enable {token}')

def zrok():
    if 'LD_PRELOAD' not in os.environ:
        os.environ['LD_PRELOAD'] = '/home/studio-lab-user/.conda/envs/default/lib/libtcmalloc_minimal.so.4'

    os.system(f"/tmp/venv/bin/python3 launch.py {' '.join(sys.argv[2:])}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)

    token = sys.argv[1]
    zrok_enable(token)
    zrok()
