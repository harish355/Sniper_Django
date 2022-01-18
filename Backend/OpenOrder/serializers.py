from django.db import models
from rest_framework import fields, serializers
from .models import OpenOrders
from CancelOrder.models import CanceledOrders
from CloseOrder.models import CloseOrders

class OpenOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenOrders
        fields = '__all__'

    def create(self, validated_data):
        return OpenOrders.objects.create(**validated_data)


class CloseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CloseOrders
        feilds = '__all__'
        exclude=['User']

class CancelOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CanceledOrders
        fields='__all__'