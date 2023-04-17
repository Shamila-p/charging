from django.http import JsonResponse
from django.shortcuts import render
from battery.models import Battery
from django.views.decorators.csrf import csrf_exempt
from car.models import Car

# Create your views here.

def battery_details(request, car_id):
    car = Car.objects.get(car_id=car_id)
    try:
        battery_data = Battery.objects.get(car_id=car.id)
    except Battery.DoesNotExist:
        battery_data = None
    
    # Set default values for battery data fields
    battery_percentage = 0
    battery_health = 0
    charging_state = "not charging"
    battery_temperature = 0
    
    if battery_data:
        battery_percentage = battery_data.battery_percentage
        battery_health = battery_data.state_of_health
        charging_state = battery_data.state_of_charging
        battery_temperature = battery_data.temperature
    
    # Create a context dictionary with the battery data
    context = {
        'car_id': car_id,
        'battery_percentage': battery_percentage,
        'battery_health': battery_health,
        'charging_state': charging_state,
        'battery_temperature': battery_temperature,
    }
    return render(request,'battery.html',context)




@csrf_exempt
def battery(request,car_id):
    if request.method == 'GET':
        car = Car.objects.get(car_id=car_id)
        battery=Battery.objects.get(car_id=car.id)
        battery_info = {
            'percentage_charge': battery.battery_percentage,
            'state_of_health':battery. state_of_health,
            'state_of_charging':battery.state_of_charging ,
            'temperature': battery.temperature,
        }
        return JsonResponse(battery_info)
    if request.method== 'POST':
        if Car.objects.filter(car_id=car_id).exists():
            car = Car.objects.get(car_id=car_id)
            percentage_charge =request.POST['percentage_charge'] 
            state_of_health =request.POST['state_of_health'] 
            state_of_charging =request.POST['state_of_charging'] 
            temperature =request.POST['temperature'] 
            if not Battery.objects.filter(car_id=car.id).exists():
                Battery.objects.create(battery_percentage=percentage_charge,state_of_health=state_of_health,
                                    state_of_charging=state_of_charging,
                                    temperature=temperature,car_id=car.id)
               
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