import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib

# Load CSV
data = pd.read_csv('mysuru_crop_data.csv')

# Prepare input (X) and output (y)
X = data[['N', 'P', 'K', 'pH', 'rainfall']]
y = data['label']

# Train model
model = DecisionTreeClassifier()
model.fit(X, y)

# Save model to file
joblib.dump(model, 'crop_model_mysuru.pkl')
print(" Model trained and saved!")
