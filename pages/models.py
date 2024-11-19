from django.db import models
from django.contrib.auth.models import User
import datetime


class ResUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phonenumber = models.CharField(default="000-000-0000", max_length=12)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - Phone {self.phonenumber}"


class Reservation(models.Model):
    tablenum = models.IntegerField(default=1)
    date = models.DateField(default=datetime.date.today)
    firstname = models.CharField(max_length=100, blank=True)
    lastname = models.CharField(max_length=100, blank=True)
    time = models.TimeField(default=datetime.time(19, 0))
    reservedBy = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('tablenum', 'date', 'time')

    def __str__(self):
        status = "Available" if self.reservedBy is None else "Reserved"
        return f"Reservation for Table {self.tablenum} on {self.date} at {self.time} - {status}"
