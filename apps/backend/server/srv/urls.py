# apps/backend/backend/urls.py

from django.urls import path
from .views import TestConnectionView

urlpatterns = [
    path('test/', TestConnectionView.as_view(), name='test_connection'),
]
