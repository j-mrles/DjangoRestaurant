from django.shortcuts import render
from .models import User


def home(request):
    users = User.objects.all()
    return render(request, 'pages/home.html', {'users': users})  

def login(request):
    return render(request, "pages/LoginComponent/LoginPage.html", {})

def register(request):
    return render(request, "pages/LoginComponent/RegisterPage.html", {})

def reservation_page(request):
    return render(request, 'pages/ReservationComponent/ReservationPageGuest.html') 

def modify_reservation(request):
    return render(request, "pages/ReservationPage.html")