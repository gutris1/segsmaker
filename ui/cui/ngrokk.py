from threading import Timer
from queue import Queue
from pyngrok import ngrok
from pathlib import Path
import sys, os

def ngrok_tunnel(port, queue, auth_token):
    ngrok.set_auth_token(auth_token)
    url = ngrok.connect(port)
    queue.put(url)

if __name__ == "__main__":
    try:
        if len(sys.argv) < 3:
            sys.exit(1)

        if 'LD_PRELOAD' not in os.environ:
            os.environ['LD_PRELOAD'] = '/home/studio-lab-user/.conda/envs/default/lib/libtcmalloc_minimal.so.4'

        token = sys.argv[1]
        args = sys.argv[2:]

        ngrok_queue = Queue()
        ngrok_thread = Timer(2, ngrok_tunnel, args=(8188, ngrok_queue, token))
        ngrok_thread.start()
        ngrok_thread.join()
        print(ngrok_queue.get())

        os.system(f"/tmp/venv/bin/python3 main.py {' '.join(args)}")
    except KeyboardInterrupt:
        pass
