#!/usr/bin/env python3
"""
Simple script to run the Plant Disease Detection Project
"""

import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Check if requirements are installed"""
    try:
        import django
        import tensorflow
        import numpy
        import pandas
        import sklearn
        import requests
        from bs4 import BeautifulSoup
        return True
    except ImportError as e:
        print(f"❌ Missing requirement: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_database():
    """Check if database is set up"""
    db_file = Path("db.sqlite3")
    if not db_file.exists():
        print("⚠️ Database not found. Running migrations...")
        subprocess.run([sys.executable, "manage.py", "makemigrations"], check=True)
        subprocess.run([sys.executable, "manage.py", "migrate"], check=True)
        print("✅ Database setup completed")

def main():
    """Main function to run the application"""
    print("🚀 Starting Plant Disease Detection Project...")
    
    # Check requirements
    if not check_requirements():
        return False
    
    # Check database
    check_database()
    
    print("🌐 Starting Django development server...")
    print("📱 Open your browser and go to: http://127.0.0.1:8000")
    print("⏹️ Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, "manage.py", "runserver"])
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 