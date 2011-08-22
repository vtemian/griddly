from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    money = models.IntegerField(null=True, default=10)
    exp = models.IntegerField(null=True, default=0)
    lvl = models.IntegerField(default=1)

    money_to_all = models.IntegerField(null=True, default=20)
    exp_to_all = models.IntegerField(null=True, default=20)
