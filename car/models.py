from django.db import models

from access.models import User

# Create your models here.
class Car(models.Model):
    car_id = models.CharField(max_length=36,null=True)
    user= models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    is_linked=models.BooleanField(null=True ,default=False)