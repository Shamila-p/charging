from . import views
from django.urls import path


urlpatterns=[
     path('link-car',views.link_car,name="link_car"),
     path('unlink-car',views.unlink_car,name="unlink_car"),
]