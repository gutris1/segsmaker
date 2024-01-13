import subprocess

tempe = [
    ['ln', '-vs', '/tmp', '~/tmp'],
    ['ln', '-vs', '/tmp/models', '~/asd/models/Stable-diffusion/tmp_models'],
    ['ln', '-vs', '/tmp/Lora', '~/asd/models/Lora/tmp_Lora'],
    ['ln', '-vs', '/tmp/ControlNet', '~/asd/models/ControlNet']
]

for tahu in tempe:
    subprocess.run(tahu, check=True)
