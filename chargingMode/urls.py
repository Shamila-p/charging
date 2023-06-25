from . import views
from django.urls import path

urlpatterns=[
    path('charging-mode-details/<int:car_id>',views.charging_mode_concept,name='charging_mode_details'),
    # path('charging-mode/<int:car_id>',views.charging_mode,name='charging_mode')
]