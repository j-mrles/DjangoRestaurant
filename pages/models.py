from django.db import models
from django.contrib.auth.models import User
import datetime

class ResUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phonenumber = models.CharField(default="000-000-0000", max_length=12)

    def __str__(self):
        return f"{self.firstname} {self.lastname} - Table {self.tablenumber}"

class Reservation(models.Model):
    # we can change below fields if they don't make sense, but just to have them in there
    tablenum = models.IntegerField(default=1)
    date = models.DateField(default=datetime.date(2024, 11, 1))
    starttime = models.TimeField(default=datetime.time(19, 0))
    # looked up below line; don't know if this is how to correctly refer to instance of the table being reserved by a user
    reservedBy = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL)

    class Meta:
        # this forces the reservations made to be inherently unique: there cannot be a reservation made if the specific table has already been reserved for a certain date and time
        unique_together = ('tablenum', 'date', 'starttime')  # might need to figure out how to make 'time' a range - depends on how we use 'time' in our system; can a guest reserve a table one minute after it's been reserved by someone else?
    def __str__(self):
        return f"Reservation for Table {self.tablenum} on {self.date} at {self.time} - {'Available' if self.available else 'Reserved'}"