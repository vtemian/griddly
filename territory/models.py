from django.db import models
from Items.models import Defends
from account.models import UserProfile
from location.models import Location


class Territory(models.Model):
    owner = models.OneToOneField(UserProfile)
    defense = models.IntegerField(max_length=6, null=True)

    capital = models.OneToOneField(Location, related_name='capital_territory')
    
    price = models.IntegerField(max_length=6)
    area = models.IntegerField(max_length=6)