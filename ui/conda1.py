from IPython.display import HTML, display
import subprocess

def ass(command, message, color):
    display(HTML(f"<span style='color:{color};'>・・・ {message} ・・・</span>"))
    result = subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

ass('conda install -qy conda=23.11.0 glib psutil', 'Installing Conda', 'cyan')
ass('conda install -q -y -n base python=3.10.12', 'Installing Python 3.10.12', '#D48900')
ass('conda clean -y --all', 'Cleaning Conda Environment', '#66ff00')
ass('curl -Lo ~/.ipython/profile_default/startup/pantat88.py https://github.com/gutris1/segsmaker/raw/main/ui/asd88.py', 'gathering magic', 'red')
get_ipython().kernel.do_shutdown(True)
