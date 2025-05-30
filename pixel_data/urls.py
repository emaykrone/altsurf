# pixel_data/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('event/', views.PixelEventCreateAPIView.as_view(), name='pixel_event_create'),
    # Здесь могут быть другие API-эндпоинты для pixel_data
]