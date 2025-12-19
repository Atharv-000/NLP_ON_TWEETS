from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # 👇 ROOT URL NOW POINTS TO UI
    path("", include("predictor.urls")),
]
