# TensorFlow Setup Guide for Disease Detection

## 🎯 Goal: Enable Disease Detection Feature

The disease detection feature requires TensorFlow to be properly installed. Follow this guide based on your system.

## 🖥️ System-Specific Installation

### For Apple Silicon Mac (M1/M2/M3)
```bash
# Install TensorFlow for Apple Silicon
pip install tensorflow-macos

# Optional: Install GPU support
pip install tensorflow-metal
```

### For Intel Mac
```bash
# Install standard TensorFlow
pip install tensorflow
```

### For Windows/Linux
```bash
# Install TensorFlow
pip install tensorflow

# If you have GPU and want GPU support
pip install tensorflow[gpu]
```

## 🚀 Quick Installation Script

Run the automated installation script:
```bash
python install_tensorflow.py
```

## 🔧 Manual Installation Steps

### Step 1: Check Your System
```bash
python -c "import platform; print(f'System: {platform.system()}'); print(f'Architecture: {platform.machine()}')"
```

### Step 2: Update pip
```bash
pip install --upgrade pip
```

### Step 3: Install TensorFlow

**For Apple Silicon Mac:**
```bash
pip install tensorflow-macos
pip install tensorflow-metal
```

**For Intel Mac/Windows/Linux:**
```bash
pip install tensorflow
```

### Step 4: Test Installation
```bash
python -c "import tensorflow as tf; print(f'TensorFlow version: {tf.__version__}')"
```

### Step 5: Install Other Dependencies
```bash
pip install numpy pandas scikit-learn Pillow
```

### Step 6: Setup Django
```bash
python manage.py makemigrations
python manage.py migrate
```

## 🧪 Test Disease Detection

After installation, test the disease detection:

1. **Start the server:**
   ```bash
   python manage.py runserver
   ```

2. **Access the application:**
   - Go to: http://127.0.0.1:8000
   - Register as a farmer
   - Go to disease upload page
   - Upload a plant image

## 🔍 Troubleshooting

### If TensorFlow Installation Fails

**Error: "No matching distribution found"**
```bash
# Try specific version
pip install tensorflow==2.15.0

# Or try CPU-only version
pip install tensorflow-cpu
```

**Error: "Permission denied"**
```bash
# Use user installation
pip install --user tensorflow

# Or use virtual environment
python -m venv venv
source venv/bin/activate  # On Mac/Linux
# venv\Scripts\activate  # On Windows
pip install tensorflow
```

**Error: "SSL certificate"**
```bash
# Trust certificates
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org tensorflow
```

### For Apple Silicon Mac Issues

**If tensorflow-macos fails:**
```bash
# Try conda installation
conda install tensorflow-deps
pip install tensorflow-macos
pip install tensorflow-metal
```

**Alternative approach:**
```bash
# Install via conda
conda install tensorflow
```

### For Memory Issues

**If you get memory errors:**
```bash
# Install CPU-only version
pip install tensorflow-cpu

# Or limit TensorFlow memory usage
export TF_FORCE_GPU_ALLOW_GROWTH=true
```

## ✅ Verification

After installation, verify everything works:

```bash
python -c "
import tensorflow as tf
import numpy as np
from tensorflow import keras
print('✅ TensorFlow:', tf.__version__)
print('✅ Keras available')
print('✅ NumPy:', np.__version__)
"
```

## 🎯 Expected Results

When disease detection is working:

1. **Model loads without errors** in console
2. **Upload page** accepts image files
3. **Prediction results** show disease name and treatment
4. **No import errors** in Django console

## 🆘 Still Having Issues?

### Check Python Version
```bash
python --version
# Should be 3.7 or higher
```

### Check pip Version
```bash
pip --version
```

### Try Virtual Environment
```bash
# Create virtual environment
python -m venv plant_disease_env

# Activate it
source plant_disease_env/bin/activate  # Mac/Linux
# plant_disease_env\Scripts\activate  # Windows

# Install in clean environment
pip install tensorflow
pip install Django numpy pandas scikit-learn Pillow
```

### Alternative: Use Conda
```bash
# Install Miniconda first, then:
conda create -n plant_disease python=3.9
conda activate plant_disease
conda install tensorflow
pip install Django
```

## 📞 Get Help

If you're still having issues:

1. **Check the error messages carefully**
2. **Try the system-specific commands above**
3. **Use the virtual environment approach**
4. **Consider using conda instead of pip**

The disease detection feature will work once TensorFlow is properly installed! 