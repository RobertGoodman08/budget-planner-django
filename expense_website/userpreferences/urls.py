from django.urls import path
from userpreferences.views import preferences

urlpatterns = [
    path('', preferences, name="preferences")
]