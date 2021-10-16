from django.db import models
from django.db.models.base import Model

# Create your models here.
class Breakout_stock(models.Model):
    date = models.DateField()
    stock_name = models.CharField(max_length=50)
    close = models.DecimalField(max_digits=10, decimal_places=2)
    boxsize = models.DecimalField(max_digits=10, decimal_places=2)
    sl = models.DecimalField(max_digits=10, decimal_places=2)
    breakout = models.BooleanField()
