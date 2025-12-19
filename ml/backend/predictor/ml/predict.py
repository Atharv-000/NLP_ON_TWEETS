import numpy as np
import pandas as pd
from predictor.ml.model_loader import model, tokenizer
from predictor.ml.preprocess import preprocess_texts


def predict_tweets(tweets):
    """
    tweets: list of strings
    returns: list of dicts with prediction & confidence
    """
    # Check if model and tokenizer are loaded
    if model is None or tokenizer is None:
        raise ValueError("Model or tokenizer not loaded. Please check model files.")

    # Ensure input is a list
    if isinstance(tweets, str):
        tweets = [tweets]

    if not tweets or len(tweets) == 0:
        raise ValueError("No tweets provided for prediction")

    try:
        print(f"Processing {len(tweets)} tweet(s)...")
        
        # Preprocess
        X = preprocess_texts(tweets, tokenizer)
        print(f"Preprocessed shape: {X.shape}")
        
        # Predict probabilities
        probs = model.predict(X, verbose=0)
        print(f"Predictions shape: {probs.shape}")
        print(f"Sample prediction: {probs[0] if len(probs) > 0 else 'None'}")
        
        results = []
        for tweet, prob in zip(tweets, probs):
            # Handle different probability formats
            if isinstance(prob, (list, np.ndarray)):
                if len(prob) > 0:
                    confidence = float(prob[0])
                else:
                    confidence = float(prob)
            else:
                confidence = float(prob)
            
            label = "Disaster" if confidence >= 0.5 else "Non-Disaster"

            results.append({
                "tweet": tweet,
                "prediction": label,
                "confidence": round(confidence, 4)
            })

        print(f"Generated {len(results)} results")
        return results
    except Exception as e:
        import traceback
        print(f"Error in predict_tweets: {str(e)}")
        print(traceback.format_exc())
        raise Exception(f"Error during prediction: {str(e)}")


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
