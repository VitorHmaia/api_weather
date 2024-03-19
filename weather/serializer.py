from rest_framework import serializers
from .models import WeatherEntity

class WeatherEntitySerializer(serializers.Serializer):
    temperature = serializers.IntegerField()
    date = serializers.DateField()

    def create(self, validated_data):
        return WeatherEntity.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.temperature = validated_data.get('temperature', instance.temperature)
        instance.date = validated_data.get('date', instance.date)
        instance.save()
        return instance
