"""
Complete build and installer creation script for Scanify
This script:
1. Builds the application using PyInstaller (directory or single-file)
2. Creates installer using Inno Setup (if available)
3. Produces a clean program-style release folder and ZIP
"""
import os
import sys
import subprocess
import shutil

def print_step(message):
    print("\n" + "="*60)
    print(f"  {message}")
    print("="*60)

def check_pyinstaller():
    try:
        import PyInstaller
        return True
    except ImportError:
        return False

def build_exe():
    print_step("STEP 1: Building Application in Directory Mode (PyInstaller --onedir)")
    if not check_pyinstaller():
        print("ERROR: PyInstaller not found!\nInstall it with: pip install pyinstaller")
        return False
    import PyInstaller.__main__
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    args = [
        'scanify.py',
        '--name=Scanify',
        '--onedir',
        '--windowed',
        '--add-data=requirements.txt;.',
        '--add-data=README.md;.',
        '--add-data=version.json;.',
        '--add-data=icon.ico;.',
        '--hidden-import=PIL',
        '--hidden-import=PIL._tkinter_finder',
        '--hidden-import=customtkinter',
        '--hidden-import=tkinterdnd2',
        '--hidden-import=fitz',
        '--hidden-import=cv2',
        '--hidden-import=numpy',
        '--collect-all=customtkinter',
        '--collect-all=tkinterdnd2',
        '--noconfirm',
        '--clean',
    ]
    if os.path.exists('icon.ico'):
        args.append('--icon=icon.ico')
    if os.path.exists('version_info.txt'):
        args.append('--version-file=version_info.txt')
    try:
        PyInstaller.__main__.run(args)
        print("\n✓ Application built successfully in directory mode: dist/Scanify/")
        return True
    except Exception as e:
        print(f"\n✗ Build failed: {e}")
        return False

def check_inno_setup():
    inno_paths = [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
        r"C:\Program Files (x86)\Inno Setup 5\ISCC.exe",
        r"C:\Program Files\Inno Setup 5\ISCC.exe",
    ]
    for path in inno_paths:
        if os.path.exists(path):
            return path
    return None

def create_installer():
    print_step("STEP 2: Creating Installer with Inno Setup")
    inno_path = check_inno_setup()
    if not inno_path:
        print("WARNING: Inno Setup not found!\nTo create a professional installer:\n1. Download Inno Setup from: https://jrsoftware.org/isinfo.php\n2. Install it\n3. Run this script again\nFor now, you can distribute: dist/Scanify.exe")
        return False
    if not os.path.exists('installer.iss'):
        print("ERROR: installer.iss not found!")
        return False
    if not os.path.exists('dist/Scanify.exe'):
        print("ERROR: dist/Scanify.exe not found! Build the EXE first.")
        return False
    try:
        os.makedirs('installer_output', exist_ok=True)
        result = subprocess.run([
            inno_path, 'installer.iss'
        ], capture_output=True, text=True)
        if result.returncode == 0:
            print("\n✓ Installer created successfully!")
            installer_files = [f for f in os.listdir('installer_output') if f.endswith('.exe')]
            if installer_files:
                installer_path = os.path.join('installer_output', installer_files[0])
                print(f"\nInstaller location: {os.path.abspath(installer_path)}")
            return True
        else:
            print(f"\n✗ Installer creation failed!")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"\n✗ Error creating installer: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("  SCANIFY - COMPLETE BUILD & INSTALLER CREATOR")
    print("="*60)
    if not build_exe():
        print("\n✗ BUILD FAILED!")
        return 1
    installer_created = create_installer()
    print("\n" + "="*60)
    print("  BUILD SUMMARY")
    print("="*60)
    print("\n✓ Application: dist/Scanify.exe")
    if installer_created:
        print("✓ Windows Installer: installer_output/Scanify-Setup-v2.0.0.exe")
    else:
        print("✗ Windows Installer: Not created (Inno Setup not found)")
    print("\n" + "="*60)
    print("  DISTRIBUTION OPTIONS")
    print("="*60)
    print("\n1. Simple: Share 'dist/Scanify.exe' directly")
    if installer_created:
        print("2. Professional: Share the installer (.exe from installer_output)")
    else:
        print("3. To create installer: Install Inno Setup from https://jrsoftware.org/isinfo.php")
    print("\n" + "="*60)
    return 0

if __name__ == "__main__":
    sys.exit(main())


if __name__ == "__main__":
    sys.exit(main())
