from django.http import JsonResponse
from django.shortcuts import redirect, render
from battery.models import Battery
from django.views.decorators.csrf import csrf_exempt
from car.models import Car
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta

from chargingMode.models import ChargingMode
from .models import Regeneretion, Battery
import requests
from django.utils import timezone
import datetime



# Create your views here.

@csrf_exempt
def battery_details(request, car_id):
        print("enter")
        print(car_id)
        car = Car.objects.get(car_id=car_id)
        print(car)
        try:
            battery_data = Battery.objects.get(car_id=car.id)
        except Battery.DoesNotExist:
            battery_data = None
        
        # Set default values for battery data fields
        battery_percentage = 0
        battery_health = 0
        charging_state = "not charging"
        battery_temperature = 0
        below30=False
        above80=False
        anything=False
        
        if battery_data:
            battery_percentage = battery_data.battery_percentage
            battery_health = battery_data.state_of_health
            charging_state = battery_data.state_of_charging
            battery_temperature = battery_data.temperature

            if battery_percentage<30:
                below30=True
                print("after",below30)
            elif  battery_percentage>80:
                above80=True
                print("after90",above80)
            else:
                anything=True

       

        # Create a context dictionary with the battery data
        context = {
            'car_id': car_id,
            'battery_percentage': battery_percentage,
            'battery_health': battery_health,
            'charging_state': charging_state,
            'battery_temperature': battery_temperature,
            'change_mode_below_30': battery_percentage < 30,
            'change_mode_80': battery_percentage == 80,
            'below':below30,
            'above':above80,
            'anything':anything,
        }
        return render(request,'battery.html',context)




@csrf_exempt
def battery(request,car_id):
    if request.method == 'GET':
        car = Car.objects.get(car_id=car_id)
        battery=Battery.objects.filter(car_id=car.id).first()
        battery_percentage = 0
        state_of_health = 0
        state_of_charging = "not charging"
        temperature = 0
        below30=False
        above80=False
        print("befoore",below30)
        print("before56",above80)

        
        if battery:
            battery_percentage = battery.battery_percentage
            state_of_health = battery.state_of_health
            state_of_charging = battery.state_of_charging
            temperature = battery.temperature
            if battery_percentage<30:
                below30=True
                print("after",below30)
            if  battery_percentage>80:
                above80=True
                print("after90",above80)

        battery_info = {
                'percentage_charge': battery_percentage,
                'state_of_health':state_of_health,
                'state_of_charging':state_of_charging ,
                'temperature': temperature,
                'below':below30,
                'above':above80
        }
        print(battery_info)
        return JsonResponse(battery_info)
      

    if request.method== 'POST':
        print('post enter')
        if Car.objects.filter(car_id=car_id).exists():
            car = Car.objects.get(car_id=car_id)
            percentage_charge =request.POST['percentage_charge'] 
            print('percentage_charge')
            state_of_health =request.POST['state_of_health'] 
            print('state_of_health')

            state_of_charging =request.POST['state_of_charging'] 
            temperature =request.POST['temperature'] 
            if not Battery.objects.filter(car_id=car.id).exists():
                Battery.objects.create(battery_percentage=percentage_charge,state_of_health=state_of_health,
                                    state_of_charging=state_of_charging,
                                    temperature=temperature,car_id=car.id)
            Regeneretion.objects.create(battery_percentage=percentage_charge,car_id=car.id)  
            charging_mode=ChargingMode.objects.filter(car_id=car.id).first()
            if charging_mode is None:
                  ChargingMode.objects.create(mode="-",car_id=car.id)
            battery=Battery.objects.get(car_id=car.id)
            battery.battery_percentage=percentage_charge
            battery.state_of_health=state_of_health
            battery.state_of_charging=state_of_charging
            battery.temperature=temperature
            battery.save()
            return JsonResponse(
                    {'status': 'success'},
                    safe=False
                )
        else:
            return JsonResponse(
                {'status': 'failed'},
                safe=False
            )

    # if request.method== 'POST':
    #     if Car.objects.filter(car_id=car_id).exists():
    #         car = Car.objects.get(car_id=car_id)
    #         percentage_charge =request.POST['percentage_charge'] 
    #         state_of_health =request.POST['state_of_health'] 
    #         state_of_charging =request.POST['state_of_charging'] 
    #         temperature =request.POST['temperature'] 
    #         if not Battery.objects.filter(car_id=car.id).exists():
    #             Battery.objects.create(battery_percentage=percentage_charge,state_of_health=state_of_health,
    #                                 state_of_charging=state_of_charging,
    #                           temperature=temperature,car_id=car.id)
    #         Regeneretion.objects.create(battery_percentage=percentage_charge,car_id=car.id)   
    #         battery=Battery.objects.get(car_id=car.id)
    #         battery.battery_percentage=percentage_charge
    #         battery.state_of_health=state_of_health
    #         battery.state_of_charging=state_of_charging
    #         battery.temperature=temperature
    #         battery.save()
    #         return JsonResponse(
    #                 {'status': 'success'},
    #                 safe=False
    #             )
    #     else:
    #         return JsonResponse(
    #             {'status': 'failed'},
    #             safe=False
    #         )
        
from django.shortcuts import render
from .models import Regeneretion
@csrf_exempt
def regeneration_graph(request, car_id):
    car=Car.objects.get(car_id=car_id)
    try:
        regenerations = Regeneretion.objects.filter(car_id=car.id).order_by('time')
    except Regeneretion.DoesNotExist:
        regenerations = []

    # Extract battery percentage and time from Regeneretion objects
    labels = []
    data = []
    print(regenerations)
    for regen in regenerations:
        labels.append(regen.time.strftime(' %M'))
        data.append(float(regen.battery_percentage)) 
    print(labels)
    print(data)
    # Create context dictionary
    context = {
        'car_id': car_id,
        'labels': labels,
        'data': data,
    }

    return render(request, 'regeneration.html', context)
