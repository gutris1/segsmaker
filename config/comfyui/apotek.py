from pathlib import Path
import pkg_resources
import subprocess
import importlib
import sys
import re
import os

MAGENTA = '\033[35m'
RED = '\033[31m'
CYAN = '\033[36m'
GREEN = '\033[38;5;35m'
YELLOW = '\033[33m'
BLUE = '\033[38;5;69m'
PURPLE = '\033[38;5;135m'
ORANGE = '\033[38;5;208m'
RESET = '\033[0m'

def GetsAll(base):
    subdirs_with_files = []
    base_path = Path(base)

    for subdir in os.listdir(base_path):
        try:
            full_path = base_path / subdir
            if full_path.is_dir() and not subdir.endswith(".disabled") and not subdir.startswith('.') and subdir != '__pycache__':
                print(f"Checking dependencies for >> {CYAN}{subdir}{RESET}")
                requirements_file = full_path / "requirements.txt"
                install_script = full_path / "install.py"

                if requirements_file.exists() or install_script.exists():
                    subdirs_with_files.append((full_path, requirements_file, install_script))
        except Exception as e:
            print(f"EXCEPTION during dependencies check on {RED}{subdir}{RESET}:\n{e}")

    return subdirs_with_files

def Get_git_pkg_name(git_url):
    if git_url.startswith("git+"):
        git_url = git_url[4:]

    if "github.com" in git_url:
        match = re.search(r'github\.com/[^/]+/([^/.]+)', git_url)
        if match:
            return match.group(1)

    match = re.search(r'/([^/]+)\.git', git_url)
    if match:
        return match.group(1)

    parts = git_url.rstrip('/').split('/')
    if parts:
        return parts[-1]

    return None

def CheckGit(package_spec):
    package_name = Get_git_pkg_name(package_spec)
    if not package_name:
        return "install"

    package_variations = [
        package_name,
        package_name.lower(),
        package_name.replace('-', '_'),
        package_name.lower().replace('-', '_')
    ]

    for variant in package_variations:
        try:
            importlib.import_module(variant)
            return "skip"
        except ImportError:
            continue

    return "install"

def CheckPYPI(package_spec):
    match = re.match(r'^([^=><]+)([<>=!]+)(.+)$', package_spec)
    if match:
        package_name = match.group(1).strip()
        comparison_operator = match.group(2).strip()
        required_version = match.group(3).strip()
    else:
        package_name = package_spec.strip()
        comparison_operator = None
        required_version = None

    try:
        package = pkg_resources.get_distribution(package_name)
        installed_version = package.version

        if not comparison_operator or not required_version:
            return "skip"

        if comparison_operator == "==":
            if installed_version == required_version:
                return "skip"
            else:
                return "install"
        elif comparison_operator == ">=":
            if Compare(installed_version, required_version) >= 0:
                return "skip"
            else:
                return "install"
        elif comparison_operator == ">":
            if Compare(installed_version, required_version) > 0:
                return "skip"
            else:
                return "install"
        elif comparison_operator == "<=":
            if Compare(installed_version, required_version) <= 0:
                return "skip"
            else:
                return "install"
        elif comparison_operator == "<":
            if Compare(installed_version, required_version) < 0:
                return "skip"
            else:
                return "install"
        else:
            return "install"

    except pkg_resources.DistributionNotFound:
        return "install"
    except Exception as e:
        return "install"

def Compare(v1, v2):
    v1_parts = list(map(int, re.findall(r'\d+', v1)))
    v2_parts = list(map(int, re.findall(r'\d+', v2)))

    for i in range(min(len(v1_parts), len(v2_parts))):
        if v1_parts[i] < v2_parts[i]:
            return -1
        elif v1_parts[i] > v2_parts[i]:
            return 1

    if len(v1_parts) < len(v2_parts):
        return -1
    elif len(v1_parts) > len(v2_parts):
        return 1
    else:
        return 0

def installing(fp):
    if fp.exists():
        with open(fp, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                if "git+" in line:
                    action = CheckGit(line)
                else:
                    action = CheckPYPI(line)

                if action == "install":
                    print(f"Installing package: {ORANGE}{line}{RESET}")
                    subprocess.run([sys.executable, "-m", "pip", "install", "-q", line], check=True)
                else:
                    pass

def Run(fp):
    if fp.exists(): subprocess.run([sys.executable, str(fp)], check=True)

custom_nodes_directory = "custom_nodes"
subdirs_with_files = GetsAll(custom_nodes_directory)

for subdir, requirements_file, install_script in subdirs_with_files:
    installing(requirements_file)
    Run(install_script)
