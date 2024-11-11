from django.shortcuts import render, redirect 
from .models import User
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect

def home(request):
    users = User.objects.all()
    return render(request, 'pages/home.html', {'users': users})  

def login(request):
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
    return render(request, "pages/LoginComponent/LoginPage.html")

def register(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')

        if password and repassword:
            if password == repassword:
                try:
                    user = User(
                        firstname=firstname,
                        lastname=lastname,
                        username=username,
                        password=password  
                    )
                    user.save()
                    messages.success(request, "Registration successful!")
                    return redirect('login_page')
                except Exception as e:
                    messages.error(request, "Registration failed. Try again.")
            else:
                messages.error(request, "Passwords do not match.")
        else:
            messages.error(request, "Please fill in all required fields.")
    return render(request, "pages/LoginComponent/RegisterPage.html", {})

def reservation_page(request):
    return render(request, 'pages/ReservationComponent/ReservationPage.html') 

def viewall_reservations(request):
    messages.get_messages(request).used = True
    user = User.objects.get(id=request.session['user_id'])
    if user.role != 'Admin':
        messages.error(request, "User not authorized!")
    return render(request, 'pages/ReservationComponent/ReservationViewAll.html', {'user': user})

def modify_reservation(request):
    return render(request, "pages/ViewReservationsPage.html")

def search_reservation(request):
    return render(request, "pages/ReservationComponent/ReservationSearch.html")


def custom_logout(request):
    if messages.get_messages(request):
        messages.get_messages(request).used = True
    
    logout(request)
    messages.success(request, "You have logged out successfully.")
    return redirect('login_page')  