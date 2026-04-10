from rest_framework import serializers
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class FindPostcodeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True,
            }
        }

    def create(self, validated_data):
        return UserModel.objects.create_user(**validated_data)