#!/usr/bin/env python3
"""
Test script to verify the Plant Disease Detection Project setup
"""

import os
import sys
import django
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import django
        print("✅ Django imported successfully")
    except ImportError as e:
        print(f"❌ Django import failed: {e}")
        return False
    
    try:
        import tensorflow as tf
        print("✅ TensorFlow imported successfully")
    except ImportError as e:
        print(f"❌ TensorFlow import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ NumPy imported successfully")
    except ImportError as e:
        print(f"❌ NumPy import failed: {e}")
        return False
    
    try:
        import pandas as pd
        print("✅ Pandas imported successfully")
    except ImportError as e:
        print(f"❌ Pandas import failed: {e}")
        return False
    
    try:
        import sklearn
        print("✅ Scikit-learn imported successfully")
    except ImportError as e:
        print(f"❌ Scikit-learn import failed: {e}")
        return False
    
    try:
        import requests
        print("✅ Requests imported successfully")
    except ImportError as e:
        print(f"❌ Requests import failed: {e}")
        return False
    
    try:
        from bs4 import BeautifulSoup
        print("✅ BeautifulSoup imported successfully")
    except ImportError as e:
        print(f"❌ BeautifulSoup import failed: {e}")
        return False
    
    return True

def test_django_setup():
    """Test Django configuration"""
    print("\n🔍 Testing Django setup...")
    
    try:
        # Add the project directory to Python path
        project_dir = Path(__file__).resolve().parent
        sys.path.insert(0, str(project_dir))
        
        # Set Django settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plant.settings')
        django.setup()
        
        print("✅ Django setup successful")
        return True
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        return False

def test_model_files():
    """Test if model files exist"""
    print("\n🔍 Testing model files...")
    
    model_files = [
        'ml_models/abc.h5',
        'ml_models/pd1.txt'
    ]
    
    all_exist = True
    for file in model_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
            all_exist = False
    
    return all_exist

def test_database():
    """Test database connection"""
    print("\n🔍 Testing database...")
    
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_static_files():
    """Test if static files exist"""
    print("\n🔍 Testing static files...")
    
    static_files = [
        'static/styles.css',
        'static/img/farmer.svg',
        'static/img/volunteer.svg',
        'static/img/leaf.svg'
    ]
    
    all_exist = True
    for file in static_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
            all_exist = False
    
    return all_exist

def test_templates():
    """Test if templates exist"""
    print("\n🔍 Testing templates...")
    
    template_files = [
        'templates/index.html',
        'templates/farmer_login.html',
        'templates/volunteer_login.html',
        'templates/disease_upload.html'
    ]
    
    all_exist = True
    for file in template_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
            all_exist = False
    
    return all_exist

def main():
    """Run all tests"""
    print("🧪 Testing Plant Disease Detection Project Setup")
    print("=" * 50)
    
    tests = [
        ("Import Tests", test_imports),
        ("Django Setup", test_django_setup),
        ("Model Files", test_model_files),
        ("Database", test_database),
        ("Static Files", test_static_files),
        ("Templates", test_templates)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The project is ready to run.")
        print("\nTo start the server:")
        print("python manage.py runserver")
    else:
        print("⚠️ Some tests failed. Please check the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 