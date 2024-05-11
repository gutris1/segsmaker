import subprocess, sys, os, re, json, threading
from multiprocessing import Process, Queue
from pathlib import Path
from queue import Empty

os.environ['LD_PRELOAD'] = '/home/studio-lab-user/.conda/envs/default/lib/libtcmalloc_minimal.so.4'

def zrok_enable(token, zrok_output):
    try:
        _file = Path('/home/studio-lab-user/.zrok/environment.json')
        _token = False
        if _file.exists():
            with _file.open('r') as f:
                _value = json.load(f)
                if 'zrok_token' in _value and _value['zrok_token'] == token:
                    _token = True

        if not _token:
            _enable = subprocess.run(
                ['/home/studio-lab-user/.zrok/bin/zrok', 'enable', token],
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            if _enable.returncode == 0:
                zrok_output.put(f"\n[ZROK] environment enabled.")

        _share = subprocess.Popen(
            ["/home/studio-lab-user/.zrok/bin/zrok", "share", "public", "localhost:7860", "--headless"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        _url = re.compile(r'https?://[^\s]*\.zrok\.io')

        for line in _share.stdout:
            urls = _url.findall(line)
            for url in urls:
                zrok_output.put(f"\n[ZROK] {url}\n")

        _share.wait()

    except:
        pass


def zrok_launch(token, launch_args, zrok_output):
    tmp = ["/tmp/models", "/tmp/Lora", "/tmp/ControlNet", "/tmp/svd", "/tmp/z123"]
    for dir in tmp:
        Path(dir).mkdir(parents=True, exist_ok=True)
    
    try:
        _process = subprocess.Popen(
            ['python', 'launch.py'] + launch_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        def zrok_url(process):
            try:
                if process.stdout is not None:
                    for line in process.stdout:
                        print(line.strip())
                        if "Running on local URL" in line:
                            while not zrok_output.empty():
                                print(zrok_output.get(), end='', flush=True)
                        
            except Exception:
                pass

        _launch = threading.Thread(target=zrok_url, args=(_process,))

        _launch.start()
        _launch.join()

    except KeyboardInterrupt:
        pass
    
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    
    token = sys.argv[1]
    launch_args = sys.argv[2:]
    zrok_output = Queue()

    process = Process(target=zrok_enable, args=(token, zrok_output))
    process.start()

    zrok_launch(token, launch_args, zrok_output)
