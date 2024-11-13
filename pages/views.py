from django.shortcuts import render, redirect 
from .models import User
from .models import Reservation
from .models import Makes
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q
import datetime

from django.contrib import messages
import logging

logger = logging.getLogger(__name__)

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
                    logger.error(f"Registration failed: {str(e)}")  # Log the error
                    messages.error(request, "Registration failed. Try again.")
            else:
                messages.error(request, "Passwords do not match.")
        else:
            messages.error(request, "Please fill in all required fields.")
    return render(request, "pages/LoginComponent/RegisterPage.html", {})

def reservation_page(request):
    
    # gabe's added code for making a reservation #
    
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        resdate = request.POST.get('resdate')
        restime = request.POST.get('restime')
        tablenumber = request.POST.get('tablenum')

        reservation_date = datetime.datetime.strptime(resdate, '%Y-%m-%d').date()
        reservation_time = datetime.datetime.strptime(restime, '%H:%M').time()

        existingReservation = Reservation.objects.filter(
            tablenum=tablenumber,
            date=reservation_date,
            time=reservation_time
        ).first()

        # if the reservation already exists / there's already a reservation for the request time
        if existingReservation and not existingReservation.available:
            return render(request, 'pages/ReservationComponent/ReservationPage.html', {
                'Error': f"Table {tablenumber} is already reserved for {reservation_date} at {reservation_time}."
            })

        # make the reservation if it is possible (doesn't already exist/date and time available)
        reservation = Reservation(
            tablenum=tablenumber,
            date=reservation_date,
            time=reservation_time,
            available=False,
        )
        reservation.save()
        
        # same as in my welcome user ticket, we'll probably need to add a user id
        username = request.POST.get('username')
        user = User.objects.get(username=username)

        if user:
            Makes.objects.create(user=user, reservation=reservation)
        else:
            return render(request, 'pages/ReservationComponent/ReservationPage.html', {
                'Error': "The user entered was not found, please log in or provide a valid username"
            })
            
        successMessage = f"Reservation for Table {tablenumber} on {reservation_date} at {reservation_time} has been successfully made."
        
        return render(request, 'pages/ReservationComponent/ReservationPage.html', {
            'successMessage' : successMessage
        })
        # we can do below redirect when we make a successful, confirmed reservation page
        # return redirect('reservation_confirmation')
    return render(request, 'pages/ReservationComponent/ReservationPage.html')
    # ------------------------------------------ #

def viewall_reservations(request):
    messages.get_messages(request).used = True
    user = User.objects.get(id=request.session['user_id'])
    reservations = Reservation.objects.all()
    if user.role != 'Admin':
        messages.error(request, "User not authorized!")
    return render(request, 'pages/ReservationComponent/ReservationViewAll.html', {'user': user, 'reservations' : reservations})

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
        'reservations':reservations
    })


def custom_logout(request):
    if messages.get_messages(request):
        messages.get_messages(request).used = True
    
    logout(request)
    messages.success(request, "You have logged out successfully.")
    return redirect('login_page')  