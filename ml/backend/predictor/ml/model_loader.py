import os
import joblib
from tensorflow.keras.models import load_model

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "disaster_lstm_v2.h5")
TOKENIZER_PATH = os.path.join(BASE_DIR, "tokenizer.pkl")

# Initialize model and tokenizer as None
model = None
tokenizer = None

try:
    print("🔹 Loading LSTM model...")
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at: {MODEL_PATH}")
    model = load_model(MODEL_PATH)
    print("✅ Model loaded successfully")
except Exception as e:
    print(f"❌ Error loading model: {str(e)}")
    raise

try:
    print("🔹 Loading tokenizer...")
    if not os.path.exists(TOKENIZER_PATH):
        raise FileNotFoundError(f"Tokenizer file not found at: {TOKENIZER_PATH}")
    tokenizer = joblib.load(TOKENIZER_PATH)
    print("✅ Tokenizer loaded successfully")
except Exception as e:
    print(f"❌ Error loading tokenizer: {str(e)}")
    raise

print("✅ Model & tokenizer ready for predictions")
