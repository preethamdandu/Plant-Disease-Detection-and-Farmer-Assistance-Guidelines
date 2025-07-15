#!/usr/bin/env python3
"""
Specialized script to install TensorFlow for disease detection feature
"""

import subprocess
import sys
import platform
import os

def get_system_info():
    """Get system information for proper TensorFlow installation"""
    system = platform.system()
    machine = platform.machine()
    python_version = sys.version_info
    
    print(f"🖥️ System: {system}")
    print(f"🔧 Architecture: {machine}")
    print(f"🐍 Python: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    return system, machine, python_version

def install_tensorflow(system, machine, python_version):
    """Install TensorFlow based on system configuration"""
    
    print("\n🤖 Installing TensorFlow for disease detection...")
    
    # Check if we're on Apple Silicon Mac
    if system == "Darwin" and machine == "arm64":
        print("🍎 Detected Apple Silicon Mac")
        print("Installing tensorflow-macos...")
        
        commands = [
            "pip install tensorflow-macos",
            "pip install tensorflow-metal"  # GPU support
        ]
        
    # Check if we're on Intel Mac
    elif system == "Darwin" and machine == "x86_64":
        print("🍎 Detected Intel Mac")
        print("Installing tensorflow...")
        
        commands = [
            "pip install tensorflow"
        ]
        
    # Linux or Windows
    else:
        print(f"💻 Installing TensorFlow for {system}")
        
        commands = [
            "pip install tensorflow"
        ]
    
    # Try installation commands
    for cmd in commands:
        print(f"📦 Running: {cmd}")
        try:
            result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
            print(f"✅ {cmd} completed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ {cmd} failed: {e.stderr}")
            continue
    
    return False

def test_tensorflow():
    """Test if TensorFlow is working properly"""
    print("\n🧪 Testing TensorFlow installation...")
    
    try:
        import tensorflow as tf
        print(f"✅ TensorFlow version: {tf.__version__}")
        
        # Test basic functionality
        import numpy as np
        x = np.array([[1, 2], [3, 4]])
        y = tf.constant(x)
        print("✅ TensorFlow basic operations working")
        
        # Test Keras
        from tensorflow import keras
        print("✅ Keras available")
        
        return True
    except ImportError as e:
        print(f"❌ TensorFlow import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ TensorFlow test failed: {e}")
        return False

def install_other_deps():
    """Install other required dependencies"""
    print("\n📦 Installing other dependencies...")
    
    deps = [
        "numpy>=1.21.0",
        "pandas>=1.5.0",
        "scikit-learn>=1.0.0",
        "Pillow>=8.0.0"
    ]
    
    for dep in deps:
        try:
            subprocess.run(f"pip install {dep}", shell=True, check=True, capture_output=True)
            print(f"✅ {dep} installed")
        except subprocess.CalledProcessError:
            print(f"⚠️ {dep} installation failed, continuing...")

def main():
    """Main installation function"""
    print("🚀 Installing TensorFlow for Disease Detection Feature")
    print("=" * 60)
    
    # Get system info
    system, machine, python_version = get_system_info()
    
    # Check Python version
    if python_version < (3, 7):
        print("❌ Python 3.7 or higher is required")
        return False
    
    # Install TensorFlow
    if not install_tensorflow(system, machine, python_version):
        print("\n❌ TensorFlow installation failed")
        print("\n🔧 Alternative solutions:")
        print("1. Try: pip install tensorflow==2.15.0")
        print("2. Try: pip install tensorflow-cpu")
        print("3. For Apple Silicon: pip install tensorflow-macos")
        print("4. Check your Python version and pip installation")
        return False
    
    # Install other dependencies
    install_other_deps()
    
    # Test TensorFlow
    if not test_tensorflow():
        print("\n❌ TensorFlow test failed")
        return False
    
    print("\n" + "=" * 60)
    print("✅ TensorFlow installed successfully!")
    print("🎉 Disease detection feature is now available!")
    print("\nTo run the application:")
    print("python manage.py runserver")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 