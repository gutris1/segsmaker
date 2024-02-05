from multiprocessing import Process, Queue
import subprocess
import sys
import re

def hitozuma(token, zrok_out):
    try:
        oppai = subprocess.run(['/home/studio-lab-user/.zrok/bin/zrok', 'enable', token], 
                                check=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        ass = subprocess.Popen(["/home/studio-lab-user/.zrok/bin/zrok", "share", "public", "localhost:7860", "--headless"],
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        urlp = re.compile(r'https?://[^\s]*\.zrok\.io')
        asu = ("◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼")
        
        if oppai.returncode == 0:
            zrok_out.put(f"\n{asu}\n[ZROK] environment enabled.\n")
            
        else:
            if "enabled environment" in oppai.stdout:
                zrok_out.put(f"\n{asu}\n[ZROK] environment already enabled.\n")
            else:
                zrok_out.put(oppai.stdout)

        for line in ass.stdout:
            urls = urlp.findall(line)
            for url in urls:
                zrok_out.put(f"[ZROK] {url}\n{asu}\n\n")

        ass.wait()

    except:
        pass

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("")

    zrok_out = Queue()

    process = Process(target=hitozuma, args=(sys.argv[1], zrok_out))
    process.start()

    while process.is_alive() or not zrok_out.empty():
        while not zrok_out.empty():
            print(zrok_out.get(), end='', flush=True)

    process.join()