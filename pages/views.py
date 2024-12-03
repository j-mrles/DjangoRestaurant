from django.shortcuts import render, redirect 
from django.contrib.auth.models import User
from .models import Reservation
from .models import ResUser
from django.contrib.auth import logout, authenticate
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q
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
    context = {}

    # Authenticate user for role-specific UI elements
    today, tablenumber, restime, resdate = str(date.today()), request.GET.get('tablenumber'), request.GET.get('restime'), request.GET.get('resdate')
    loggedin, role = 'false', 'user'
    welcomename, firstname, lastname, email, phonenumber, user, reservations = None, None, None, None, None, None, None
    if request.session.has_key('username'): # If user is logged in
        user = User.objects.get(username=request.session.get('username')) # Get the user object from session 'username' field
        # Fill out variables from user account
        firstname, welcomename = user.first_name, user.first_name
        lastname = user.last_name
        email = user.email
        phonenumber = user.resuser.phonenumber
        reservations = Reservation.objects.filter(reservedBy=user)
        # Set login flag and role appropriately for dynamic HTML elements
        loggedin = 'true'
        if user.is_staff:
            role = 'employee'
    else:
        welcomename = "Guest"

    # Update context
    context['welcomename'], context['loggedin'], context['role'], context['reservations'], context['today'], context['tablenumber'], context['restime'], context['resdate'] = welcomename, loggedin, role, reservations, today, tablenumber, restime, resdate

    # If trying to make a reservation
    if request.method == "POST":                                                        
        # Get information for reservation (date, time, table number)
        resdate, restime, tablenumber = date.fromisoformat(request.POST.get('resdate')), time.fromisoformat(request.POST.get('restime')), int(request.POST.get('tablenumber'))

        # Update Context
        context['today'], context['tablenumber'], context['restime'], context['resdate'] = today, tablenumber, restime, resdate

        # Check if date is more than 90 days out
        latestdate = datetime.now() + timedelta(days=90)
        latestdate = latestdate.date()
        if resdate > latestdate:
            messages.error(request, "Please select date on or before " + latestdate.strftime("%B %d, %Y"))
            return render(request, 'pages/ReservationComponent/ReservationPage.html', context)  
        # Check if table is available during that time
        if not tableIsAvailable(tablenumber, resdate, restime):
            # Table is not available
            messages.error(request, "Table is not available!")
            return render(request, 'pages/ReservationComponent/ReservationPage.html', context)  
        
        # Table is available
        # If user isn't logged in, get personal details from form
        if user is None:
            username = str(User.objects.count())
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
                return render(request, 'pages/ReservationComponent/ReservationPage.html', context) 
        try:        
            reservation = Reservation.objects.create(tablenum=tablenumber, date=resdate, time=restime, reservedBy=user)
            reservation.save()
        except:
            messages.error(request, "Error occured while creating reservation")
            return render(request, 'pages/ReservationComponent/ReservationPage.html', context) 
        
        return redirect('confirm_reservation', reservation_id=reservation.id)

    return render(request, 'pages/ReservationComponent/ReservationPage.html', context) 
    

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
            restime = time.fromisoformat(restime)
            reservations = reservations.filter(time=restime)
            context['res_time'] = restime
        if tablenum:
            reservations = reservations.filter(tablenum=tablenum)
            context['tablenum'] = tablenum

        context['reservations'] = reservations

    return render(request, 'pages/ReservationComponent/ReservationViewAll.html', context)

def modify_reservation(request, reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        return redirect('viewall_reservation')
    
    if not request.session.has_key('username'):
        messages.error(request, 'User not authorised!')
        return redirect('home')
    if not User.objects.get(username=request.session.get('username')).is_staff and reservation.reservedBy.username != request.session.get('username'):
        messages.error(request, 'User not authorised!')
        return redirect('home')
    
    success = False
    failure_reason = None
    neutral = False
    is_submitted = False

    if request.method == 'POST':
        is_submitted = True
        new_date = request.POST.get('date') or reservation.date
        new_time = request.POST.get('time') or reservation.time
        new_tablenumber = request.POST.get('tablenum') or reservation.tablenum

        if isinstance(new_date, str):
            new_date = date.fromisoformat(new_date)
        if isinstance(new_time, str):
            new_time = time.fromisoformat(new_time)

        if new_date == reservation.date and new_time == reservation.time and new_tablenumber == reservation.tablenum:
            neutral = True
        elif not tableIsAvailable(int(new_tablenumber), new_date, new_time, res_id=reservation.id):
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
        #'formatted_date': formatted_date,
        #'formatted_time': formatted_time
    })

def checkin_reservation(request, reservation_id):
    # Validate user
    if not request.session.has_key('username'):
        messages.error(request, 'User not authorised!')
        return redirect('home')
    if not User.objects.get(username=request.session.get('username')).is_staff and reservation.reservedBy.username != request.session.get('username'):
        messages.error(request, 'User not authorised!')
        return redirect('home')
    # Validate reservation id
    try:
        reservation = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        messages.error(request, "Reservation does not exist.")
        return redirect('viewall_reservations')

    # Check if user is trying to check in before today
    if reservation.date != datetime.now().date():
        messages.error(request, "Check in cannot be done before reservation date.")
        return redirect('viewall_reservations')
    
    # Check if user has clicked 'Check In' on check in confirmation page
    if request.method == 'POST':
        # Update the checked_in status to True
        reservation.checked_in = True
        reservation.save()
        messages.success(request, f"Reservation for Table {reservation.tablenum} has been checked in.")
        return redirect('viewall_reservations')
    # If user hasn't clicked 'Check In' on the confirmation page, they need to be sent to confirmation page
    return render(request, 'pages/ReservationComponent/CheckinReservation.html', {
        'reservation': reservation
    })

