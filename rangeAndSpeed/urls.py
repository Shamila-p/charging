from django.urls import path
from . import views

urlpatterns=[
    path('range-speed/<int:car_id>',views.range_speed,name='range_speed'),
    path('view-range-speed/<int:car_id>',views.view_range_speed,name='view_range_speed')

]