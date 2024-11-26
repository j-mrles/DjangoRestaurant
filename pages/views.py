from django.shortcuts import render, redirect 
from django.contrib.auth.models import User
from .models import Reservation
from .models import ResUser
from django.contrib.auth import logout, authenticate
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q
import random
from datetime import datetime, date, time, timedelta

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
    clearmessages(request)                              # clear any messages in request
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
    clearmessages(request)
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
    clearmessages(request)                               # Clear any messages
    
    # Authenticate user for role-specific UI elements
    today = str(date.today())
    tablenumber = request.GET.get('tablenumber')
    loggedin = 'false'
    role = 'user'
    reservations = None
    firstname, lastname, email, phonenumber, user = None, None, None, None, None
    if request.session.has_key('username'): # If user is logged in
        user = User.objects.get(username=request.session.get('username')) # Get the user object from session 'username' field
        # Fill out variables from user account
        firstname = user.first_name
        lastname = user.last_name
        email = user.email
        phonenumber = user.resuser.phonenumber
        reservations = Reservation.objects.filter(reservedBy=user)
        # Set login flag and role appropriately for dynamic HTML elements
        loggedin = 'true'
        if user.is_staff:
            role = 'employee'
    else:
        firstname = "Guest"


    if request.method == "POST":                                                        # If trying to make a reservation
        # Get information for reservation (date, time, table number)
        resdate = date.fromisoformat(request.POST.get('resdate'))
        restime = time.fromisoformat(request.POST.get('restime')+":00")
        tablenumber = int(request.POST.get('tablenumber'))
        # Check if table is available during that time
        if not tableIsAvailable(tablenumber, resdate, restime):
            # Table is not available
            messages.error(request, "Table is not available!")
            return render(request, 'pages/ReservationComponent/ReservationPage.html', {
                'firstname': firstname,
                'loggedin': loggedin,
                'role': role,
                'reservations': reservations,
             })  
        # Table is available
        # If user isn't logged in, get personal details from form
        if user is None:
            username = f"guest_{User.objects.count()}"

            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            email = request.POST.get('email')
            phonenumber = request.POST.get('phone')
            
        try:
            user = User.objects.create(first_name=firstname, last_name=lastname, email=email, username=username)
            user.save()
            resuser = ResUser.objects.create(phonenumber=phonenumber, user=user)
            resuser.save()
        except:
            messages.error(request, "Error occured while saving guest data for reservation")

        try:        
            reservation = Reservation.objects.create(tablenum=tablenumber, date=resdate, time=restime, reservedBy=user)
            reservation.save()
        except:
            messages.error(request, "Error occured while creating reservation")
            return redirect('reservation_page')
        return redirect('confirm_reservation', reservation_id=reservation.id)

    return render(request, 'pages/ReservationComponent/ReservationPage.html', {
        'firstname': firstname,
        'loggedin': loggedin,
        'role': role,
        'reservations': reservations,
        'today': today,
        'tablenumber': tablenumber
    }) 
    

def viewall_reservations(request):
    clearmessages(request)
    try:
        user = User.objects.get(username=request.session.get('username'))
        if not user.is_staff:
            messages.error(request, "User not authorized!")
            return render(request, 'pages/ReservationComponent/ReservationViewAll.html', {
                'reservations': [],
            })
    except User.DoesNotExist:
        messages.error(request, "User not authorized!")
        return render(request, 'pages/ReservationComponent/ReservationViewAll.html', {
            'reservations' : []
        })
    
    reservations = Reservation.objects.all()
    context = {'reservations': reservations}

    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        resdate = request.POST.get('res_date')
        restime = request.POST.get('res_time')
        tablenum = request.POST.get('tablenum')

        if firstname:
            reservations = reservations.filter(reservedBy__first_name__iexact=firstname)
            context['firstname'] = firstname
        if lastname:
            reservations = reservations.filter(reservedBy__last_name__iexact=lastname)
            context['lastname'] = lastname
        if resdate:
            resdate = date.fromisoformat(resdate)
            reservations = reservations.filter(date=resdate)
            context['res_date'] = resdate
        if restime:
            restime = time.fromisoformat(restime+":00")
            reservations = reservations.filter(time=restime)
            context['res_time'] = restime
        if tablenum:
            reservations = reservations.filter(tablenum=tablenum)
            context['tablenum'] = tablenum

        context['reservations'] = reservations

    return render(request, 'pages/ReservationComponent/ReservationViewAll.html', context)

