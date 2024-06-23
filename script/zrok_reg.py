from IPython import get_ipython
from pathlib import Path
from nenen88 import say

def zrok_install():
    home = Path.home()
    zrok = home / ".zrok/bin"
    
    if zrok.exists():
        return

    zrok.mkdir(parents=True, exist_ok=True)
    url = "https://github.com/openziti/zrok/releases/download/v0.4.32/zrok_0.4.32_linux_amd64.tar.gz"
    name = zrok / Path(url).name

    get_ipython().system(f"curl -sLo {name} {url}")
    get_ipython().system(f"tar -xzf {name} -C {zrok} --wildcards *zrok")
    get_ipython().system(f"rm -rf {home}/.cache/*")

zrok_install()

print("\nCopy and Paste this command into Terminal\n")
say("~/.zrok/bin/zrok invite{orange}")
print("""
press Tab to move the cursor
or you can watch this short video https://youtu.be/prTD99GbWlQ
""")
