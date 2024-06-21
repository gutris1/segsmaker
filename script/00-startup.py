import os, sys

boa = '/tmp/venv/bin/python3'
os.environ['PYTHONPATH'] = f"{os.environ.get('PYTHONPATH', '')}:{boa}"
sys.path.append("/home/studio-lab-user/.ipython/profile_default/startup")
