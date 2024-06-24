from pathlib import Path
import os

comfyui = Path.home() / "ComfyUI"
if comfyui.exists():
    ckpt = comfyui / "models/checkpoints_symlink"
    src = comfyui / "models/checkpoints"
    os.system(f"unlink {ckpt}")
    os.system(f"ln -vs {src} {ckpt}")
