import subprocess
import os

minyak = [
    ['rm', '-rf', '/kaggle/temp/*', '/kaggle/working/asd/models/Stable-diffusion', '/kaggle/working/asd/models/Lora', '/kaggle/working/asd/outputs'],
    ['mkdir', '-p', '/kaggle/working/asd/models/ESRGAN'],
    ['ln', '-vs', '/kaggle/temp/checkpoint', '/kaggle/working/asd/models/Stable-diffusion'],
    ['ln', '-vs', '/kaggle/temp/lora', '/kaggle/working/asd/models/Lora'],
    ['ln', '-vs', '/kaggle/temp/output', '/kaggle/working/asd/outputs'],
    ['unzip', '-o', '/kaggle/working/asd/embeddings.zip', '-d', '/kaggle/working/asd/embeddings'],
    ['rm', '/kaggle/working/asd/embeddings.zip'],
    ['mkdir', '-p', '/kaggle/temp/checkpoint', '/kaggle/temp/lora', '/kaggle/temp/output']]

for tepung in minyak:
    gorengan = [os.path.expanduser(arg) for arg in tepung]
    subprocess.run(gorengan, check=True)
