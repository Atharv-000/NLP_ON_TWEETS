# Render Deployment Guide

## Quick Start

### Option 1: Using Render Dashboard (Recommended)

1. **Go to Render Dashboard**
   - Visit https://dashboard.render.com
   - Sign up/Login with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `Atharv-000/NLP_ON_TWEETS`
   - Click "Connect"

3. **Configure Settings**
   - **Name**: `nlp-on-tweets` (or your preferred name)
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: Leave empty (root of repo)
   - **Environment**: `Python 3`
   - **Build Command**:
     ```bash
     pip install --upgrade pip && pip install -r requirements.txt && cd ml/backend && python manage.py collectstatic --noinput
     ```
   - **Start Command**:
     ```bash
     cd ml/backend && gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT
     ```

4. **Set Environment Variables**
   Click "Advanced" → "Add Environment Variable":
   - `SECRET_KEY`: Generate using:
     ```python
     python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
     ```
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `your-app-name.onrender.com` (Render will provide this after first deploy)

5. **Deploy**
   - Click "Create Web Service"
   - Wait for build to complete (5-10 minutes for first build)
   - Your app will be live at `https://your-app-name.onrender.com`

### Option 2: Using render.yaml (Automatic)

If you use `render.yaml`, Render will automatically detect it:

1. **Connect Repository** (same as above)
2. **Render will auto-detect** `render.yaml`
3. **Review and Deploy**
   - Render will use settings from `render.yaml`
   - You may need to update `ALLOWED_HOSTS` in environment variables

## Important Notes

### Model Files Size
- Your model files (`disaster_lstm_v2.h5` and `tokenizer.pkl`) are large
- Ensure they're committed to Git (not in `.gitignore`)
- First deployment may take longer due to model file upload

### Free Tier Limitations
- Render free tier has **512MB RAM** and **0.1 CPU**
- Your app may spin down after 15 minutes of inactivity
- First request after spin-down may take 30-60 seconds (cold start)

### Environment Variables Checklist
- ✅ `SECRET_KEY` - Django secret key
- ✅ `DEBUG` - Set to `False`
- ✅ `ALLOWED_HOSTS` - Your Render domain
- ✅ `PYTHON_VERSION` - Already set in render.yaml (3.11.0)

### Troubleshooting

#### Build Fails
- Check Render logs for errors
- Verify all dependencies in `requirements.txt`
- Ensure Python version matches (3.11.0)

#### App Crashes on Start
- Check logs in Render dashboard
- Verify `startCommand` path is correct
- Ensure model files exist in correct location

#### Static Files Not Loading
- Verify `collectstatic` runs in build command
- Check `STATIC_ROOT` in settings.py
- Ensure WhiteNoise is installed (already in requirements.txt)

#### Model Loading Errors
- Check file paths in `model_loader.py`
- Verify model files are committed to Git
- Check Render logs for file not found errors

## Post-Deployment

1. **Test Your App**
   - Visit your Render URL
   - Test single tweet prediction
   - Test CSV upload

2. **Monitor Logs**
   - Go to Render dashboard → Your service → Logs
   - Watch for any errors

3. **Update Domain** (Optional)
   - Render provides free subdomain
   - You can add custom domain in settings

## File Structure for Render

```
NLP_ON_TWEETS/
├── requirements.txt          # Python dependencies
├── Procfile                 # Process file for Render
├── render.yaml              # Render configuration
├── README.md                # Project documentation
├── .gitignore               # Git ignore rules
└── ml/
    └── backend/             # Django project
        ├── manage.py
        ├── backend/
        │   ├── settings.py   # Updated for production
        │   ├── wsgi.py       # WSGI config
        │   └── urls.py
        └── predictor/
            ├── ml/
            │   ├── disaster_lstm_v2.h5  # Model file
            │   ├── tokenizer.pkl        # Tokenizer file
            │   └── ...
            └── templates/
                └── predictor/
                    └── home.html
```

## Support

If you encounter issues:
1. Check Render logs
2. Verify all files are committed
3. Check environment variables
4. Review this guide

Good luck with your deployment! 🚀

