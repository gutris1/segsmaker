import subprocess
import os

minyak = [
    ['rm', '-rf', '~/tmp/*', '~/tmp', '~/ComfyUI/models/loras', '~/ComfyUI/models/controlnet'],
    ['ln', '-vs', '/tmp', '~/tmp'],
    ['ln', '-vs', '/tmp/Lora', '~/ComfyUI/models/loras'],
    ['ln', '-vs', '/tmp/ControlNet', '~/ComfyUI/models/controlnet']
]

for tepung in minyak:
    gorengan = [os.path.expanduser(arg) for arg in tepung]
    subprocess.run(gorengan, check=True)