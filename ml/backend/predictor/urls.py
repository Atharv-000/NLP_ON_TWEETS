from django.urls import path
from .views import home, predict_api, predict_csv_api

urlpatterns = [
    path('predict/', predict_api),
    path('predict-csv/', predict_csv_api),
]
