from django.shortcuts import render

def home(request):
    return render(request, "pages/home.html", {})

def login(request):
    return render(request, "pages/LoginComponent/LoginPage.html", {})

def register(request):
    return render(request, "pages/LoginComponent/RegisterPage.html", {})

def reservation_page(request):
    return render(request, 'pages/ReservationComponent/ReservationPageGuest.html') 
