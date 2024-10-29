# pages/urls.py

from django.urls import path
from pages import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page at the root URL
    path('reservation/', views.reservation_page, name='reservation_page'),  # Reservation page
]
