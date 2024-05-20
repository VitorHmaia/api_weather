from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .repositories import WeatherRepository
from .models import WeatherEntity
from datetime import datetime
from random import randrange
from .serializer import WeatherSerializer
from .forms import WeatherForm
from .authentication import generate_token
from typing import Any

MAIN_VIEW = 'Weather View'

class UnauthorizedView(View):
    def get(self, request):
        return render(request, 'unauthorized.html')

class WeatherView(View):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.repository = WeatherRepository(collection_name='weathers')

    def get(self, request):
        try:
            weathers = list(self.repository.get_all())
            serializer = WeatherSerializer(data=weathers, many=True)
            if serializer.is_valid():
                weathers_data = serializer.data
                return render(request, "home.html", {"weathers": weathers_data})
            else:
                return render(request, "home.html", {"error": serializer.errors})
        except Exception as e:
            return render(request, "home.html", {"error": str(e)})
    
    def post(self, request):
        weather_data = {
            "temperature": request.POST.get("temperature"),
            "date": request.POST.get("date"),
            "atmospheric_pressure": request.POST.get("atmospheric_pressure"),
            "humidity": request.POST.get("humidity"),
            "city": request.POST.get("city"),
            "weather": request.POST.get("weather")
        }
        self.repository.insert(weather_data)
        return redirect('home')

    def put(self, request):
        weather_id = request.POST.get("weather_id")
        weather_data = {
            "temperature": request.POST.get("temperature"),
            "date": request.POST.get("date"),
            "atmospheric_pressure": request.POST.get("atmospheric_pressure"),
            "humidity": request.POST.get("humidity"),
            "city": request.POST.get("city"),
            "weather": request.POST.get("weather")
        }
        query = {"_id": weather_id}
        self.repository.update(query, weather_data)
        return redirect('home')

    def delete(self, request):
        weather_id = request.POST.get("weather_id")
        query = {"_id": weather_id}
        self.repository.delete(query)
        return redirect('home')

class UserTokenizer(View):
    def post(self, request):
        try:
            data = request.POST
            username = data.get('username')
            password = data.get('password')

            if username is None or password is None:
                return HttpResponse('Username and password are required.', status=400)

            user = authenticate(username=username, password=password)
            if user:
                token = generate_token(user)
                return HttpResponse(token, content_type='text/plain')
            else:
                return HttpResponse('Username and/or password incorrect.', status=401)
        except Exception as e:
            return HttpResponse(str(e), status=500)

class WeatherGenerate(View):
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

        return redirect('home')

class WeatherClear(View):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.repository = WeatherRepository(collection_name='weathers')
    
    def get(self, request):
        self.repository.delete_all()
        return redirect('home')

class WeatherInsert(View):
    def get(self, request):
        weather_form = WeatherForm()
        return render(request, "add-weather.html", {"form": weather_form})
    
    def post(self, request):
        weather_form = WeatherForm(request.POST)
        if weather_form.is_valid():
            serializer = WeatherSerializer(data=weather_form.data)
            if serializer.is_valid():
                repository = WeatherRepository(collection_name='weathers')
                repository.insert(serializer.validated_data)
            else:
                print(serializer.errors)
        else:
            print(weather_form.errors)

        return redirect('home')

class WeatherEdit(View):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.repository = WeatherRepository(collection_name='weathers')
    
    def post(self, request, id):
        weather_form = WeatherForm(request.POST)
        if weather_form.is_valid():
            serializer = WeatherSerializer(data=weather_form.data)
            if serializer.is_valid():
                repository = WeatherRepository(collection_name='weathers')
                repository.update(id, serializer.validated_data)
            else:
                print(serializer.errors)
        else:
            print(weather_form.errors)
        return redirect('home')
    
    def get(self, request, id):
        weather_data = self.repository.get_by_id(id)
        weather_form = WeatherForm(initial=weather_data)
        weathers = list(self.repository.get_all())
        serializer = WeatherSerializer(data=weathers, many=True)
        if serializer.is_valid():
            weathers_data = serializer.data
            return render(request, "edit-weather.html", {"form": weather_form, 'id': id, "weathers": weathers_data})

class WeatherRemove(View):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.repository = WeatherRepository(collection_name='weathers')
    
    def get(self, request, id):
        self.repository.delete_by_id(id)
        return redirect('home')

class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'register.html', {'form': form})
