import subprocess
import os

minyak = [
    ['rm', '-rf', '/kaggle/temp/*', '/kaggle/temp', '/kaggle/working/asd/models/Stable-diffusion/tmp_models', '/kaggle/working/asd/models/Lora/tmp_Lora'],
    ['mkdir', '-p', '/kaggle/working/asd/models/Lora'],
    ['mkdir', '-p', '/kaggle/working/asd/models/ESRGAN'],
    ['ln', '-vs', '/kaggle/temp/models', '/kaggle/working/asd/models/Stable-diffusion/tmp_models'],
    ['ln', '-vs', '/kaggle/temp/Lora', '/kaggle/working/asd/models/Lora/tmp_Lora'],
]

for tepung in minyak:
    subprocess.run(tepung, check=True)