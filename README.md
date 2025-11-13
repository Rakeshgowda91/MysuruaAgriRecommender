

# **Crop Recommendation System – Mysuru Region (ML + Django)**

This project is a machine learning–based Crop Recommendation System designed for farmers and students in the Mysuru region.
The system analyzes soil nutrients, environmental conditions, and regional factors to suggest the most suitable crop for cultivation.

It integrates a trained Random Forest model with a Django web application, providing an easy-to-use interface for predictions.

---

## **Features**

* Predicts the best crop based on:

  * Nitrogen, Phosphorus, Potassium (NPK)
  * Soil pH
  * Rainfall
  * Temperature
  * Humidity
  * Soil type
* Region-specific model trained on Mysuru agricultural data
* Django-based user interface
* Encoded soil and crop labels for accurate model processing
* Scalable structure supporting future additions like dashboards and articles

---

## **How It Works**

1. Load and preprocess the Mysuru agriculture dataset
2. Add temperature, humidity, and soil type fields
3. Encode categorical values such as soil type and crop labels
4. Train a Random Forest Classifier
5. Save the trained model and encoders
6. Django application takes user input, processes it, and returns the predicted crop

---

## **Project Structure**

```
/project
│── backend
│   ├── crop_model.pkl
│   ├── soil_encoder.pkl
│   ├── crop_encoder.pkl
│   ├── train_model.py
│   ├── ml_model.py
│
│── agri_site (Django project)
│   ├── manage.py
│   ├── db.sqlite3
│   └── crop_app/
│
│── templates/
│── static/
│── README.md
```

---

## **Tech Stack**

**Machine Learning**

* Python
* scikit-learn
* Random Forest Classifier
* Pandas, NumPy
* Joblib

**Web Framework**

* Django
* SQLite

---

## **How to Run**

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Train the model (optional)

```bash
python train_model.py
```

### 3. Start the Django server

```bash
python manage.py runserver
```

Open a browser and navigate to:
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## **Purpose**

This system provides a data-driven method for selecting optimal crops based on soil health and environmental parameters for the Mysuru region. It helps farmers, students, and researchers make informed agricultural decisions.

---

## **Author**

**Rakesh Gowda P**
Information Science Engineering
Focused on Machine Learning, Django Development, and Cloud/DevOps.

