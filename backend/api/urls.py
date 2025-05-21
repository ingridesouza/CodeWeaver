# api/urls.py

from django.urls import path
from .views import GenerateLandingPageView

urlpatterns = [
    path('generate/', GenerateLandingPageView.as_view(), name='generate-landing-page'),
]
