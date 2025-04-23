from importlib.metadata import distribution
from pathlib import Path
import subprocess
import importlib
import sys
import re
import os

RED = '\033[31m'
CYAN = '\033[36m'
ORANGE = '\033[38;5;208m'
RESET = '\033[0m'

def GetsAll(path):
    subdirs = []
    base = Path(path)

    for subdir in os.listdir(base):
        try:
            fp = base / subdir
            if fp.is_dir() and not subdir.endswith('.disabled') and not subdir.startswith('.') and subdir != '__pycache__':
                print(f'Checking > {CYAN}{subdir}{RESET}')
                reqs = fp / 'requirements.txt'
                scripts = fp / 'install.py'

                if reqs.exists() or scripts.exists():
                    subdirs.append((fp, reqs, scripts))
        except Exception as e:
            print(f'EXCEPTION during dependencies check on {RED}{subdir}{RESET}:\n{e}')

    print()
    return subdirs

def Get_git_pkg_name(git_url):
    if git_url.startswith('git+'):
        git_url = git_url[4:]

    if 'github.com' in git_url:
        match = re.search(r'github\.com/[^/]+/([^/.]+)', git_url)
        if match:
            return match.group(1)

    match = re.search(r'/([^/]+)\.git', git_url)
    if match:
        return match.group(1)

    parts = git_url.rstrip('/').split('/')
    return parts[-1] if parts else None

def CheckGit(pkg):
    name = Get_git_pkg_name(pkg)
    if not name:
        return 'install'

    variations = [
        name,
        name.lower(),
        name.replace('-', '_'),
        name.lower().replace('-', '_')
    ]

    for variant in variations:
        try:
            importlib.import_module(variant)
            return 'skip'
        except ImportError:
            continue

    return 'install'

def CheckPYPI(pkg):
    m = re.match(r'^([^=><]+)([<>=!]+)(.+)$', pkg)
    name, op, req = (m.group(1).strip(), m.group(2).strip(), m.group(3).strip()) if m else (pkg.strip(), None, None)

    try:
        package = distribution(name)
        installed = package.version

        if not op or not req:
            return 'skip'

        if op == '==':
            return 'skip' if installed == req else 'install'
        if op == '>=':
            return 'skip' if Compare(installed, req) >= 0 else 'install'
        if op == '>':
            return 'skip' if Compare(installed, req) > 0 else 'install'
        if op == '<=':
            return 'skip' if Compare(installed, req) <= 0 else 'install'
        if op == '<':
            return 'skip' if Compare(installed, req) < 0 else 'install'
        return 'install'

    except Exception:
        return 'install'

def Compare(v1, v2):
    v1_parts, v2_parts = list(map(int, re.findall(r'\d+', v1))), list(map(int, re.findall(r'\d+', v2)))

    for i in range(min(len(v1_parts), len(v2_parts))):
        if v1_parts[i] < v2_parts[i]: return -1
        if v1_parts[i] > v2_parts[i]: return 1

    return -1 if len(v1_parts) < len(v2_parts) else 1 if len(v1_parts) > len(v2_parts) else 0

def installing(fp):
    if fp.exists():
        with open(fp, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    action = CheckGit(line) if 'git+' in line else CheckPYPI(line)
                    if action == 'install':
                        print(f'Installing : {ORANGE}{line}{RESET}')
                        subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', line], check=True)

def Run(fp):
    if fp.exists(): subprocess.run([sys.executable, str(fp)], check=True)

for subdir, reqs, scripts in GetsAll('custom_nodes'):
    installing(reqs)
    Run(scripts)

os.system(f"pip install -r {Path.cwd() / 'requirements.txt'}")
