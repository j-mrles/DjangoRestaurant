from django.db import models

# Create your models here.
class User(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)

class Reservation(models.Model):
  # below fields can change if we need, not set in stone right now
  tablenum = models.IntegerField()
  date = models.DateField()
  time = models.TimeField()
  available = models.BooleanField(default=True)
  # looked up below line; don't know if this is how to correctly refer to instance of the table being reserved by a user
  reservedBy = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL)