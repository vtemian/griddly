from django.db import models
from account.models import UserProfile

class Location(models.Model):
    name = models.CharField(max_length=30)
    lat = models.FloatField(max_length=30)
    lng = models.FloatField(max_length=30)

    territory = models.ForeignKey("territory.Territory", related_name="locations", null=True)
    
    subscription = models.FloatField(max_length=20, default=1)

class Loyalty(models.Model):
    value = models.IntegerField(default=0, max_length=30)
    location = models.ForeignKey(Location)
    userProfile = models.ForeignKey(UserProfile)
    active = models.BooleanField(default=True)