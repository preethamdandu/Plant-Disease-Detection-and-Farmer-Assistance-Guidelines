#!/usr/bin/env python3
"""
Setup script for Plant Disease Detection Project
"""

import os
import sys
import subprocess

def run_command(command):
    """Run a command and return the result"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        return False
    print("✅ Python version is compatible")
    return True

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    success, output = run_command("pip install -r requirements.txt")
    if success:
        print("✅ Packages installed successfully")
        return True
    else:
        print(f"❌ Failed to install packages: {output}")
        return False

def setup_database():
    """Setup Django database"""
    print("🗄️ Setting up database...")
    success, output = run_command("python manage.py makemigrations")
    if not success:
        print(f"❌ Failed to make migrations: {output}")
        return False
    
    success, output = run_command("python manage.py migrate")
    if not success:
        print(f"❌ Failed to migrate database: {output}")
        return False
    
    print("✅ Database setup completed")
    return True

def check_model_files():
    """Check if model files exist"""
    model_files = ['ml_models/abc.h5', 'ml_models/pd1.txt']
    missing_files = []
    
    for file in model_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"⚠️ Warning: Missing model files: {missing_files}")
        print("   The disease detection feature may not work properly")
    else:
        print("✅ Model files found")
    
    return len(missing_files) == 0

def main():
    """Main setup function"""
    print("🚀 Setting up Plant Disease Detection Project...")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install requirements
    if not install_requirements():
        return False
    
    # Setup database
    if not setup_database():
        return False
    
    # Check model files
    check_model_files()
    
    print("=" * 50)
    print("✅ Setup completed successfully!")
    print("\nTo run the project:")
    print("1. python manage.py runserver")
    print("2. Open http://127.0.0.1:8000 in your browser")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 