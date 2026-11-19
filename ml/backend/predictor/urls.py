from django.urls import path
from .views import home, predict_api, predict_csv_api

urlpatterns = [
    path('', home, name='home'),
    path('predict/', predict_api, name='predict'),
    path('predict-csv/', predict_csv_api, name='predict-csv'),
]
