import subprocess
import os

minyak = [
    ['rm', '-rf', '~/tmp/*', '~/tmp', '~/asd/models/Stable-diffusion', '~/asd/models/Lora', '~/asd/models/ControlNet'],
    ['mkdir', '-p', '~/asd/models/ESRGAN'],
    ['ln', '-vs', '/tmp', '~/tmp'],
    ['ln', '-vs', '/tmp/models', '~/asd/models/Stable-diffusion'],
    ['ln', '-vs', '/tmp/Lora', '~/asd/models/Lora'],
    ['ln', '-vs', '/tmp/ControlNet', '~/asd/models/ControlNet']
]

for tepung in minyak:
    gorengan = [os.path.expanduser(arg) for arg in tepung]
    subprocess.run(gorengan, check=True)