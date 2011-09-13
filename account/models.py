from django.db import models
from django.contrib.auth.models import User
from territory.models import Territory

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    gravatar_url = models.CharField(max_length=100)
    
    facebook = models.CharField(max_length=100, default="Facebook")
    google = models.CharField(max_length=100, default="Google")
    yahoo = models.CharField(max_length=100, default="Yahoo")

    money = models.IntegerField(null=True, default=10)
    exp = models.IntegerField(null=True, default=0)
    lvl = models.IntegerField(default=1)
    
    money_to_all = models.IntegerField(null=True, default=20)
    exp_to_all = models.IntegerField(null=True, default=20)

    territory = models.ForeignKey(Territory, null=True)

    achieve_points = models.IntegerField(default=0)

    clan_stream = models.CharField(max_length=30, default="none")
    friends_stream = models.BooleanField(max_length=30, default=True)

    widget_top = models.CharField(max_length=30, default="0")
    widget_left = models.CharField(max_length=30, default="0")