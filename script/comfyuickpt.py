from pathlib import Path
import os

webui = Path.home() / "ComfyUI"
if webui.exists():
    ckpt = webui / "models" / "checkpoints_symlink"
    if not ckpt.exists():
        src = webui / "models" / "checkpoints"
        cmd = f"ln -vs {src} {ckpt}"
        os.system(cmd)

    else:
        pass
else:
    pass
