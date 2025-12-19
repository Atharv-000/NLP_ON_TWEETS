import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.utils import class_weight

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout, Bidirectional
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping

from preprocess import preprocess_and_tokenize, MAX_WORDS, MAX_LEN

# -----------------------------
# Load & preprocess data
# -----------------------------
df = pd.read_csv("data/train.csv")
X, y = preprocess_and_tokenize(df)

X_train, X_val, y_train, y_val = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# -----------------------------
# Class weights
# -----------------------------
weights = class_weight.compute_class_weight(
    class_weight='balanced',
    classes=np.unique(y_train),
    y=y_train
)
class_weights = {i: weights[i] for i in range(len(weights))}
print("Class weights:", class_weights)

# -----------------------------
# Improved Model
# -----------------------------
model = Sequential([
    Embedding(
        input_dim=MAX_WORDS,
        output_dim=128,
        input_length=MAX_LEN
    ),
    Bidirectional(LSTM(64, return_sequences=False)),
    Dropout(0.4),
    Dense(1, activation='sigmoid')
])

model.compile(
    optimizer=Adam(learning_rate=0.0005),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

model.summary()

# -----------------------------
# Train
# -----------------------------
early_stop = EarlyStopping(
    monitor='val_loss',
    patience=3,
    restore_best_weights=True
)

history = model.fit(
    X_train,
    y_train,
    validation_data=(X_val, y_val),
    epochs=10,
    batch_size=64,
    class_weight=class_weights,
    callbacks=[early_stop]
)

# -----------------------------
# Save improved model
# -----------------------------
model.save("model/disaster_lstm_v2.h5")
print("✅ Improved model saved: model/disaster_lstm_v2.h5")
