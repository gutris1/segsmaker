import os
import subprocess

fff = {"shell": True, "stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL}

def zrok_in():
    zorok = f"{xxx}/.zrok/bin"
    os.makedirs(zorok, exist_ok=True)
    tarok = f"{zorok}/zrok_0.4.25_linux_amd64.tar.gz"
    subprocess.run(f"curl -sLo {tarok} https://github.com/openziti/zrok/releases/download/v0.4.25/zrok_0.4.25_linux_amd64.tar.gz", **fff)
    subprocess.run(f"tar -xzf {tarok} -C {zorok} --wildcards *zrok", **fff)
    os.remove(tarok)
            print("""
Copy and Paste this command
~/.zrok/bin/zrok invite
into Terminal
press Tab to move the cursor

or you can watch this short video https://youtu.be/prTD99GbWlQ
""")

zrok_in()