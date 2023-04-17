from . import views
from django.urls import path


urlpatterns=[
     path('battery-details/<int:car_id>',views.battery_details,name="battery_details"),
     path('battery/<int:car_id>',views.battery,name="battery")
]