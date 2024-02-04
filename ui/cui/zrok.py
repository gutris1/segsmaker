import subprocess
import sys
import os
import re
import threading

plock = threading.Lock()

def hitozuma(token):
    
    os.environ['LD_PRELOAD'] = '/home/studio-lab-user/.conda/envs/default/lib/libtcmalloc_minimal.so.4'
    
    try:
        oppai = subprocess.run(['/home/studio-lab-user/.zrok/bin/zrok', 'enable', token], 
                                check=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        ass = subprocess.Popen(["/home/studio-lab-user/.zrok/bin/zrok", "share", "public", "localhost:7860", "--headless"],
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        urlp = re.compile(r'https?://[^\s]*\.zrok\.io')
        
        if oppai.returncode == 0:
            print("\n[ZROK] environment enabled.")
            
        else:
            if "enabled environment" in oppai.stdout:
                print("\n[ZROK] environment already enabled.")
            else:
                print(oppai.stdout)

        for line in ass.stdout:
            urls = urlp.findall(line)
            for url in urls:
                zurl(f"[ZROK] {url}\n")

        ass.wait()

    except:
        pass

def zurl(url):
    with plock:
        print(url)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("")

    hitozuma(sys.argv[1])
