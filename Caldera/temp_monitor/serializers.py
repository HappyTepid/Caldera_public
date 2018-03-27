from rest_framework import serializers
from temp_monitor.models import TemperatureReading

class TemperatureSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TemperatureReading
        fields = ('date_time', 'temperature')


class site24Serializer(serializers.Serializer):
    status = serializers.BooleanField()
