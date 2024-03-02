import subprocess
import os

minyak = [
    ['rm', '-rf', '~/tmp/*', '~/tmp', '~/sdwf/models/Stable-diffusion/tmp_models', '~/sdwf/models/Lora/tmp_Lora', '~/sdwf/models/ControlNet'],
    ['mkdir', '-p', '~/sdwf/models/Lora'],
    ['mkdir', '-p', '~/sdwf/models/ESRGAN'],
    ['ln', '-vs', '/tmp', '~/tmp'],
    ['ln', '-vs', '/tmp/models', '~/sdwf/models/Stable-diffusion/tmp_models'],
    ['ln', '-vs', '/tmp/Lora', '~/sdwf/models/Lora/tmp_Lora'],
    ['ln', '-vs', '/tmp/ControlNet', '~/sdwf/models/ControlNet']]

for tepung in minyak:
    gorengan = [os.path.expanduser(arg) for arg in tepung]
    subprocess.run(gorengan, check=True)