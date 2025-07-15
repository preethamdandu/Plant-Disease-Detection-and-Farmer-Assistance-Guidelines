# 🌱 Plant Disease Detection and Farmer Assistance Platform

## Overview

This project is a full-stack web application designed to help farmers diagnose plant diseases, get weather and market information, and connect with agricultural volunteers for support. It leverages machine learning for image-based disease detection and provides a collaborative Q&A platform for the farming community.

---

## Features

- **AI-Powered Plant Disease Detection:**  
  Farmers can upload images of plant leaves to receive instant disease diagnosis using a deep learning model.

- **Weather Forecasting:**  
  Real-time and forecasted weather data for various regions.

- **Market Price Information:**  
  Up-to-date fruit and vegetable prices by city/district.

- **Q&A Platform:**  
  Farmers can post questions; volunteers can answer and assist based on location.

- **Real-Time Notifications:**  
  Users receive notifications for new questions, answers, and messages.

- **Resource Sharing:**  
  Volunteers can upload and share agricultural resources.

---

## Technologies Used

- **Backend:** Django (Python)
- **Frontend:** HTML5, CSS3, Bootstrap 4, JavaScript
- **Database:** SQLite (default, can be swapped for PostgreSQL)
- **Machine Learning:** TensorFlow, Keras (for disease detection)
- **Data Processing:** Pandas, NumPy
- **Web Scraping:** BeautifulSoup, Requests
- **Other:** Django Admin, RESTful APIs

---

## Requirements

- Python 3.8 or higher (recommended: 3.12)
- pip or conda for package management
- (Optional) [conda](https://docs.conda.io/) for environment management

**Python Packages:**  
All required packages are listed in `requirements.txt`.  
Install with:
```bash
pip install -r requirements.txt
```

---

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Plant-Disease-Detection-and-Farmer-Assistance-Guidelines
   ```

2. **Set up your Python environment:**
   - Using conda (recommended):
     ```bash
     conda create -n agroenv python=3.12
     conda activate agroenv
     ```
   - Or using venv:
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser (for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   - Open your browser and go to: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Directory Structure

```
Plant-Disease-Detection-and-Farmer-Assistance-Guidelines/
├── account/         # Django app (users, Q&A, notifications)
├── plant/           # Django project settings
├── templates/       # HTML templates
├── static/          # CSS, JS, images
├── media/           # Uploaded files
├── ml_models/       # ML model files (.h5, .txt)
├── data/            # CSVs and external data
├── docs/            # Documentation
├── requirements.txt # Python dependencies
├── manage.py        # Django management script
└── README.md
```

---

## Notes

- For production deployment, use a production-ready database and web server.
- Make sure to place the ML model files in the `ml_models/` directory.
- For any issues, check the documentation in the `docs/` folder or open an issue.

---

## License

This project is open-source and available under the MIT License.

---

**Happy farming! 🌾**
