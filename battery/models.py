from django.db import models

from car.models import Car

# Create your models here.
class Battery(models.Model):
    car= models.ForeignKey(Car, on_delete=models.CASCADE, null=False)
    battery_percentage = models.IntegerField()
    state_of_health = models.CharField(max_length=255)
    state_of_charging = models.CharField(max_length=255)
    temperature = models.CharField(max_length=255)
