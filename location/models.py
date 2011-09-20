from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=30)
    lat = models.FloatField(max_length=30)
    lng = models.FloatField(max_length=30)

    territory = models.ForeignKey("territory.Territory", related_name="locations", null=True)
    
    subscription = models.FloatField(max_length=20, default=1)

    zone = models.CharField(max_length=30, null=True)