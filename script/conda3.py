from IPython.display import HTML, display
import subprocess

def ass(cmd, bacod, color):
    display(HTML(f"<span style='color:{color};'>{bacod}</span>"))
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

ass('conda install -y conda glib gxx_linux-64 ffmpeg imageio imageio-ffmpeg av gst-libav pyngrok psutil gperftools', '【 Installing Conda 】', 'cyan')
ass('conda install -y -n base python=3.10.12', '【 Installing Python 3.10 】', '#D48900')
ass('conda clean -y --all', '【 Cleaning Conda 】', '#66ff00')
ass('curl -Lo ~/.ipython/profile_default/startup/pantat88.py https://github.com/gutris1/segsmaker/raw/main/script/pantat88.py', '【 Gathering Magic 】', 'red')
ass('curl -Lo ~/.ipython/profile_default/startup/00-startup.py https://github.com/gutris1/segsmaker/raw/main/script/00-startup.py', '', '')
display(HTML('<span style="color: cyan;">【 Done 】</span>'))

from IPython import get_ipython
get_ipython().kernel.do_shutdown(True)
