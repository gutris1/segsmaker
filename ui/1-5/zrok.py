import sys
import subprocess

def hitozuma(token):
    oppai = subprocess.run(['/home/studio-lab-user/.zrok/bin/zrok', 'enable', token], 
                            check=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    if oppai.returncode == 0:
        print("")
    else:
        print("")

    ass = "/home/studio-lab-user/.zrok/bin/zrok share public localhost:7860 --headless 2>&1 | grep 'zrok.io'"
    subprocess.run(ass, shell=True, stdout=sys.stdout, stderr=subprocess.STDOUT)

if __name__ == '__hitozuma__':
    if len(sys.argv) != 2:
        sys.exit(1)

    hitozuma(sys.argv[1])