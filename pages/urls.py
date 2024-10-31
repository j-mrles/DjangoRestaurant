# pages/urls.py

from django.urls import path
from pages import views

urlpatterns = [
    path('', views.login, name='login_page'),
    path('home/', views.home, name='home'),  # Home page at the root URL
    path('reservation/', views.reservation_page, name='reservation_page'),  # Reservation page
    path('reservations/<int:id>/modify/', views.modify_reservation, name='modify_reservation'), # Customer modify reservation
    path('register/', views.register, name="registration_page"),
    path('search/', views.search_reservation, name="search_page")
]