# def modify_reservation(request):
#     return render(request, "pages/ViewReservationsPage.html")

def modify_reservation(request, reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        return redirect('viewall_reservation')
    
    success = False
    failure_reason = None
    neutral = False
    is_submitted = False

    if request.method == 'POST':
        is_submitted = True
        new_date = request.POST.get('date') or reservation.date
        new_time = request.POST.get('time') or reservation.time
        new_tablenumber = request.POST.get('tablenum') or reservation.tablenum

        if new_date == reservation.date and new_time == reservation.time and new_tablenumber == reservation.tablenum:
            neutral = True
        elif not tableIsAvailable(int(new_tablenumber), new_date, new_time):
            success = False
            failure_reason = f"Table {new_tablenumber} is already reserved at {new_date} {new_time}"
        else:
            reservation.date = new_date
            reservation.time = new_time
            reservation.tablenum = new_tablenumber
            reservation.save()
            success = True
        
        # someone can try and fix if they want; think this can be done with datetime but ugh
        # formatted_date = reservation.date.strftime("%B %d, %Y")
        # formatted_time = reservation.time.strftime("%I:%M %p")

    return render(request, 'pages/ReservationComponent/ModifyReservation.html', {
        'reservation': reservation,
        'reservation_id': reservation_id,
        'success': success if is_submitted else None,
        'neutral': neutral if is_submitted else None,
        'failure_reason': failure_reason if is_submitted else None,
        # 'formatted_date': formatted_date,
        # 'formatted_time': formatted_time
    })

def checkin_reservation(request, reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        messages.error(request, "Reservation does not exist.")
        return redirect('viewall_reservation')

    if request.method == 'POST':
        # Update the checked_in status to True
        reservation.checked_in = True
        reservation.save()
        messages.success(request, f"Reservation for Table {reservation.tablenum} has been checked in.")
        return redirect('viewall_reservation')

    return render(request, 'pages/ReservationComponent/CheckinReservation.html', {
        'reservation': reservation
    })

def remove_reservation(request, reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        return redirect('viewall_reservation')
    
    if request.method == 'POST' and 'confirm' in request.POST:  # confirm POST obv but also that confirm was pressed
        reservation.delete() # feels like not enough code to actually do it but we'll see
        return render(request, 'pages/ReservationComponent/RemoveReservation.html', {
            'success': True  # for display stuff
        })    
    return render(request, 'pages/ReservationComponent/RemoveReservation.html', {
        'reservation': reservation,
        'success': False
    })

def confirm_reservation(request, reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        return redirect('reservation_page')
    return render(request, "pages/ReservationComponent/ReservationConfirm.html", {
        'reservation':reservation})

'''
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
'''
def search_reservation(request):
    email = request.GET.get('search-by-email')
    phone = request.GET.get('search-by-phone')
    reservations = None

    if email and phone:
        try:
            user = User.objects.get(email=email)
            reservations = Reservation.objects.filter(reservedBy=user, reservedBy__resuser__phonenumber=phone)
        except User.DoesNotExist:
            reservations = None
    else:
        reservations = None
    
    return render(request, 'pages/ReservationComponent/ReservationSearch.html', {
        'reservations': reservations,
        'email': email,
        'phone': phone,
    })

def custom_logout(request):
    clearmessages(request)
    
    logout(request)
    messages.success(request, "You have logged out successfully.")
    # i think we should return to the home page after logging out, because if we don't, then there's no way to get back to the homescreen and continue as a guest
    return redirect('home')  # redirect('login_page')  

def table_statuses(request):

    resdate = request.GET.get('resdate')
    restime = request.GET.get('restime')
    now = datetime.now()

    if resdate == None:
        resdate = date(day=now.day, month=now.month, year=now.year)
    else:
        resdate = date.fromisoformat(resdate)
    if restime == None:
        restime = now + (datetime.min - now) % timedelta(minutes=30)
        restime = restime.time()
        if restime < time(hour=16):
            restime = time(hour=16)
        if restime > time(hour=22):
            restime = time(hour=16)
            resdate = resdate + timedelta(days=1)
    else:
        restime = time.fromisoformat(restime + ":00")

    availability = tableAvailability(resdate, restime)
    tables = [
        {"number": 1, "capacity": 2, "availability": 'Available' if availability[0] else 'Unavailable'},
        {"number": 2, "capacity": 2, "availability": 'Available' if availability[1] else 'Unavailable'},
        {"number": 3, "capacity": 2, "availability": 'Available' if availability[2] else 'Unavailable'},
        {"number": 4, "capacity": 2, "availability": 'Available' if availability[3] else 'Unavailable'},
        {"number": 5, "capacity": 4, "availability": 'Available' if availability[4] else 'Unavailable'},
        {"number": 6, "capacity": 4, "availability": 'Available' if availability[5] else 'Unavailable'},
        {"number": 7, "capacity": 4, "availability": 'Available' if availability[6] else 'Unavailable'},
        {"number": 8, "capacity": 4, "availability": 'Available' if availability[7] else 'Unavailable'},
        {"number": 9, "capacity": 4, "availability": 'Available' if availability[8] else 'Unavailable'},
        {"number": 10, "capacity": 6, "availability": 'Available' if availability[9] else 'Unavailable'},
        {"number": 11, "capacity": 6, "availability": 'Available' if availability[10] else 'Unavailable'},
        {"number": 12, "capacity": 6, "availability": 'Available' if availability[11] else 'Unavailable'},
        {"number": 13, "capacity": 8, "availability": 'Available' if availability[12] else 'Unavailable'},
        {"number": 14, "capacity": 8, "availability": 'Available' if availability[13] else 'Unavailable'},
        {"number": 15, "capacity": 12, "availability": 'Available' if availability[14] else 'Unavailable'},
    ]

    selected_table = request.GET.get('tablenumber', '')

    return render(request, 'pages/ReservationComponent/TableStatuses.html', {
        'time': str(restime),
        'urltime': str(restime).replace(':', '%3A'),
        'date': str(resdate),
        "tables": tables,
        # pass selected table to the template
        "selected_table": selected_table,  
    })


def tableAvailability(resdate, restime):
    if restime.hour == 22:
        resendtime = restime.replace(hour=23, minute=59, second=59)
    else:
        #print(restime)
        resendtime = restime.replace(hour=restime.hour+2)

    reservations = Reservation.objects.all()

    reservations = reservations.filter(date=resdate)

    tables = [True] * 15

    for reservation in reservations:
        if reservation.time.hour >= 22:
            endtime = reservation.time.replace(hour=23, minute=59, second = 59)
        else:
            #print(reservation.time)
            endtime = reservation.time.replace(hour=reservation.time.hour+2)
        
        #print(resdate, reservation.date, restime, reservation.time, endtime, reservation.tablenum)
        if reservation.time < restime < endtime or reservation.time < resendtime < endtime: 
           tables[reservation.tablenum-1] = False
    
    print(tables)
    return tables

def tableIsAvailable(tablenum, resdate, restime):
    return tableAvailability(resdate, restime)[tablenum-1]

def clearmessages(request):
    for message in messages.get_messages(request):
        message.used = True