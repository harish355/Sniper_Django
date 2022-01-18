from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from .models import Symbols


class SymbolsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symbols
        fields = ('Market', 'Chart_Symbol', 'Terminal_Symbol', 'Stoploss','Limit','Quantity')


    def create(self, validated_data):
        return Symbols.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.save()
    #     return instance

class Symbols_Get_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Symbols
        fields = '__all__'



    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.save()
    #     return instance
