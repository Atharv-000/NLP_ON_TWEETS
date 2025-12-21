from django.urls import path
from .views import predict_api, predict_csv_api

urlpatterns = [
    path('predict/', predict_api, name='predict'),
    path('predict-csv/', predict_csv_api, name='predict-csv'),
]
