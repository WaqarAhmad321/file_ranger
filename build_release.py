import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path

def run_command(command, cwd=None):
    print(f"Running: {command}")
    try:
        subprocess.check_call(command, shell=True, cwd=cwd)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        sys.exit(1)

def build_backend():
    print("Building C++ Backend...")
    build_dir = Path("bindings/build")
    build_dir.mkdir(parents=True, exist_ok=True)
    
    run_command("cmake ..", cwd=str(build_dir))
    run_command("cmake --build . --config Release", cwd=str(build_dir))
    
    ext = ".pyd" if platform.system() == "Windows" else ".so"
    # Search recursively in build dir because sometimes it's in subfolders (like Release/ or Debug/)
    found_files = list(build_dir.rglob(f"*{ext}"))
   
    target_files = [f for f in found_files if "backend" in f.name and "cmake" not in f.name]
    
    if not target_files:
        print(f"Could not find compiled {ext} file in {build_dir}")
        sys.exit(1)
        
    source_file = target_files[0]
    dest_file = Path("ui") / source_file.name
    
    print(f"📦 Copying {source_file.name} to ui/ directory...")
    shutil.copy2(source_file, dest_file)
    return dest_file.name

def build_executable(backend_filename):
    print("Packaging with PyInstaller...")
    
    # Separator for --add-binary depends on OS
    sep = ";" if platform.system() == "Windows" else ":"
    
    # We add the backend shared object to the root of the bundle (.)
    add_binary = f"ui/{backend_filename}{sep}."
    
    cmd = [
        "pyinstaller",
        "--name", "file_ranger",
        "--onefile",
        "--clean",
        "--add-binary", f'"{add_binary}"',
        "--hidden-import", "backend",
        "ui/app.py"
    ]
    
    full_cmd = " ".join(cmd)
    run_command(full_cmd)
    
    print("\n✅ Build Complete!")
    dist_path = Path("dist") / ("file_ranger.exe" if platform.system() == "Windows" else "file_ranger")
    print(f"Executable is located at: {dist_path.absolute()}")

if __name__ == "__main__":
    # Ensure we are in project root
    if not os.path.exists("ui/app.py"):
        print("Please run this script from the project root directory.")
        sys.exit(1)
        
    # Check for PyInstaller
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        run_command(f"{sys.executable} -m pip install pyinstaller")

    backend_file = build_backend()
    build_executable(backend_file)
