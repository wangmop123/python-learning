from django.urs import path
from django.urls import include, path

urlpatterns = [
    path(),
    path("", include("predictor.urls")),
]