def remove_reservation(request, reservation_id):
    # Validate user
    if not request.session.has_key('username'):
        messages.error(request, 'User not authorised!')
        return redirect('home')
    if not User.objects.get(username=request.session.get('username')).is_staff and reservation.reservedBy.username != request.session.get('username'):
        messages.error(request, 'User not authorised!')
        return redirect('home')
    
    try:
        reservation = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        return redirect('viewall_reservations')
    
    if request.method == 'POST' and 'confirm' in request.POST:  # confirm POST obv but also that confirm was pressed
        if reservation.reservedBy.username.isdigit:
            user = reservation.reservedBy
        reservation.delete() # feels like not enough code to actually do it but we'll see
        if user.username.isdigit():
            user.resuser.delete()
            user.delete()
        return render(request, 'pages/ReservationComponent/RemoveReservation.html', {
            'success': True  # for display stuff
        })    
    return render(request, 'pages/ReservationComponent/RemoveReservation.html', {
        'reservation': reservation,
        'success': False
    })

def confirm_reservation(request, reservation_id):
    # Check if user was not redirected to this page (check if they typed in address themselves)
    if not 'HTTP_REFERER' in request.META:
        messages.error(request,'Page not available!')
        return redirect('home')
    

    try:
        reservation = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        messages.error(request, 'Reservation does not exist!')
        return redirect('reservation_page')
    return render(request, "pages/ReservationComponent/ReservationConfirm.html", {
        'reservation':reservation})

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
    clearmessages(request)

    resdate = request.GET.get('resdate')
    restime = request.GET.get('restime')
    now = datetime.now()

    if resdate == None:
        resdate = now.date()
    else:
        resdate = date.fromisoformat(resdate)
        latestdate = now + timedelta(days=90)
        latestdate = latestdate.date()
        if resdate > latestdate:
            resdate = latestdate
            messages.error(request, "Please select date on or before " + latestdate.strftime("%B %d, %Y"))
        if resdate < now.date():
            resdate = now.date()
            messages.error(request, "Please select date on or after " + now.date().strftime("%B %d, %Y"))
    if restime == None:
        restime = now + (datetime.min - now) % timedelta(minutes=30)
        restime = restime.time()
        if restime < time(hour=16):
            restime = time(hour=16)
        if restime > time(hour=22):
            restime = time(hour=16)
            resdate = resdate + timedelta(days=1)
    else:
        restime = time.fromisoformat(restime)

    availability = tableAvailability(resdate, restime)
    tables = [
        {"number": 1, "capacity": 2, "availability": 'Available' if availability[0] else 'Unavailable'},
        {"number": 2, "capacity": 2, "availability": 'Available' if availability[1] else 'Unavailable'},
        {"number": 3, "capacity": 4, "availability": 'Available' if availability[2] else 'Unavailable'},
        {"number": 4, "capacity": 8, "availability": 'Available' if availability[3] else 'Unavailable'},
        {"number": 5, "capacity": 8, "availability": 'Available' if availability[4] else 'Unavailable'},
        {"number": 6, "capacity": 2, "availability": 'Available' if availability[5] else 'Unavailable'},
        {"number": 7, "capacity": 4, "availability": 'Available' if availability[6] else 'Unavailable'},
        {"number": 8, "capacity": 6, "availability": 'Available' if availability[7] else 'Unavailable'},
        {"number": 9, "capacity": 4, "availability": 'Available' if availability[8] else 'Unavailable'},
        {"number": 10, "capacity": 4, "availability": 'Available' if availability[9] else 'Unavailable'},
        {"number": 11, "capacity": 4, "availability": 'Available' if availability[10] else 'Unavailable'},
        {"number": 12, "capacity": 6, "availability": 'Available' if availability[11] else 'Unavailable'},
        {"number": 13, "capacity": 6, "availability": 'Available' if availability[12] else 'Unavailable'},
        {"number": 14, "capacity": 12, "availability": 'Available' if availability[13] else 'Unavailable'},
        {"number": 15, "capacity": 2, "availability": 'Available' if availability[14] else 'Unavailable'},
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


def tableAvailability(resdate, restime, res_id=None):
    if restime.hour == 22:
        resendtime = restime.replace(hour=23, minute=59, second=59)
    else:
        #print(restime)
        resendtime = restime.replace(hour=restime.hour+2)

    reservations = Reservation.objects.all()

    reservations = reservations.filter(date=resdate)
    if isinstance(res_id, int):
        reservations = reservations.exclude(id=res_id)

    tables = [True] * 15

    for reservation in reservations:
        if reservation.time.hour >= 22:
            endtime = reservation.time.replace(hour=23, minute=59, second = 59)
        else:
            #print(reservation.time)
            endtime = reservation.time.replace(hour=reservation.time.hour+2)
        
        #print(resdate, reservation.date, restime, reservation.time, endtime, reservation.tablenum)
        if reservation.time <= restime < endtime or reservation.time < resendtime <= endtime: 
           tables[reservation.tablenum-1] = False
    
    print(tables)
    return tables

def tableIsAvailable(tablenum, resdate, restime, res_id=None):
    return tableAvailability(resdate, restime, res_id=res_id)[tablenum-1]

def clearmessages(request):
    for message in messages.get_messages(request):
        message.used = True