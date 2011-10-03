from django.db import models
from Items.models import Defends
from account.models import UserProfile
from location.models import Location

class Points(models.Model):
    lat = models.CharField(max_length=30)
    lng = models.CharField(max_length=30)
    
class Territory(models.Model):
    defense = models.IntegerField(max_length=6, null=True)

    name = models.CharField(max_length=50, null=True)
    price = models.IntegerField(max_length=6)
    area = models.IntegerField(max_length=6)
    
    points = models.ManyToManyField(Points, null=True)

    owner = models.ForeignKey(UserProfile)

    lvl = models.IntegerField(default=1)

    color = models.CharField(max_length=50, default="#ffe019")