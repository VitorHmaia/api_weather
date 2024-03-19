from django.shortcuts import render

from datetime import datetime
from random import randrange
from django.views import View
from django.shortcuts import render, redirect
from .models import WeatherEntity
from .repositories import WeatherRepository
from .serializer import WeatherEntitySerializer

class WeatherView(View):
    def get(self, request):
        repository = WeatherRepository(collection_name='weathers')
        weathers = repository.get_all()
        return render(request, "home.html", {"weathers":weathers})
    

class WeatherGenerate(View):
    def get(self, request):
        repository = WeatherRepository(collection_name='weathers')
        weather = {
            "temperature" : 28,
            "date": "hoje"
            }
        repository.insert(weather)

        return redirect('Weather View')
    
class WeatherReset(View):
    def get(self, request):
        repository = WeatherRepository(collection_name='weathers')
        repository.delete_all()
        return redirect('Weather View')