import subprocess
import os

minyak = [
    ['rm', '-rf', '~/tmp/*', '~/tmp', '~/asd/models/Stable-diffusion/tmp_models', '~/asd/models/Lora/tmp_Lora'],
    ['mkdir', '-p', '~/asd/models/Lora'],
    ['mkdir', '-p', '~/asd/models/ESRGAN'],
    ['ln', '-vs', '/tmp', '~/tmp'],
    ['ln', '-vs', '/tmp/models', '~/asd/models/Stable-diffusion/tmp_models'],
    ['ln', '-vs', '/tmp/Lora', '~/asd/models/Lora/tmp_Lora'],
]

for tepung in minyak:
    gorengan = [os.path.expanduser(arg) for arg in tepung]
    subprocess.run(gorengan, check=True)