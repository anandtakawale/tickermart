from django.urls import path
from .views import pnf_home, pnf_date

urlpatterns = [
    path('', pnf_home, name="pnf"),
    path('<str:datestr>', pnf_date, name="bostocks")
]
