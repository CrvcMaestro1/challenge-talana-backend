from rest_framework import serializers


class JourneySerializer(serializers.Serializer):
    name = serializers.CharField()
    passengers = serializers.IntegerField()


class VehicleSerializer(serializers.Serializer):
    name = serializers.CharField()
    passengers = serializers.IntegerField()
    vehicle_type = serializers.CharField()
