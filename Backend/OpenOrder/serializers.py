from django.db import models
from rest_framework import fields, serializers
from .models import OpenOrders
from CancelOrder.models import CanceledOrders

class OpenOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenOrders
        fields = '__all__'

    def create(self, validated_data):
        return OpenOrders.objects.create(**validated_data)


class CloseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenOrders
        feilds = ['Order_Number', 'Chart_Symbol', 'Exit_at']

class CancelOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CanceledOrders
        fields='__all__'