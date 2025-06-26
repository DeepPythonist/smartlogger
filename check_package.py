#!/usr/bin/env python3

import sys
import subprocess
import os
from pathlib import Path

def run_command(cmd, description):
    print(f"🔍 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        print(f"✅ {description} passed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def check_files_exist():
    required_files = [
        'smartlogger/__init__.py',
        'smartlogger/auto.py',
        'setup.py',
        'pyproject.toml',
        'README.md',
        'LICENSE',
        'CHANGELOG.md'
    ]
    
    print("📁 Checking required files...")
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ All required files present")
        return True

def main():
    print("🧪 SmartLogger Package Validation")
    print("=================================")
    
    checks = [
        (check_files_exist, "File existence check"),
        (lambda: run_command("python -m pytest tests/ -v", "Running tests"), "Unit tests"),
        (lambda: run_command("python -c 'import smartlogger.auto; print(\"Import successful\")'", "Testing import"), "Import test"),
        (lambda: run_command("python demo_smartlogger.py", "Running demo"), "Demo execution"),
        (lambda: run_command("python -m build", "Building package"), "Package build"),
        (lambda: run_command("python -m twine check dist/*", "Checking package"), "Package validation"),
    ]
    
    all_passed = True
    
    for check_func, description in checks:
        if not check_func():
            all_passed = False
            print()
    
    print("\n" + "="*50)
    if all_passed:
        print("🎉 All checks passed! Package is ready for upload.")
        print("\nNext steps:")
        print("1. Test upload: ./upload_to_pypi.sh test")
        print("2. Production upload: ./upload_to_pypi.sh prod")
    else:
        print("❌ Some checks failed. Please fix the issues before uploading.")
        sys.exit(1)

if __name__ == "__main__":
    main() 