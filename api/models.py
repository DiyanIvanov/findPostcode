from django.db import models

# Create your models here.
class Postcode(models.Model):
    postcode = models.CharField(max_length=10, unique=True)
    area = models.CharField(max_length=2)
    date_introduced = models.CharField(blank=True, null=True)
    date_terminated = models.CharField(blank=True, null=True)
    district = models.CharField(max_length=5)
    eastings = models.IntegerField(blank=True, null=True)
    northings = models.IntegerField(blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()


    def __str__(self):
        return self.postcode