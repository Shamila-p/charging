from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from battery.models import Battery
from car.models import Car
from chargingMode.models import ChargingMode

# Create your views here.

# def charging_mode_details(request,car_id):
#     if not request.user.is_authenticated:
#         return redirect('login')
#     else:
#         car = Car.objects.get(car_id=car_id)
        
#         try:
#             mode = ChargingMode.objects.get(car_id=car.id)
#         except ChargingMode.DoesNotExist:
#             mode = None
        
#         charging_mode = "Not charging"
        
        
#         if mode:
#             charging_mode=mode.mode
        
#         context = {
#             'car_id': car_id,
#             'charging_mode': charging_mode,
#         }
#         return render(request,'mode.html',context)



# @csrf_exempt
# def charging_mode(request,car_id):
#     if request.method=='GET':
#         car=Car.objects.get(car_id=car_id)
#         mode_of=ChargingMode.objects.filter(car_id=car.id).first()
        
#         charging_mode = "Not charging"
        
#         if mode_of:
#             charging_mode=mode_of.mode
        
#         mode = {
#             'charging_mode': charging_mode,
#         }
       
#         return JsonResponse(mode)
    
#     if request.method=='POST':
#         if Car.objects.filter(car_id=car_id).exists():
#             car = Car.objects.get(car_id=car_id)
#             mode =request.POST['mode'] 
#             if not ChargingMode.objects.filter(car_id=car.id).exists():
#                 ChargingMode.objects.create(mode=mode,car_id=car.id)
#             mode_of=ChargingMode.objects.get(car_id=car.id)
#             mode_of.mode=mode
#             mode_of.save()
#             return JsonResponse(
#                     {'status': 'success'},
#                     safe=False
#                 )
#         else:
#             return JsonResponse(
#                 {'status': 'failed'},
#                 safe=False
#             )
        
def charging_mode_concept(request,car_id):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        below=False
        above=False
        mode='-'
        context={}
        if request.method == 'GET':
            car = Car.objects.get(car_id=car_id)
            if Battery.objects.filter(car_id=car.id).exists():
                battery=Battery.objects.filter(car_id=car.id).first()
                mode = ChargingMode.objects.filter(car_id=car.id).first()

                if battery.battery_percentage < 30:
                    below=True
                if battery.battery_percentage>80:
                    above=True
                context = {
                'below':below,
                'above':above,
                'car_id': car_id,
                'charging_mode': mode,
                }
            print(context)
            return render(request,'mode.html',context)
        if request.method == 'POST':
            car = Car.objects.get(car_id=car_id)
            battery=Battery.objects.get(car_id=car.id)
            mode = ChargingMode.objects.filter(car_id=car.id).first()
            print(mode)
            if battery.battery_percentage<30:
                mode.mode=ChargingMode.HOME_TO_CAR
                mode.save()
            if battery.battery_percentage>80:
                mode.mode=ChargingMode.CAR_TO_HOME
                mode.save()
            return redirect('charging_mode_details',car_id=car_id)
        # try:
        #     mode = ChargingMode.objects.get(car_id=car.id)
        # except ChargingMode.DoesNotExist:
        #     mode = None
        
        # charging_mode = "Not charging"
        
        
        # if mode:
        #     charging_mode=mode.mode
        
        
