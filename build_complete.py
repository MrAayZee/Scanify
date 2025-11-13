"""
Complete build and installer creation script for PDF2Scan
This script:
1. Builds the .exe using PyInstaller
2. Creates installer using Inno Setup (if available)
"""
import os
import sys
import subprocess
import shutil

def print_step(message):
    """Print a formatted step message."""
    print("\n" + "="*60)
    print(f"  {message}")
    print("="*60)

def check_pyinstaller():
    """Check if PyInstaller is installed."""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False

def check_inno_setup():
    """Check if Inno Setup is installed."""
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

def build_exe():
    """Build the .exe using PyInstaller."""
    print_step("STEP 1: Building EXE with PyInstaller")

    if not check_pyinstaller():
        print("ERROR: PyInstaller not found!")
        print("Install it with: pip install pyinstaller")
        return False

    import PyInstaller.__main__

    # Clean previous builds
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')

    # Build arguments
    args = [
        'pdf2scan.py',
        '--name=PDF2Scan',
        '--onefile',
        '--windowed',
        '--add-data=requirements.txt;.',
        '--add-data=README.md;.',
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

    # Add icon if exists
    if os.path.exists('icon.ico'):
        args.append('--icon=icon.ico')

    # Add version info if exists
    if os.path.exists('version_info.txt'):
        args.append('--version-file=version_info.txt')

    try:
        PyInstaller.__main__.run(args)
        print("\n✓ EXE built successfully: dist/PDF2Scan.exe")
        return True
    except Exception as e:
        print(f"\n✗ Build failed: {e}")
        return False

def create_installer():
    """Create installer using Inno Setup."""
    print_step("STEP 2: Creating Installer with Inno Setup")

    inno_path = check_inno_setup()

    if not inno_path:
        print("WARNING: Inno Setup not found!")
        print("\nTo create a professional installer:")
        print("1. Download Inno Setup from: https://jrsoftware.org/isinfo.php")
        print("2. Install it")
        print("3. Run this script again")
        print("\nFor now, you can distribute: dist/PDF2Scan.exe")
        return False

    if not os.path.exists('installer.iss'):
        print("ERROR: installer.iss not found!")
        return False

    if not os.path.exists('dist/PDF2Scan.exe'):
        print("ERROR: dist/PDF2Scan.exe not found! Build the EXE first.")
        return False

    try:
        # Create output directory
        os.makedirs('installer_output', exist_ok=True)

        # Run Inno Setup compiler
        result = subprocess.run(
            [inno_path, 'installer.iss'],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("\n✓ Installer created successfully!")

            # Find the created installer
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

def create_portable_zip():
    """Create a portable ZIP package."""
    print_step("STEP 3: Creating Portable ZIP Package")

    if not os.path.exists('dist/PDF2Scan.exe'):
        print("ERROR: dist/PDF2Scan.exe not found!")
        return False

    try:
        # Create release folder
        release_dir = 'release_package'
        if os.path.exists(release_dir):
            shutil.rmtree(release_dir)
        os.makedirs(release_dir)

        # Copy files
        shutil.copy('dist/PDF2Scan.exe', release_dir)
        if os.path.exists('README.md'):
            shutil.copy('README.md', release_dir)
        if os.path.exists('LICENSE'):
            shutil.copy('LICENSE', release_dir)
        if os.path.exists('INSTALL.md'):
            shutil.copy('INSTALL.md', release_dir)

        # Create ZIP
        zip_name = 'PDF2Scan-v1.0.0-Windows-Portable'
        shutil.make_archive(zip_name, 'zip', release_dir)

        print(f"\n✓ Portable package created: {zip_name}.zip")
        return True

    except Exception as e:
        print(f"\n✗ Error creating portable package: {e}")
        return False

def main():
    """Main build process."""
    print("\n" + "="*60)
    print("  PDF2SCAN - COMPLETE BUILD & INSTALLER CREATOR")
    print("="*60)

    # Step 1: Build EXE
    if not build_exe():
        print("\n✗ BUILD FAILED!")
        return 1

    # Step 2: Create Installer
    installer_created = create_installer()

    # Step 3: Create Portable ZIP
    zip_created = create_portable_zip()

    # Summary
    print("\n" + "="*60)
    print("  BUILD SUMMARY")
    print("="*60)
    print("\n✓ Standalone EXE: dist/PDF2Scan.exe")

    if installer_created:
        print("✓ Windows Installer: installer_output/PDF2Scan-Setup-v1.0.0.exe")
    else:
        print("✗ Windows Installer: Not created (Inno Setup not found)")

    if zip_created:
        print("✓ Portable Package: PDF2Scan-v1.0.0-Windows-Portable.zip")

    print("\n" + "="*60)
    print("  DISTRIBUTION OPTIONS")
    print("="*60)
    print("\n1. Simple: Share 'dist/PDF2Scan.exe' directly")
    print("2. Portable: Share the ZIP package")

    if installer_created:
        print("3. Professional: Share the installer (.exe from installer_output)")
    else:
        print("3. To create installer: Install Inno Setup from https://jrsoftware.org/isinfo.php")

    print("\n" + "="*60)

    return 0

if __name__ == "__main__":
    sys.exit(main())
