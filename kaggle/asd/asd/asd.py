import subprocess
import os

minyak = [
    ['rm', '-rf', '/kaggle/temp/*', '/kaggle/temp', '/kaggle/working/asd/models/Stable-diffusion', '/kaggle/working/asd/models/Lora'],
    ['mkdir', '-p', '/kaggle/working/asd/models/ESRGAN'],
    ['ln', '-vs', '/kaggle/temp/checkpoint', '/kaggle/working/asd/models/Stable-diffusion'],
    ['ln', '-vs', '/kaggle/temp/lora', '/kaggle/working/asd/models/Lora'],
    ['unzip', '-o', '/kaggle/working/asd/embeddings.zip', '-d', '/kaggle/working/asd/embeddings'],
    ['rm', '/kaggle/working/asd/embeddings.zip']]

for tepung in minyak:
    gorengan = [os.path.expanduser(arg) for arg in tepung]
    subprocess.run(gorengan, check=True)
