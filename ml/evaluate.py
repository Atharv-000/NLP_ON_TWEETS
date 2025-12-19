import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

from tensorflow.keras.models import load_model
from preprocess import preprocess_and_tokenize

# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv("data/train.csv")
X, y = preprocess_and_tokenize(df)

# Same split as training
X_train, X_val, y_train, y_val = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# -----------------------------
# Load model
# -----------------------------
model = load_model("model/disaster_lstm.h5")

# -----------------------------
# Predict
# -----------------------------
y_pred_prob = model.predict(X_val)
y_pred = (y_pred_prob >= 0.5).astype(int)

# -----------------------------
# Metrics
# -----------------------------
print("Accuracy:", accuracy_score(y_val, y_pred))
print("Precision:", precision_score(y_val, y_pred))
print("Recall:", recall_score(y_val, y_pred))
print("F1 Score:", f1_score(y_val, y_pred))

print("\nClassification Report:\n")
print(classification_report(y_val, y_pred))

# -----------------------------
# Confusion Matrix
# -----------------------------
cm = confusion_matrix(y_val, y_pred)
print("Confusion Matrix:\n", cm)
