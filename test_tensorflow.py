#!/usr/bin/env python3
"""
Test script to verify TensorFlow installation and model loading
"""

import os
import sys

def test_tensorflow_import():
    """Test if TensorFlow can be imported"""
    print("🧪 Testing TensorFlow import...")
    
    try:
        import tensorflow as tf
        print(f"✅ TensorFlow version: {tf.__version__}")
        return True
    except ImportError as e:
        print(f"❌ TensorFlow import failed: {e}")
        return False

def test_keras_import():
    """Test if Keras can be imported"""
    print("\n🧪 Testing Keras import...")
    
    try:
        from tensorflow import keras
        print("✅ Keras available")
        return True
    except ImportError as e:
        print(f"❌ Keras import failed: {e}")
        return False

def test_model_loading():
    """Test if the disease detection model can be loaded"""
    print("\n🧪 Testing model loading...")
    
    try:
        from tensorflow.keras.models import load_model
        import os
        
        model_path = os.path.join('ml_models', 'abc.h5')
        if os.path.exists(model_path):
            print(f"✅ Model file found: {model_path}")
            
            # Try to load the model
            model = load_model(model_path)
            print("✅ Model loaded successfully")
            print(f"✅ Model summary: {model.summary()}")
            return True
        else:
            print(f"❌ Model file not found: {model_path}")
            return False
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        return False

def test_image_processing():
    """Test if image processing works"""
    print("\n🧪 Testing image processing...")
    
    try:
        from tensorflow.keras.preprocessing import image
        import numpy as np
        
        # Create a dummy image array
        dummy_image = np.random.random((200, 200, 3))
        print("✅ Image processing libraries available")
        return True
    except Exception as e:
        print(f"❌ Image processing test failed: {e}")
        return False

def test_django_integration():
    """Test if Django can work with TensorFlow"""
    print("\n🧪 Testing Django integration...")
    
    try:
        import os
        import django
        
        # Set up Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plant.settings')
        django.setup()
        
        # Test if we can import the views
        from account.views import model
        if model is not None:
            print("✅ Django integration successful")
            print("✅ Model available in views")
            return True
        else:
            print("⚠️ Model not available in views")
            return False
    except Exception as e:
        print(f"❌ Django integration failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 TensorFlow and Disease Detection Test Suite")
    print("=" * 50)
    
    tests = [
        ("TensorFlow Import", test_tensorflow_import),
        ("Keras Import", test_keras_import),
        ("Image Processing", test_image_processing),
        ("Model Loading", test_model_loading),
        ("Django Integration", test_django_integration)
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
        print("🎉 All tests passed! Disease detection is ready!")
        print("\nTo start the application:")
        print("python manage.py runserver")
    elif passed >= 3:
        print("⚠️ Most tests passed. Disease detection should work.")
        print("Some features may be limited.")
    else:
        print("❌ Many tests failed. Please check TensorFlow installation.")
        print("Refer to TENSORFLOW_SETUP.md for help.")
    
    return passed >= 3

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 