from django.db import models
from alliance.models import Alliance
from location.models import Location

class Battle(models.Model):
    attacker = models.ForeignKey(Alliance, related_name="attacking_battles")
    defender = models.ForeignKey(Alliance, related_name="defending_battles")

    active = models.BooleanField(default=True)
    start_time = models.DateTimeField()
    capital = models.ForeignKey(Location)

    winner = models.ForeignKey(Alliance, null=True)