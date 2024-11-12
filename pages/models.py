from django.db import models
import datetime

class User(models.Model):
    firstname = models.CharField(max_length=255, default="John") 
    lastname = models.CharField(max_length=255, default="Doe")    
    username = models.CharField(max_length=150, unique=True,  default="Admin") 
    password = models.CharField(max_length=128,default = "123")  
    reservationtime = models.TimeField(default=datetime.time(19, 0))  
    reservationdate = models.DateField(default=datetime.date(2024, 11, 1)) 
    role = models.CharField(max_length=100, default="Guest")  
    tablenumber = models.IntegerField(default=1)  

    def __str__(self):
        return f"{self.firstname} {self.lastname} - Table {self.tablenumber}"

class Reservation(models.Model):
    # we can change below fields if they don't make sense, but just to have them in there
    tablenum = models.IntegerField(default=1)
    date = models.DateField(default=datetime.date(2024, 11, 1))
    time = models.TimeField(default=datetime.time(19, 0))
    available = models.BooleanField(default=True)
    # looked up below line; don't know if this is how to correctly refer to instance of the table being reserved by a user
    reservedBy = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL)

    class Meta:
        # this forces the reservations made to be inherently unique: there cannot be a reservation made if the specific table has already been reserved for a certain date and time
        unique_together = ('tablenum', 'date', 'time')  # might need to figure out how to make 'time' a range - depends on how we use 'time' in our system; can a guest reserve a table one minute after it's been reserved by someone else?
    def __str__(self):
        return f"Reservation for Table {self.tablenum} on {self.date} at {self.time} - {'Available' if self.available else 'Reserved'}"