from django.shortcuts import render, redirect 
from .models import User
from django.contrib import messages

def home(request):
    users = User.objects.all()
    return render(request, 'pages/home.html', {'users': users})  

def login(request):
    username = None  
    password = None  
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username and password:
            try:
                user = User.objects.get(username=username, password=password)
                request.session['user_id'] = user.id
                messages.success(request, "You are logged in successfully!")
                return redirect('reservation_page')
            except User.DoesNotExist:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Please enter both username and password")
    return render(request, "pages/LoginComponent/LoginPage.html", {})

def register(request):
    return render(request, "pages/LoginComponent/RegisterPage.html", {})

def reservation_page(request):
    return render(request, 'pages/ReservationComponent/ReservationPageGuest.html') 

def modify_reservation(request):
    return render(request, "pages/ReservationPage.html")

def search_reservation(request):
    return render(request, "pages/ReservationComponent/ReservationSearch.html")