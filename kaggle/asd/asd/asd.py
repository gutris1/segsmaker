import subprocess
import os

jalanan = [
    'rm -rf /kaggle/temp/* /kaggle/working/asd/models/Stable-diffusion /kaggle/working/asd/models/Lora /kaggle/working/asd/outputs',
    'mkdir -p /kaggle/working/asd/models/ESRGAN',
    'ln -vs /kaggle/temp/checkpoint /kaggle/working/asd/models/Stable-diffusion',
    'ln -vs /kaggle/temp/lora /kaggle/working/asd/models/Lora',
    'ln -vs /kaggle/temp/output /kaggle/working/asd/outputs',
    'mkdir -p /kaggle/temp/checkpoint /kaggle/temp/lora /kaggle/temp/output /kaggle/temp/svd /kaggle/temp/z123']

for janda in jalanan:
    bocil = os.path.expanduser(janda)
    subprocess.run(bocil, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
def zzz():
    try:
        zorok = "/kaggle/working/asd/zrok/bin"
        os.makedirs(zorok, exist_ok=True)
        subprocess.run(["curl", "-sLO", "https://github.com/openziti/zrok/releases/download/v0.4.25/zrok_0.4.25_linux_amd64.tar.gz"], check=True)
        subprocess.run(["tar", "-xzf", "zrok_0.4.25_linux_amd64.tar.gz", "-C", zorok, "--wildcards", "*zrok"], check=True)
        os.remove("zrok_0.4.25_linux_amd64.tar.gz")

    except Exception as e:
        print(f"An error occurred: {e}")

zzz()
