from django.shortcuts import render
from .models import TemperatureReading, GlobalFlag, TempThresholdConfiguration
from rest_framework import viewsets
from .serializers import TemperatureSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.
def index(request):
    temps = TemperatureReading.objects.all()
    last_temp = TemperatureReading.objects.last()
    return render(request, 'Caldera/index.html', context={'temps': temps, 't_date_time': [t.date_time.isoformat() for t in temps], 't': [t.temperature for t in temps], 'last_temp': last_temp})


class TempViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows temps to be viewed or edited.
    """
    queryset = TemperatureReading.objects.all().order_by('date_time')
    serializer_class = TemperatureSerializer
