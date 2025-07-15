#!/usr/bin/env python3
"""
Conda-based TensorFlow installation for Apple Silicon Mac with Python 3.13
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and return success status"""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def create_conda_environment():
    """Create a conda environment with compatible Python version"""
    print("🔧 Creating conda environment with Python 3.11...")
    
    # Create environment with Python 3.11 (compatible with TensorFlow)
    if not run_command("conda create -n plant_disease python=3.11 -y", "Creating conda environment"):
        return False
    
    print("✅ Conda environment created successfully")
    print("\n📝 To activate the environment, run:")
    print("conda activate plant_disease")
    print("\n📝 Then install TensorFlow:")
    print("pip install tensorflow")
    
    return True

def install_tensorflow_conda():
    """Install TensorFlow using conda"""
    print("🤖 Installing TensorFlow via conda...")
    
    commands = [
        "conda install tensorflow -c conda-forge -y",
        "conda install numpy pandas scikit-learn pillow -c conda-forge -y"
    ]
    
    for cmd in commands:
        if not run_command(cmd, f"Running {cmd}"):
            print(f"⚠️ Warning: {cmd} failed, trying alternative...")
            continue
    
    return True

def install_django_conda():
    """Install Django and other dependencies"""
    print("🌐 Installing Django and web dependencies...")
    
    commands = [
        "pip install Django>=3.2.0",
        "pip install requests beautifulsoup4 python-dateutil"
    ]
    
    for cmd in commands:
        if not run_command(cmd, f"Running {cmd}"):
            print(f"⚠️ Warning: {cmd} failed")
    
    return True

def test_tensorflow_conda():
    """Test TensorFlow installation"""
    print("🧪 Testing TensorFlow installation...")
    
    test_script = """
import tensorflow as tf
import numpy as np
from tensorflow import keras
print(f"✅ TensorFlow version: {tf.__version__}")
print("✅ Keras available")
print("✅ NumPy available")
"""
    
    try:
        result = subprocess.run([sys.executable, "-c", test_script], 
                              capture_output=True, text=True, check=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ TensorFlow test failed: {e.stderr}")
        return False

def main():
    """Main installation function"""
    print("🚀 Installing TensorFlow for Apple Silicon Mac (Python 3.13)")
    print("=" * 60)
    print("⚠️ Note: Python 3.13 is too new for TensorFlow")
    print("🔧 Solution: Using conda with Python 3.11")
    print("=" * 60)
    
    print("\n📋 Available options:")
    print("1. Create conda environment with Python 3.11 (Recommended)")
    print("2. Try alternative TensorFlow installation")
    print("3. Use minimal installation without TensorFlow")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        if create_conda_environment():
            print("\n✅ Conda environment created!")
            print("\n📝 Next steps:")
            print("1. conda activate plant_disease")
            print("2. pip install tensorflow")
            print("3. pip install Django numpy pandas scikit-learn")
            print("4. python manage.py runserver")
        else:
            print("❌ Failed to create conda environment")
    
    elif choice == "2":
        print("\n🔄 Trying alternative TensorFlow installation...")
        if install_tensorflow_conda():
            if install_django_conda():
                if test_tensorflow_conda():
                    print("\n✅ TensorFlow installed successfully!")
                else:
                    print("\n❌ TensorFlow test failed")
            else:
                print("\n❌ Django installation failed")
        else:
            print("\n❌ TensorFlow installation failed")
    
    elif choice == "3":
        print("\n📦 Installing minimal dependencies...")
        if install_django_conda():
            print("\n✅ Minimal installation completed!")
            print("⚠️ Disease detection will be disabled")
        else:
            print("\n❌ Minimal installation failed")
    
    else:
        print("❌ Invalid choice")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 