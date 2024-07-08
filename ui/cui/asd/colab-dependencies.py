import os, subprocess, sys
from pathlib import Path

def get_enabled_subdirectories_with_files(base_directory):
    subdirs_with_files = []
    base_path = Path(base_directory)
    
    for subdir in os.listdir(base_path):
        try:
            full_path = base_path / subdir
            if full_path.is_dir() and not subdir.endswith(".disabled") and not subdir.startswith('.') and subdir != '__pycache__':
                print(f"## Install dependencies for '{subdir}'")
                requirements_file = full_path / "requirements.txt"
                install_script = full_path / "install.py"

                if requirements_file.exists() or install_script.exists():
                    subdirs_with_files.append((full_path, requirements_file, install_script))
        except Exception as e:
            print(f"EXCEPTION During Dependencies INSTALL on '{subdir}':\n{e}")

    return subdirs_with_files

def install_requirements(requirements_file_path):
    if requirements_file_path.exists():
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements_file_path)])

def run_install_script(install_script_path):
    if install_script_path.exists():
        subprocess.run([sys.executable, str(install_script_path)])

custom_nodes_directory = "custom_nodes"
subdirs_with_files = get_enabled_subdirectories_with_files(custom_nodes_directory)

for subdir, requirements_file, install_script in subdirs_with_files:
    install_requirements(requirements_file)
    run_install_script(install_script)
