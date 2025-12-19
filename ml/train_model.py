import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.utils import class_weight

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping

from preprocess import preprocess_and_tokenize, MAX_WORDS, MAX_LEN

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv("data/train.csv")

# Preprocess text
X, y = preprocess_and_tokenize(df)

# -----------------------------
# Train / Validation split
# -----------------------------
X_train, X_val, y_train, y_val = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# -----------------------------
# Handle class imbalance
# -----------------------------
weights = class_weight.compute_class_weight(
    class_weight='balanced',
    classes=np.unique(y_train),
    y=y_train
)

class_weights = {i: weights[i] for i in range(len(weights))}
print("Class weights:", class_weights)

# -----------------------------
# Build LSTM model
# -----------------------------
model = Sequential([
    Embedding(input_dim=MAX_WORDS, output_dim=128, input_length=MAX_LEN),
    LSTM(128),
    Dropout(0.5),
    Dense(1, activation='sigmoid')
])

model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

model.summary()

# -----------------------------
# Training
# -----------------------------
early_stop = EarlyStopping(
    monitor='val_loss',
    patience=2,
    restore_best_weights=True
)

history = model.fit(
    X_train,
    y_train,
    validation_data=(X_val, y_val),
    epochs=5,
    batch_size=64,
    class_weight=class_weights,
    callbacks=[early_stop]
)

# -----------------------------
# Save model
# -----------------------------
model.save("model/disaster_lstm.h5")
print("✅ Model saved at model/disaster_lstm.h5")
