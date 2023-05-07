from django.shortcuts import render,redirect

from car.models import Car

# Create your views here.

def link_car(request):
    if request.method=='GET':
        if Car.objects.filter(user_id=request.user.id).exists:
            car=Car.objects.get(user_id=request.user.id)
            if car.is_linked is not True:
                return render(request,'link.html')
            return redirect('home')
        else:
        # car = Car.objects.get(user_id=request.user.id)
        # if car.is_linked is not True:
            return render(request,'link.html')
        # else:
        #     return redirect ('home')
    if request.method == 'POST':
        car_id = request.POST['car_id']
        print(car_id)
        if Car.objects.filter(user_id=request.user.id).exists:
            car = Car.objects.get(user_id=request.user.id)
            car.car_id = car_id
            car.is_linked = True
            car.save()
        else:
            Car.objects.create(user_id=request.user.id,car_id=car_id,is_linked=True)
        return redirect('home')
def unlink_car(request):
    if request.method == 'POST':
        car = Car.objects.get(user_id=request.user.id)
        # car.car_id = None
        car.is_linked =False
        car.save()
        return redirect('link_car')