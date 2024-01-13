import subprocess

tempe = [
    ['rm', '-rf', '~/tmp/*', '~/tmp', '~/asd/models/Stable-diffusion/tmp_models', '~/asd/models/Lora/tmp_Lora', '~/asd/models/ControlNet'],
    ['mkdir', '-p', '~/asd/models/Lora'],
    ['mkdir', '-p', '~/asd/models/ESRGAN'],
    ['ln', '-vs', '/tmp', '~/tmp'],
    ['ln', '-vs', '/tmp/models', '~/asd/models/Stable-diffusion/tmp_models'],
    ['ln', '-vs', '/tmp/Lora', '~/asd/models/Lora/tmp_Lora'],
    ['ln', '-vs', '/tmp/ControlNet', '~/asd/models/ControlNet']
]

for tahu in tempe:
    subprocess.run(tahu, check=True)
