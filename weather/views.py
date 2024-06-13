from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .repositories import WeatherRepository
from .models import Weather
from .serializer import WeatherSerializer
from .forms import WeatherForm
from datetime import datetime
from random import randrange
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from typing import Any

MAIN_VIEW = 'weather_view'

class WeatherView(LoginRequiredMixin, APIView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.repository = WeatherRepository(collection_name='weathers')

    def get(self, request):
        try:
            weathers = list(self.repository.get_all())
            serializer = WeatherSerializer(weathers, many=True)
            return render(request, "home.html", {"weathers": serializer.data})
        except Exception as e:
            return render(request, "home.html", {"error": str(e)})

    def post(self, request):
        serializer = WeatherSerializer(data=request.data)
        if serializer.is_valid():
            self.repository.insert(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WeatherGenerate(LoginRequiredMixin, APIView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.repository = WeatherRepository(collection_name='weathers')

    def get(self, request):
        CIDADES_BRASIL = ["São Paulo", "Rio de Janeiro", "Salvador", "Brasília", "Fortaleza", "Belo Horizonte", "Manaus", "Curitiba", "Recife", "Porto Alegre"]
        CONDICOES_TEMPO = ["Ensolarado", "Nublado", "Chuvoso", "Neve", "Tempestade", "Parcialmente nublado", "Neblina", "Ventania"]
        weather_data = {
            "temperature": randrange(5, 30),
            "date": datetime.now(),
            "atmospheric_pressure": randrange(800, 1500),
            "humidity": randrange(20, 90),
            "city": CIDADES_BRASIL[randrange(len(CIDADES_BRASIL))],
            "weather": CONDICOES_TEMPO[randrange(len(CONDICOES_TEMPO))]
        }
        
        serializer = WeatherSerializer(data=weather_data)
        if serializer.is_valid():
            self.repository.insert(serializer.validated_data)
        else:
            print(serializer.errors)
        return redirect(MAIN_VIEW)

class WeatherClear(LoginRequiredMixin, APIView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.repository = WeatherRepository(collection_name='weathers')

    def get(self, request):
        self.repository.delete_all()
        return redirect(MAIN_VIEW)

class WeatherInsert(LoginRequiredMixin, View):
    def get(self, request):
        weather_form = WeatherForm()
        return render(request, "add-weather.html", {"form": weather_form})
    
    def post(self, request):
        weather_form = WeatherForm(request.POST)
        if weather_form.is_valid():
            serializer = WeatherSerializer(data=weather_form.cleaned_data)
            if serializer.is_valid():
                self.repository.insert(serializer.validated_data)
            else:
                print(serializer.errors)
        else:
            print(weather_form.errors)
        return redirect(MAIN_VIEW)

class WeatherEdit(LoginRequiredMixin, View):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.repository = WeatherRepository(collection_name='weathers')

    def post(self, request, id):
        weather_form = WeatherForm(request.POST)
        if weather_form.is_valid():
            serializer = WeatherSerializer(data=weather_form.cleaned_data)
            if serializer.is_valid():
                self.repository.update(id, serializer.validated_data)
            else:
                print(serializer.errors)
        else:
            print(weather_form.errors)
        return redirect(MAIN_VIEW)

    def get(self, request, id):
        weather_data = get_object_or_404(Weather, pk=id)
        weather_form = WeatherForm(instance=weather_data)
        return render(request, "edit-weather.html", {"form": weather_form, 'id': id})

class WeatherRemove(LoginRequiredMixin, View):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.repository = WeatherRepository(collection_name='weathers')

    def get(self, request, id):
        self.repository.delete_by_id(id)
        return redirect(MAIN_VIEW)
