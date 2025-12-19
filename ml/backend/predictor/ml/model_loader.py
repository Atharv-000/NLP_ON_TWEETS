import os
import joblib
from tensorflow.keras.models import load_model

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "disaster_lstm_v2.h5")
TOKENIZER_PATH = os.path.join(BASE_DIR, "tokenizer.pkl")

model = load_model(MODEL_PATH)
tokenizer = joblib.load(TOKENIZER_PATH)
