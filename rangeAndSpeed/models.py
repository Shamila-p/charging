from django.db import models

from car.models import Car

# Create your models here.

class RangeAndSpeed(models.Model):
    range = models.DecimalField(max_digits=8, decimal_places=2)
    speed = models.DecimalField(max_digits=8, decimal_places=2)
    car = models.ForeignKey(Car, on_delete=models.CASCADE,null=False)
