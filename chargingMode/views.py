from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from car.models import Car
from chargingMode.models import ChargingMode

# Create your views here.

def charging_mode_details(request,car_id):
    car = Car.objects.get(car_id=car_id)
    try:
        mode = ChargingMode.objects.get(car_id=car.id)
    except ChargingMode.DoesNotExist:
        mode = None
    
    charging_mode = "Not charging"
    
    
    if mode:
        charging_mode=mode.mode
    
    context = {
        'car_id': car_id,
        'charging_mode': charging_mode,
    }
    return render(request,'mode.html',context)



@csrf_exempt
def charging_mode(request,car_id):
    if request.method=='GET':
        car=Car.objects.get(car_id=car_id)
        mode_of=ChargingMode.objects.get(car_id=car.id)
        mode={
            'charging_mode':mode_of.mode
        }
        return JsonResponse(mode)
    if request.method=='POST':
        if Car.objects.filter(car_id=car_id).exists():
            car = Car.objects.get(car_id=car_id)
            mode =request.POST['mode'] 
            if not ChargingMode.objects.filter(car_id=car.id).exists():
                ChargingMode.objects.create(mode=mode,car_id=car.id)
            mode_of=ChargingMode.objects.get(car_id=car.id)
            mode_of.mode=mode
            mode_of.save()
            return JsonResponse(
                    {'status': 'success'},
                    safe=False
                )
        else:
            return JsonResponse(
                {'status': 'failed'},
                safe=False
            )