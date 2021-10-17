from django.urls import path
from .views import pnf_home

urlpatterns = [
    path('', pnf_home, name="pnf"),
]
