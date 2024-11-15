from django.shortcuts import render, redirect 
from django.contrib.auth.models import User
from .models import Reservation
from .models import ResUser
from django.contrib.auth import logout, authenticate
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q
import random

def home(request):
    loggedin = 'false'
    role = 'user'
    if request.session.has_key('username'):
        loggedin = 'true'
        if User.objects.get(username=request.session.get('username')).is_staff:
            role = 'employee'
    return render(request, 'pages/LoginComponent/HomePage.html', {
        'loggedin' : loggedin,
        'role': role
        })  

def login(request):
    messages.get_messages(request).used = True                              # clear any messages in request
    if request.method == "POST":                                            # If the request is someone clicking a form button
        # Get the form data (For login, just username and password)
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:                                           # If both fields are NOT empty
            user = authenticate(username=username , password=password)      # Authenticate user
            if user is not None:                                            # If user is found
                request.session['user_id'] = user.id
                # consider below -> remove if doesn't work
                request.session['username'] = username
                messages.success(request, "You are logged in successfully!")
                return redirect('reservation_page')
            else:                                                           # If user is NOT found
                messages.error(request, "Invalid username or password")
        else:                                                               # If one or both fields are empty
            messages.error(request, "Please enter both username and password")
    return render(request, "pages/LoginComponent/LoginPage.html")

def register(request):
    # Clear any messages in the request
    messages.get_messages(request).used = True
    if request.method == "POST":
        # Get form data
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        phonenumber = request.POST.get('phone')
        username = request.POST.get('username')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')

        if password and repassword:                                         # If password and repassword are not blank
            if password == repassword:                                      # If password and repassword match
                try:
                    user = User.objects.create_user(username, email, password, first_name = firstname, last_name = lastname)    # Create user object with provided data and save it
                    user.save()
                    resuser = ResUser.objects.create(phonenumber=phonenumber, user=user)                                        # Create resuser object to store phone number and save it
                    resuser.save()
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
    messages.get_messages(request).used = True                               # Clear any messages
    
    # Authenticate user for role-specific UI elements
    loggedin = 'false'
    role = 'user'
    firstname = None
    if request.session.has_key('username'):
        user = User.objects.get(username=request.session.get('username'))
        firstname = user.first_name
        loggedin = 'true'
        if user.is_staff:
            role = 'employee'
    else:
        firstname = "Guest"

    return render(request, 'pages/ReservationComponent/ReservationPage.html', {
        'firstname': firstname,
        'loggedin': loggedin,
        'role': role,
    }) 

def viewall_reservations(request):
    messages.get_messages(request).used = True
    reservations = Reservation.objects.all()
    try:
        user = User.objects.get(username=request.session.get('username'))
        if not user.is_staff:
            messages.error(request, "User not authorized!")
    except:
        messages.error(request, "User not authorized!")
    return render(request, 'pages/ReservationComponent/ReservationViewAll.html', {'reservations' : reservations})

def modify_reservation(request):
    return render(request, "pages/ViewReservationsPage.html")

def search_reservation(request):
    # do search database stuff here :D

    reservations = []

    if request.method == "GET":
        first_name = request.GET.get('search-by-firstname','')
        last_name = request.GET.get('search-by-lastname','')
        date = request.GET.get('search-by-resdate','')
        time = request.GET.get('search-by-restime','')
        tablenum = request.GET.get('search-by-tablenum','')
        # available = request.GET.get('search-by-availability','')
        # reserved_by = request.GET.get('search-by-reservedby','')  # this is a little janky
        
        if first_name or last_name or date or time or tablenum:
            reservations = Reservation.objects.all()

            if first_name:
                reservations = reservations.filter(reservedBy__firstname__icontains=first_name)
            if last_name:
                reservations = reservations.filter(reservedBy__lastname__icontains=last_name)
            if date:
                reservations = reservations.filter(date=date)
            if time:
                reservations = reservations.filter(time=time)
            if tablenum:
                reservations = reservations.filter(tablenum=tablenum)
            # if available:
            # if reserved_by:

    return render(request, "pages/ReservationComponent/ReservationSearch.html", {
        'reservations':reservations,
        'firstname': first_name,
        'lastname' : last_name,
        'date' : date,
        'time' : time,
        'tablenum' : tablenum
    })


def custom_logout(request):
    if messages.get_messages(request):
        messages.get_messages(request).used = True
    
    logout(request)
    messages.success(request, "You have logged out successfully.")
    return redirect('login_page')  

def table_statuses(request):
    tables = [
        {
            "number": i + 1,
            # placeholder data for each table's capacity
            "capacity": random.choice([2, 4, 6]), 
            # can adjust weights(%) for which is more frequent, available is occuring more
            "availability": random.choices(["Available", "Reserved"], weights=[75, 15])[0]
        }
        # placeholder data for a total of 10 tables
        for i in range(10)  
    ]

    selected_table = request.GET.get('tablenumber', '')

    return render(request, 'pages/ReservationComponent/TableStatuses.html', {
        "tables": tables,
        # pass selected table to the template
        "selected_table": selected_table,  
    })