from django.db import models
import datetime

class User(models.Model):
    firstname = models.CharField(max_length=255, default="John") 
    lastname = models.CharField(max_length=255, default="Doe")    
    reservationtime = models.TimeField(default=datetime.time(19, 0))  
    reservationdate = models.DateField(default=datetime.date(2024, 11, 1)) 
    role = models.CharField(max_length=100, default="Guest")  
    tablenumber = models.IntegerField(default=1)  

    def __str__(self):
        return f"{self.firstname} {self.lastname} - Table {self.tablenumber}"
