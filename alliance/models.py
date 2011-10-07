from django.db import models
from datetime import datetime
from account.models import UserProfile


class Alliance(models.Model):
    name = models.CharField(max_length=30)
    members = models.ManyToManyField(UserProfile, null=True, through="alliance.AllianceMembership")

    avatar = models.ImageField(upload_to='avatars/%Y/%m/%d', null=True)

class AllianceMembership(models.Model):
    alliance = models.ForeignKey(Alliance)
    profile = models.ForeignKey(UserProfile)

    rank = models.CharField(max_length=30)
    
class Vote(models.Model):
    profile = models.ForeignKey(UserProfile)

    created_at = models.DateField(default=datetime.now())

    class Meta:
        abstract = True

class Like(Vote):
    type = models.CharField(max_length=30, default="like")
    
class Unlike(Vote):
    type = models.CharField(max_length=30, default="unlike")

class AllianceNews(models.Model):
    alliance = models.ForeignKey(Alliance)
    profile = models.ForeignKey(UserProfile)

    title = models.CharField(max_length=50)
    created_at = models.DateField(default=datetime.now())
    text = models.TextField(null=True)
    type = models.CharField(max_length=30, default="simple")

    like = models.ManyToManyField(Like)
    unlike = models.ManyToManyField(Unlike)

