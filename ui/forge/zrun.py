import subprocess
import sys
import os
import re
from pathlib import Path

os.environ['LD_PRELOAD'] = '/home/studio-lab-user/.conda/envs/default/lib/libtcmalloc_minimal.so.4'

def zrok_enable(token):
    oppai = subprocess.run(['/home/studio-lab-user/.zrok/bin/zrok', 'enable', token],
                           check=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    if oppai.returncode == 0:
        print(f"\n[ZROK] environment enabled.\n")

def zrok_launch(launch_args):
    tmp = ["/tmp/models", "/tmp/Lora", "/tmp/ControlNet", "/tmp/svd", "/tmp/z123"]
    for dir in tmp:
        Path(dir).mkdir(parents=True, exist_ok=True)

    try:
        zrok_ = subprocess.Popen(["/home/studio-lab-user/.zrok/bin/zrok", "share", "public", "localhost:7860", "--headless"],
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        launch_process = subprocess.Popen(['python', 'launch.py'] + launch_args,
                                          stdout=sys.stdout, stderr=sys.stdout, text=True)
        
        get_url = re.compile(r'https?://[^\s]*\.zrok\.io')
        for line in zrok_.stdout:
            urls = get_url.findall(line)
            for url in urls:
                print(f"\n[ZROK] {url}\n")
                
        zrok_.wait()
        
    except:
        pass

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    
    token = sys.argv[1]
    launch_args = sys.argv[2:]
    
    zrok_enable(token)
    zrok_launch(launch_args)
