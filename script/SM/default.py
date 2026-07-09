from pathlib import Path
import os

conda = Path('/home/studio-lab-user/.conda/envs/default')
py = conda / 'bin/python'
SyS = os.system

if not py.exists():
    for cmd in [
        f'conda create -qy -p {conda} python=3.10.15',
        f'{py} -m pip install -q ipykernel ipywidgets',
        f'{py} -m ipykernel install --user --name default --display-name "default"'
    ]: SyS(cmd)

    print('\nRestart JupyterLab... then switch kernel to default:Python')
