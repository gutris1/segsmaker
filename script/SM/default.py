from IPython import get_ipython
from pathlib import Path

conda = Path('/home/studio-lab-user/.conda/envs/default')
py = conda / 'bin/python'
SyS = get_ipython().system

if not py.exists():
    SyS(f'conda create -qy -p {conda} python=3.10.13')
    SyS(f'{py} -m pip install -q ipykernel ipywidgets')
    SyS(f'{py} -m ipykernel install --user --name default --display-name "default"')
    print('\nRestart JupyterLab... then switch kernel to default:Python')
