from rest_framework import serializers
from api.models import Postcode


class PostcodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Postcode
        fields = ('postcode', 'district', 'area', 'eastings', 'northings', 'latitude', 'longitude')


class BatchSerializer(serializers.Serializer):
    postcodes = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=False
    )

    def validate_postcodes(self, value):
        cleaned = []

        for postcode in value:
            postcode = postcode.strip().upper()

            if not postcode:
                raise serializers.ValidationError("Empty postcode not allowed")

            cleaned.append(postcode)

        return cleaned
