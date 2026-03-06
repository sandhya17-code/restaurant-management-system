from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth import logout
from .models import Profile
from foodie.models import Order
from django.contrib.auth.decorators import login_required


def register(request):
    message = ""
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        address = request.POST['address']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                message = "Username already exists"
                return render(request, 'register.html', {'message': message})
            elif User.objects.filter(email=email).exists():
                message = "Email already exists"
                return render(request, 'register.html', {'message': message})
            else:
                user = User.objects.create_user(
                    username=username,
                    password=password1,
                    email=email,
                    first_name=first_name,
                    last_name=last_name
                )
                user.save()

                Profile.objects.create(user=user,address=address)
                message = "User created successfully"
                return redirect('login')  # after success, go to login
        else:
            message = "Passwords do not match"
            return render(request, 'register.html', {'message': message})
    else:
        return render(request, 'register.html', {'message': message})


def login(request):
    message = ""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user:
            auth.login(request, user)
            return redirect('/')  # go to home/dashboard
        else:
            message = "Invalid credentials"
            return render(request, 'login.html', {'message': message})
    else:
        return render(request, 'login.html', {'message': message})
    
def logout_user(request):
      logout(request)
      return render(request,'logout_user.html')


@login_required   #decorator 
def profile_view(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    recent_orders = Order.objects.filter(user=request.user).order_by('-created_at')[:10] # last 10 orders

    return render(request,"profile.html",{
        "user":user,
        "profile":profile,
        "recent_orders":recent_orders
    })