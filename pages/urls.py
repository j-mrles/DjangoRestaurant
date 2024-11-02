from django.urls import path
from pages import views

urlpatterns = [
    path('', views.login, name='login_page'),
    path('home/', views.home, name='home'),  
    path('reservation/', views.reservation_page, name='reservation_page'), 
    path('reservations/<int:id>/modify/', views.modify_reservation, name='modify_reservation'), 
    path('register/', views.register, name="register_user"),
    path('search/', views.search_reservation, name="search_page"),
    path('registration/', views.register, name='registration_page') 
]