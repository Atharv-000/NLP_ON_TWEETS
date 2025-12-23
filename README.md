# NLP Tweet Disaster Prediction

A Django-based web application that uses Natural Language Processing (NLP) and LSTM neural networks to predict whether a tweet is about a disaster or not.

## Features

- **Single Tweet Prediction**: Enter a tweet and get instant prediction
- **CSV Batch Processing**: Upload a CSV file with multiple tweets for batch prediction
- **Real-time Results**: Get predictions with confidence scores
- **Modern UI**: Beautiful, responsive web interface

## Tech Stack

- **Backend**: Django 6.0, Django REST Framework
- **ML Model**: TensorFlow/Keras LSTM
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Render

## Project Structure

```
ml/backend/              # Django project root
├── backend/             # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── predictor/           # Main app
│   ├── ml/             # ML model files
│   │   ├── model_loader.py
│   │   ├── predict.py
│   │   ├── preprocess.py
│   │   ├── disaster_lstm_v2.h5
│   │   └── tokenizer.pkl
│   ├── templates/      # HTML templates
│   ├── views.py
│   └── urls.py
└── manage.py
```

## Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/Atharv-000/NLP_ON_TWEETS.git
   cd NLP_ON_TWEETS
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   cd ml/backend
   python manage.py migrate
   ```

5. **Start development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   - Open http://127.0.0.1:8000/ in your browser
