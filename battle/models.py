from django.db import models
from django.utils.datetime_safe import datetime
from account.models import UserProfile
from location.models import Location


class Battle(models.Model):
    attacker = models.ForeignKey(UserProfile, related_name="attacking_battles")
    defender = models.ForeignKey(UserProfile, related_name="defending_battles")

    active = models.BooleanField(default=True)
    start_time = models.DateTimeField(default=datetime.now())

    winner = models.ForeignKey(UserProfile, null=True)