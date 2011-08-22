from django.contrib.auth.models import User
from django.db import models
from account.models import UserProfile
from battle.models import Battle
from location.models import Location

class Checkin(models.Model):
    user = models.ForeignKey(UserProfile)
    location = models.ForeignKey(Location)

    battle = models.ForeignKey(Battle, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)