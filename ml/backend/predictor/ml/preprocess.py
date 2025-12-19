import re
import joblib
from nltk.corpus import stopwords
import nltk
from tensorflow.keras.preprocessing.sequence import pad_sequences

nltk.download('stopwords')

STOPWORDS = set(stopwords.words('english'))

MAX_LEN = 100

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-z\s]", "", text)
    words = text.split()
    words = [w for w in words if w not in STOPWORDS]
    return " ".join(words)

def preprocess_texts(texts, tokenizer):
    cleaned = [clean_text(t) for t in texts]
    sequences = tokenizer.texts_to_sequences(cleaned)
    padded = pad_sequences(sequences, maxlen=MAX_LEN, padding='post')
    return padded
