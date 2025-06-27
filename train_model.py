# train_model.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# Step 1: Load the CSV (your format has N,P,K,pH,rainfall,label)
df = pd.read_csv("mysuru_crop_data.csv")

# Rename for consistency
df.columns = ['nitrogen', 'phosphorus', 'potassium', 'ph', 'rainfall', 'label']

# Step 2: Add artificial temperature, humidity, soil_type
np.random.seed(42)
df['temperature'] = np.random.uniform(20, 35, size=len(df))   # realistic Mysuru range
df['humidity'] = np.random.uniform(40, 90, size=len(df))
df['soil_type'] = np.random.choice(['Red', 'Black', 'Loamy'], size=len(df))

# Step 3: Encode soil_type and label
soil_encoder = LabelEncoder()
df['soil_type'] = soil_encoder.fit_transform(df['soil_type'])

crop_encoder = LabelEncoder()
df['label'] = crop_encoder.fit_transform(df['label'])

# Step 4: Train-test split
X = df.drop("label", axis=1)
y = df["label"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 5: Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Step 6: Save the trained model and encoders
joblib.dump(model, 'crop_model.pkl')
joblib.dump(soil_encoder, 'soil_encoder.pkl')
joblib.dump(crop_encoder, 'crop_encoder.pkl')

print("✅ Model, soil encoder, and crop encoder trained and saved successfully!")