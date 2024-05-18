from IPython import get_ipython
from pathlib import Path
from nenen88 import say

xxx = "/home/studio-lab-user"

def zrok_install():
    zrok = Path(f"{xxx}/.zrok/bin")
    zrok.mkdir(parents=True, exist_ok=True)
    url = "https://github.com/openziti/zrok/releases/download/v0.4.25/zrok_0.4.25_linux_amd64.tar.gz"
    z = zrok / Path(url).name

    get_ipython().system(f"curl -sLo {z} {url}")
    get_ipython().system(f"tar -xzf {z} -C {zrok} --wildcards *zrok")
    get_ipython().system(f"rm -rf {xxx}/.cache/* {z}")

    print("\nCopy and Paste this command into Terminal\n")
    say("~/.zrok/bin/zrok invite{orange}")
    print("""
press Tab to move the cursor
or you can watch this short video https://youtu.be/prTD99GbWlQ
""")

zrok_install()