from django.shortcuts import render

def home(request):
    return render(request, "pages/home.html", {})

def login(request):
    return render(request, "pages/LoginComponent/LoginPage.html", {})

def register(request):
    return render(request, "pages/LoginComponent/RegisterPage.html", {})

def reservation_page(request):
    return render(request, 'pages/ReservationComponent/ReservationPageGuest.html') 

def modify_reservation(request):
    return render(request, "pages/ReservationPage.html")

def search_reservation(request):
    return render(request, "pages/ReservationComponent/ReservationSearch.html")