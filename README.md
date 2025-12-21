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

## Deployment on Render

### Prerequisites
- GitHub repository with your code
- Render account

### Steps

1. **Connect Repository**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Configure Service**
   - **Name**: nlp-on-tweets (or your preferred name)
   - **Environment**: Python 3
   - **Build Command**: 
     ```bash
     pip install --upgrade pip && pip install -r requirements.txt && cd ml/backend && python manage.py collectstatic --noinput
     ```
   - **Start Command**: 
     ```bash
     cd ml/backend && gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT
     ```

3. **Environment Variables**
   - `SECRET_KEY`: Generate a secure Django secret key
   - `DEBUG`: Set to `False` for production
   - `ALLOWED_HOSTS`: Your Render domain (e.g., `nlp-on-tweets.onrender.com`)

4. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy your application

### Using render.yaml (Alternative)

If you prefer using `render.yaml`, the file is already configured. Just:
1. Connect your repository to Render
2. Render will automatically detect `render.yaml`
3. Follow the prompts to deploy

## API Endpoints

### Single Tweet Prediction
- **URL**: `/api/predict/`
- **Method**: POST
- **Body**: 
  ```json
  {
    "tweets": ["Your tweet text here"]
  }
  ```

### CSV Upload Prediction
- **URL**: `/api/predict-csv/`
- **Method**: POST
- **Body**: Form-data with `file` field containing CSV file
- **CSV Format**: Must have a `text` column

## Model Information

- **Model Type**: LSTM (Long Short-Term Memory) Neural Network
- **Input**: Preprocessed tweet text
- **Output**: Binary classification (Disaster/Non-Disaster) with confidence score
- **Preprocessing**: Text cleaning, tokenization, padding

## Environment Variables

Create a `.env` file for local development:

```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

## Troubleshooting

### Model Loading Issues
- Ensure `disaster_lstm_v2.h5` and `tokenizer.pkl` are in `ml/backend/predictor/ml/`
- Check file paths in `model_loader.py`

### Static Files Not Loading
- Run `python manage.py collectstatic`
- Check `STATIC_ROOT` and `STATIC_URL` in settings.py

### Deployment Issues
- Check Render logs for errors
- Verify environment variables are set
- Ensure all dependencies are in `requirements.txt`

## License

This project is open source and available under the MIT License.

## Author

Atharv-000

## Repository

https://github.com/Atharv-000/NLP_ON_TWEETS

