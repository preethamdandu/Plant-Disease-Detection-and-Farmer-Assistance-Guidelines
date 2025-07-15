#!/usr/bin/env python3
"""
Simple installation script for Plant Disease Detection Project
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

def main():
    """Main installation function"""
    print("🚀 Installing Plant Disease Detection Project...")
    print("=" * 50)
    
    # Step 1: Install Django first
    if not run_command("pip install Django>=3.2.0", "Installing Django"):
        return False
    
    # Step 2: Install basic dependencies
    basic_deps = [
        "numpy>=1.21.0",
        "pandas>=1.5.0", 
        "requests>=2.25.0",
        "beautifulsoup4>=4.9.0",
        "Pillow>=8.0.0",
        "python-dateutil>=2.8.0"
    ]
    
    for dep in basic_deps:
        if not run_command(f"pip install {dep}", f"Installing {dep}"):
            print(f"⚠️ Warning: Failed to install {dep}, continuing...")
    
    # Step 3: Install scikit-learn
    if not run_command("pip install scikit-learn>=1.0.0", "Installing scikit-learn"):
        print("⚠️ Warning: scikit-learn installation failed, continuing...")
    
    # Step 4: Install TensorFlow (this might take a while)
    print("🤖 Installing TensorFlow (this may take a few minutes)...")
    if not run_command("pip install tensorflow>=2.15.0", "Installing TensorFlow"):
        print("⚠️ Warning: TensorFlow installation failed")
        print("   The disease detection feature may not work")
        print("   You can try installing it manually later")
    
    # Step 5: Setup Django
    print("\n🗄️ Setting up Django...")
    if not run_command("python manage.py makemigrations", "Creating migrations"):
        return False
    
    if not run_command("python manage.py migrate", "Running migrations"):
        return False
    
    print("\n" + "=" * 50)
    print("✅ Installation completed!")
    print("\nTo run the project:")
    print("python manage.py runserver")
    print("\nOr use the run script:")
    print("python run.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 