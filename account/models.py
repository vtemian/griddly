from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    
    gravatar_url = models.CharField(max_length=100)

    money = models.IntegerField(null=True, default=10)
    exp = models.IntegerField(null=True, default=0)
    lvl = models.IntegerField(default=1)
    
    money_to_all = models.IntegerField(null=True, default=20)
    exp_to_all = models.IntegerField(null=True, default=20)
    

class Message(models.Model):
    message = models.TextField()
    
