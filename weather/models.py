from django.db import models

# weather/models.py
class WeatherEntity:

    def __init__(self, temperature, date,
                 city='', atmospheric_pressure='',
                 humidity='', weather='') -> None:
        self.temperature = temperature
        self.city = city
        self.atmospheric_pressure = atmospheric_pressure
        self.humidity = humidity
        self.weather = weather
        self.date = date

    def __str__(self) -> str:
        return (f"Weather <{self.temperature}>")
