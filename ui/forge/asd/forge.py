import os
import subprocess

jalanan = [
    'rm -rf ~/tmp/* ~/tmp ~/forge/models/Stable-diffusion/tmp_models ~/forge/models/Lora/tmp_Lora ~/forge/models/ControlNet ~/forge/models/svd ~/forge/models/z123',
    'mkdir -p ~/forge/models/Lora',
    'mkdir -p ~/forge/models/ESRGAN',
    'ln -vs /tmp ~/tmp',
    'ln -vs /tmp/models ~/forge/models/Stable-diffusion/tmp_models',
    'ln -vs /tmp/svd ~/forge/models/svd',
    'ln -vs /tmp/z123 ~/forge/models/z123',
    'ln -vs /tmp/Lora ~/forge/models/Lora/tmp_Lora',
    'ln -vs /tmp/ControlNet ~/forge/models/ControlNet']

for janda in jalanan:
    bocil = os.path.expanduser(janda)
    subprocess.run(bocil, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
