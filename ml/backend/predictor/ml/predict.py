import numpy as np

from predictor.ml.model_loader import model, tokenizer
from predictor.ml.preprocess import preprocess_texts


from predictor.ml.model_loader import model, tokenizer
from predictor.ml.preprocess import preprocess_texts

def predict_tweets(tweets):
    import pandas as pd

def predict_from_csv(file):
    """
    file: Uploaded CSV file
    returns: list of predictions
    """

    df = pd.read_csv(file)

    if 'text' not in df.columns:
        raise ValueError("CSV must contain a 'text' column")

    tweets = df['text'].astype(str).tolist()
    return predict_tweets(tweets)

    """
    tweets: list of strings
    returns: list of dicts with prediction & confidence
    """

    # Ensure input is a list
    if isinstance(tweets, str):
        tweets = [tweets]

    # Preprocess
    X = preprocess_texts(tweets, tokenizer)

    # Predict probabilities
    probs = model.predict(X)

    results = []
    for tweet, prob in zip(tweets, probs):
        confidence = float(prob[0])

        label = "Disaster" if confidence >= 0.5 else "Non-Disaster"

        results.append({
            "tweet": tweet,
            "prediction": label,
            "confidence": round(confidence, 4)
        })

    return results
