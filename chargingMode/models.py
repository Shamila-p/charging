from django.db import models

from car.models import Car

# Create your models here.
class ChargingMode(models.Model):
    CAR_TO_HOME = 'car_to_home'
    HOME_TO_CAR = 'home_to_car'
    MODE_CHOICES = [
        (CAR_TO_HOME, 'Car to Home'),
        (HOME_TO_CAR, 'Home to Car'),
    ]
    car = models.ForeignKey(Car, on_delete=models.CASCADE,null=False)
    mode = models.CharField(max_length=20, choices=MODE_CHOICES)