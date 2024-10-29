from django.shortcuts import render

def home(request):
    return render(request, "pages/home.html", {})
def reservation_page(request):
    return render(request, 'pages/ReservationPage.html')  
