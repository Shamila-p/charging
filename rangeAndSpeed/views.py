from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from car.models import Car
from rangeAndSpeed.models import RangeAndSpeed

# Create your views here.
def view_range_speed(request,car_id):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        car = Car.objects.get(car_id=car_id)
        try:
            range_and_speed = RangeAndSpeed.objects.get(car_id=car.id)
        except RangeAndSpeed.DoesNotExist:
            range_and_speed = None
        
        range= "-"
        speed = "-"
        
        if range_and_speed:
            range = range_and_speed.range
            speed = range_and_speed.speed
        
        context = {
            'car_id': car_id,
            'range': range,
            'speed': speed,
        }
        return render(request, 'range_and_speed.html', context)




@csrf_exempt
def range_speed(request,car_id):
    if request.method=='GET':
        car=Car.objects.get(car_id=car_id)
        range_and_speed=RangeAndSpeed.objects.filter(car_id=car.id).first()
        
        range= "-"
        speed = "-"
        
        if range_and_speed:
            range = range_and_speed.range
            speed = range_and_speed.speed
        
        context = {
            'range': range,
            'speed': speed,
        }
        return JsonResponse(context)
    
    if request.method=='POST':
        if Car.objects.filter(car_id=car_id).exists():
            car = Car.objects.get(car_id=car_id)
            range =request.POST['range'] 
            speed =request.POST['speed'] 
            if not RangeAndSpeed.objects.filter(car_id=car.id).exists():
                RangeAndSpeed.objects.create(range=range,speed=speed,car_id=car.id)
            entry=RangeAndSpeed.objects.get(car_id=car.id)
            entry.speed=speed
            entry.range=range
            entry.save()
            return JsonResponse(
                    {'status': 'success'},
                    safe=False
                )
        else:
            return JsonResponse(
                {'status': 'failed'},
                safe=False
            )