# Installation Guide

## Quick Start (Recommended)

### Option 1: Minimal Installation (Basic Features)
```bash
# Install basic dependencies
pip install -r requirements_minimal.txt

# Setup database
python manage.py makemigrations
python manage.py migrate

# Run the application
python manage.py runserver
```

### Option 2: Full Installation (All Features)
```bash
# Use the installation script
python install.py

# Or install manually
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Troubleshooting

### If TensorFlow Installation Fails

1. **Try installing TensorFlow separately:**
   ```bash
   pip install tensorflow
   ```

2. **For Apple Silicon Macs:**
   ```bash
   pip install tensorflow-macos
   ```

3. **For older Python versions:**
   ```bash
   pip install tensorflow==2.15.0
   ```

### If Other Dependencies Fail

1. **Update pip:**
   ```bash
   pip install --upgrade pip
   ```

2. **Install dependencies one by one:**
   ```bash
   pip install Django
   pip install numpy
   pip install pandas
   pip install requests
   pip install beautifulsoup4
   pip install Pillow
   pip install python-dateutil
   ```

### If Database Setup Fails

1. **Check if SQLite is available:**
   ```bash
   python -c "import sqlite3; print('SQLite available')"
   ```

2. **Reset database:**
   ```bash
   rm db.sqlite3
   python manage.py makemigrations
   python manage.py migrate
   ```

## Features Available

### With Minimal Installation:
- ✅ User registration and login
- ✅ Q&A platform
- ✅ Weather data display (if CSV files exist)
- ✅ Market price system
- ❌ Disease detection (requires TensorFlow)

### With Full Installation:
- ✅ All features including disease detection

## Access the Application

After successful installation, open your browser and go to:
**http://127.0.0.1:8000**

## System Requirements

- Python 3.7 or higher
- pip (Python package installer)
- Internet connection (for initial package downloads)

## Supported Operating Systems

- ✅ macOS (Intel and Apple Silicon)
- ✅ Linux
- ✅ Windows

## Need Help?

If you encounter any issues:

1. Check the error messages carefully
2. Try the minimal installation first
3. Install TensorFlow separately if needed
4. Make sure you have Python 3.7+ installed

The application will work with basic features even without TensorFlow installed. 