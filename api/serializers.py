from rest_framework import serializers
from api.models import Postcode
from decouple import config


class PostcodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Postcode
        fields = ('postcode', 'district', 'area', 'eastings', 'northings', 'latitude', 'longitude')


class BatchSerializer(serializers.Serializer):
    postcodes = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=False,
        min_length=1,
        max_length=config('MAX_BATCH_POSTCODES', cast=int),
    )

    def validate_postcodes(self, value):
        return [postcode.upper() for postcode in value]
