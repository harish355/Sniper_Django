from rest_framework import serializers
from .models import Api_table


class Api_data_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Api_table
        fields = ('userid','api_key')

    def create(self, validated_data):
        return Api_table.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.save()
    #     return instance
