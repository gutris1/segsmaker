import shlex
import subprocess
from pathlib import Path
from IPython import get_ipython

list_1 = [
    "rm -rf ~/tmp/* ~/tmp ~/ComfyUI/models/checkpoints ~/ComfyUI/models/loras ~/ComfyUI/models/controlnet",
    "unzip -qo ~/ComfyUI/models/embeddings.zip -d ~/ComfyUI/models/embeddings",
    "rm -rf ~/ComfyUI/models/embeddings.zip"
]

list_2 = [
    "ln -vs /tmp ~/tmp",
    "ln -vs /tmp/ckpt ~/ComfyUI/models/checkpoints",
    "ln -vs /tmp/lora ~/ComfyUI/models/loras",
    "ln -vs /tmp/controlnet ~/ComfyUI/models/controlnet"
]

for cmd in list_1:
    get_ipython().system(cmd)

for cmd in list_2:
    run = shlex.split(cmd)
    run = [str(Path(arg).expanduser()) for arg in run]
    subprocess.run(run, check=True)