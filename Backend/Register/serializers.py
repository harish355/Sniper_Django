from rest_framework import serializers
from .models import Account, UserManager


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('email', 'username', 'password', 'phone')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        return Account.objects.create_user(**validated_data)
