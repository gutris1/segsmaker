import os
import subprocess

jalanan = [
    'rm -rf ~/tmp/* ~/tmp ~/sdwf/models/Stable-diffusion/tmp_models ~/sdwf/models/Lora/tmp_Lora ~/sdwf/models/ControlNet ~/sdwf/models/svd ~/sdwf/models/z123',
    'mkdir -p ~/sdwf/models/Lora',
    'mkdir -p ~/sdwf/models/ESRGAN',
    'ln -vs /tmp ~/tmp',
    'ln -vs /tmp/models ~/sdwf/models/Stable-diffusion/tmp_models',
    'ln -vs /tmp/svd ~/sdwf/models/svd',
    'ln -vs /tmp/z123 ~/sdwf/models/z123',
    'ln -vs /tmp/Lora ~/sdwf/models/Lora/tmp_Lora',
    'ln -vs /tmp/ControlNet ~/sdwf/models/ControlNet']

for janda in jalanan:
    bocil = os.path.expanduser(janda)
    subprocess.run(bocil, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
