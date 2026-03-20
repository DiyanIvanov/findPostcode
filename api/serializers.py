from rest_framework import serializers

from api.models import Postcode


class PostcodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Postcode
        fields = ('postcode', 'district', 'area', 'easting', 'northing', 'latitude', 'longitude')
