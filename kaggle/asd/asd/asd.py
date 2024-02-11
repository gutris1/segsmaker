import subprocess
import os

minyak = [
    ['rm', '-rf', '/kaggle/working/temp/*', '/kaggle/working/asd/models/Stable-diffusion', '/kaggle/working/asd/models/Lora'],
    ['mkdir', '-p', '/kaggle/working/asd/models/Lora'],
    ['mkdir', '-p', '/kaggle/working/asd/models/ESRGAN'],
    ['ln', '-vs', '/kaggle/working/temp/models', '/kaggle/working/asd/models/Stable-diffusion'],
    ['ln', '-vs', '/kaggle/working/temp/Lora', '/kaggle/working/asd/models/Lora'],
    ['mkdir', '-p', '/kaggle/working/temp/models'],
    ['mkdir', '-p', '/kaggle/working/temp/Lora'],
]

for tepung in minyak:
    subprocess.run(tepung, check=True)