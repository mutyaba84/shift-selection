# users/urls.py

from django.urls import path
from .views import shift_list, subscribe

urlpatterns = [
    path('shift-list/', shift_list, name='shift_list'),
    path('subscribe/', subscribe, name='subscribe'),
    # Add other paths as needed based on your views and models
]
