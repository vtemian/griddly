from django.contrib.auth.models import User
from django.db import models
from account.models import UserProfile

class Message(models.Model):
    message = models.TextField()
    
class Friend(models.Model):
    friends = models.ManyToManyField(UserProfile, null=True)
    user = models.ForeignKey(User)

