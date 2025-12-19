from django.urls import path
from .views import home, predict_api, predict_csv_api

urlpatterns = [
    path("", home),                    # /
    path("api/predict/", predict_api),
    path("api/predict-csv/", predict_csv_api),
]
