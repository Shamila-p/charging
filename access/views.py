from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import auth
from access.models import User
from car.models import Car

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return render(request,'index.html')

def signup(request):
    if request.method == 'GET':
        return render(request,'signup.html')
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if not password1 == password2:
            messages.info(request, 'password incorrect')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'email taken')
        elif User.objects.filter(phone=phone).exists():
            messages.info(request, 'phone number already registered')
        else:
            print("eneter")
            user=User.objects.create_user(first_name=name, username=email,
                                            email=email, phone=phone, password=password1)
              
            Car.objects.create(user_id=user.id)                              
            return redirect('login')
        return redirect('signup')

def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated :
            return redirect('home')
        return render(request, 'login.html')
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('link_car')
        messages.error(request, 'Wrong credentials!!!')
        return redirect('login')
    
def home(request):
    if request.method == 'GET':
        if not request.user.is_authenticated :
            return redirect('login')
        print("this",request.user.id)
        
        if Car.objects.filter(user_id=request.user.id).exists:
            car=Car.objects.get(user_id=request.user.id)
            context={'car_id':car.car_id}
            return render(request, 'home.html',context)
        return redirect('link_car')
    
def logout(request):
    auth.logout(request)
    return redirect('login')