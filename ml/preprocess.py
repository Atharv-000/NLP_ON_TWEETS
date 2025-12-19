# ml/preprocess.py

import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import joblib

nltk.download('stopwords')

STOPWORDS = set(stopwords.words('english'))

MAX_WORDS = 10000
MAX_LEN = 100

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-z\s]", "", text)
    words = text.split()
    words = [w for w in words if w not in STOPWORDS]
    return " ".join(words)

def preprocess_and_tokenize(train_df):
    train_df = train_df.copy()
    train_df['clean_text'] = train_df['text'].apply(clean_text)

    tokenizer = Tokenizer(num_words=MAX_WORDS, oov_token="<OOV>")
    tokenizer.fit_on_texts(train_df['clean_text'])

    sequences = tokenizer.texts_to_sequences(train_df['clean_text'])
    padded = pad_sequences(sequences, maxlen=MAX_LEN, padding='post')

    joblib.dump(tokenizer, "model/tokenizer.pkl")
    return padded, train_df['target'].values

if __name__ == "__main__":
    df = pd.read_csv("data/train.csv")
    X, y = preprocess_and_tokenize(df)
    print("Final input shape:", X.shape)
