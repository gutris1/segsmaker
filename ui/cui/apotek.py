import os, subprocess, sys, re
from pathlib import Path

def get_enabled_subdirectories_with_files(base_directory):
    subdirs_with_files = []
    base_path = Path(base_directory)
    
    for subdir in os.listdir(base_path):
        try:
            full_path = base_path / subdir
            if full_path.is_dir() and not subdir.endswith(".disabled") and not subdir.startswith('.') and subdir != '__pycache__':
                print(f"## Checking dependencies for '{subdir}'")
                requirements_file = full_path / "requirements.txt"
                install_script = full_path / "install.py"

                if requirements_file.exists() or install_script.exists():
                    subdirs_with_files.append((full_path, requirements_file, install_script))
        except Exception as e:
            print(f"EXCEPTION during dependencies check on '{subdir}':\n{e}")

    return subdirs_with_files

def check_package_installed(package_name, required_version):
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "show", package_name], capture_output=True, text=True, check=True)
        installed_version = None

        for line in result.stdout.splitlines():
            if line.startswith("Version:"):
                installed_version = line.split(":")[1].strip()

        if installed_version:
            if required_version.startswith(">="):
                if compare_versions(installed_version, required_version[2:]) >= 0:
                    return "skip"
                else:
                    return "install"
            elif required_version.startswith("=="):
                if installed_version == required_version[2:]:
                    return "skip"
                else:
                    return "install"
            elif required_version.startswith("<="):
                if compare_versions(installed_version, required_version[2:]) > 0:
                    return "uninstall"
                else:
                    return "skip"
        else:
            return "install"
    except subprocess.CalledProcessError:
        return "install"
    except FileNotFoundError:
        print("Error: 'pip' command not found. Make sure it's installed.")
        sys.exit(1)

def compare_versions(installed_version, required_version):
    installed_parts = list(map(int, re.findall(r'\d+', installed_version)))
    required_parts = list(map(int, re.findall(r'\d+', required_version)))

    for i in range(min(len(installed_parts), len(required_parts))):
        if installed_parts[i] < required_parts[i]:
            return -1
        elif installed_parts[i] > required_parts[i]:
            return 1

    return 0

def install_requirements(requirements_file_path):
    if requirements_file_path.exists():
        with open(requirements_file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    match = re.match(r'^([^=><]+)([<>=!]+)(.+)$', line)
                    if match:
                        package_name = match.group(1).strip()
                        comparison_operator = match.group(2).strip()
                        required_version = match.group(3).strip()

                        action = check_package_installed(package_name, required_version)

                        if action == "install":
                            print(f"## Installing '{package_name} {required_version}'")
                            subprocess.run([sys.executable, "-m", "pip", "install", "-q", f"{package_name}{comparison_operator}{required_version}"], check=True)
                        elif action == "uninstall":
                            print(f"## Uninstalling '{package_name}'")
                            subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", package_name], check=True)
                            print(f"## Re-installing '{package_name} {required_version}'")
                            subprocess.run([sys.executable, "-m", "pip", "install", "-q", f"{package_name}{comparison_operator}{required_version}"], check=True)
                        else:
                            print(f"## '{package_name}' is already up to date, skipping")
                    else:
                        package_name = line.strip()
                        action = check_package_installed(package_name, "")

                        if action == "install":
                            print(f"## Installing '{package_name}'")
                            subprocess.run([sys.executable, "-m", "pip", "install", "-q", package_name], check=True)
                        else:
                            print(f"## '{package_name}' is already installed, skipping")

def run_install_script(install_script_path):
    if install_script_path.exists():
        subprocess.run([sys.executable, str(install_script_path)], check=True)

custom_nodes_directory = "custom_nodes"
subdirs_with_files = get_enabled_subdirectories_with_files(custom_nodes_directory)

for subdir, requirements_file, install_script in subdirs_with_files:
    install_requirements(requirements_file)
    run_install_script(install_script)

print("## Finished checking and installing dependencies")
