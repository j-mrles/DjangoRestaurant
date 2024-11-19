from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Reservation
from .models import ResUser
from django.contrib.auth import logout, authenticate
from django.contrib import messages
from django.db.models import Q
import random
from datetime import datetime, timedelta

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
    messages.get_messages(request).used = True  # Clear any messages in request
    if request.method == "POST":  # If the request is someone clicking a form button
        # Get the form data (For login, just username and password)
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:  # If both fields are NOT empty
            user = authenticate(username=username, password=password)  # Authenticate user
            if user is not None:  # If user is found
                request.session['user_id'] = user.id
                request.session['username'] = username
                messages.success(request, "You are logged in successfully!")
                return redirect('reservation_page')
            else:  # If user is NOT found
                messages.error(request, "Invalid username or password")
        else:  # If one or both fields are empty
            messages.error(request, "Please enter both username and password")
    return render(request, "pages/LoginComponent/LoginPage.html")

def register(request):
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

        if password and repassword:  # If password and repassword are not blank
            if password == repassword:  # If password and repassword match
                try:
                    user = User.objects.create_user(username, email, password, first_name=firstname, last_name=lastname)
                    user.save()
                    resuser = ResUser.objects.create(phonenumber=phonenumber, user=user)
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
    messages.get_messages(request).used = True  # Clear any messages
    
    # Authenticate user for role-specific UI elements
    loggedin = 'false'
    role = 'user'
    firstname, lastname, email, phonenumber, user = None, None, None, None, None
    if 'username' in request.session:  # If user is logged in
        user = User.objects.get(username=request.session['username'])  # Get the user object from session 'username' field
        # Fill out variables from user account
        firstname = user.first_name
        lastname = user.last_name
        email = user.email
        phonenumber = user.resuser.phonenumber
        # Set login flag and role appropriately for dynamic HTML elements
        loggedin = 'true'
        if user.is_staff:
            role = 'employee'
    else:
        firstname = "Guest"
        lastname = ""
        email = ""
        phonenumber = ""

    if request.method == "POST":
        # If user isn't logged in, get personal details from form
        if user is None:
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            email = request.POST.get('email')
            phonenumber = request.POST.get('phone')
            
            try:
                user = User.objects.create(first_name=firstname, last_name=lastname, email=email)
                user.save()
                resuser = ResUser.objects.create(phonenumber=phonenumber, user=user)
                resuser.save()
                
            except:
                messages.error(request, "Error occurred while creating reservation")

        date = datetime.strptime(request.POST.get('resdate'), "%Y-%m-%d")
        time = datetime.strptime(request.POST.get('restime'), "%H:%M")
        tablenumber = request.POST.get('tablenumber')
        reservation = Reservation.objects.create(tablenum=tablenumber, date=date, time=time, reservedBy=user)
        reservation.save()
        return redirect('home')

    return render(request, 'pages/ReservationComponent/ReservationPage.html', {
        'firstname': firstname,
        'lastname': lastname,
        'email': email,
        'phonenumber': phonenumber,
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
    # Fetch all reservations initially
    reservations = Reservation.objects.all()

    # Extract search parameters from the GET request
    firstname = request.GET.get('firstname', '')
    lastname = request.GET.get('lastname', '')
    resdate = request.GET.get('resdate', '')
    restime = request.GET.get('restime', '')
    tablenum = request.GET.get('tablenum', '')

    # Print the search parameters to see what is being passed
    print(f"Search Parameters: firstname={firstname}, lastname={lastname}, resdate={resdate}, restime={restime}, tablenum={tablenum}")

    # Apply filters based on input
    if firstname:
        print(f"Filtering by firstname: {firstname}")
        reservations = reservations.filter(reservedBy__first_name__icontains=firstname)
    if lastname:
        print(f"Filtering by lastname: {lastname}")
        reservations = reservations.filter(reservedBy__last_name__icontains=lastname)
    if resdate:
        print(f"Filtering by resdate: {resdate}")
        reservations = reservations.filter(date=resdate)
    if restime:
        print(f"Filtering by restime: {restime}")
        reservations = reservations.filter(time=restime)
    if tablenum:
        print(f"Filtering by tablenum: {tablenum}")
        reservations = reservations.filter(tablenum=tablenum)

    # Print the final filtered queryset
    print(f"Filtered reservations: {reservations}")

    # Pass the results and search terms to the template
    return render(request, "pages/ReservationComponent/ReservationSearch.html", {    
        'reservations': reservations,
        'firstname': firstname,
        'lastname': lastname,
        'resdate': resdate,
        'restime': restime,
        'tablenum': tablenum
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
            "capacity": random.choice([2, 4, 6]),  # placeholder data for each table's capacity
            "availability": random.choices(["Available", "Reserved"], weights=[75, 15])[0]  # Random availability
        }
        for i in range(10)  # placeholder data for a total of 10 tables
    ]

    selected_table = request.GET.get('tablenumber', '')

    return render(request, 'pages/ReservationComponent/TableStatuses.html', {
        "tables": tables,
        "selected_table": selected_table,  
    })

def tableAvailability(date, time):
    reservations = Reservation.objects.all()
    reservations.filter(date=date)
    tables = [True] * 15

    for reservation in reservations:
        if reservation.time < time < reservation.time + timedelta(minutes=120):
            tables[reservation.tablenum-1] = False

    return tables
