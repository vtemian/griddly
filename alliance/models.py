from django.db import models
from account.models import UserProfile

class Alliance(models.Model):
    name = models.CharField(max_length=30)
    members = models.ManyToManyField(UserProfile)