from django.db import models
from account.models import UserProfile

class Request(models.Model):
    accepted = models.BooleanField(default=False)

    class Meta:
        abstract = True

class UpToUpRequest(Request):
    sender = models.ForeignKey(UserProfile)
    recipient = models.ForeignKey(UserProfile)
    message = models.TextField()
