from django.contrib.auth import views as auth_views
from django.urls import path
from pages import views
from .views import custom_logout  

urlpatterns = [
    path('', views.login, name='login_page'),
    path('home/', views.home, name='home'),  
    path('reservation/', views.reservation_page, name='reservation_page'), 
    path('reservation/viewall', views.viewall_reservations, name='viewall_reservations'),
    path('reservations/<int:id>/modify/', views.modify_reservation, name='modify_reservation'), 
    path('register/', views.register, name="register_user"),
    path('search/', views.search_reservation, name="search_page"),
    path('registration/', views.register, name='registration_page'),
    path('logout/', custom_logout, name='logout'), 
]