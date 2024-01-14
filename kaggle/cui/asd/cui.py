import subprocess
import os

minyak = [
    ['rm', '-rf', '/kaggle/temp/*', '/kaggle/temp', '/kaggle/working/ComfyUI/models/checkpoints', '/kaggle/working/ComfyUI/models/loras', '/kaggle/working/ComfyUI/models/controlnet'],
    ['ln', '-vs', '/kaggle/temp/checkpoints', '/kaggle/working/ComfyUI/models/checkpoints'],
    ['ln', '-vs', '/kaggle/temp/loras', '/kaggle/working/ComfyUI/models/loras'],
    ['ln', '-vs', '/kaggle/temp/controlnet', '/kaggle/working/ComfyUI/models/controlnet']
]

for tepung in minyak:
    gorengan = [os.path.expanduser(arg) for arg in tepung]
    subprocess.run(gorengan, check=True)