from django.db import models

# Create your models here.
class Postcode(models.Model):
    postcode = models.CharField(max_length=10, unique=True)
    area = models.CharField(max_length=2)
    district = models.CharField(max_length=5)
    eastings = models.IntegerField()
    northings = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()


    def __str__(self):
        return self.postcode