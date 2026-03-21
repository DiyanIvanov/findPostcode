from django.db import models

# Create your models here.
class Postcode(models.Model):
    postcode = models.CharField(max_length=10, unique=True)
    area = models.CharField(max_length=10)
    district = models.CharField(max_length=10)
    eastings = models.CharField(max_length=10)
    northings = models.CharField(max_length=10)
    latitude = models.CharField(max_length=10)
    longitude = models.CharField(max_length=10)


    def __str__(self):
        return self.postcode