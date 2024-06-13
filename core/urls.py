from django.urls import path
from django.contrib import admin
from weather.views import (
    WeatherView,
    WeatherGenerate,
    WeatherClear,
    WeatherInsert,
    WeatherEdit,
    WeatherRemove
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # JWT authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Weather endpoints
    path('', login_required(WeatherView.as_view()), name='weather_view'),
    path('generate/', login_required(WeatherGenerate.as_view()), name='generate_weather'),
    path('insert/', login_required(WeatherInsert.as_view()), name='insert_weather'),
    path('clear/', login_required(WeatherClear.as_view()), name='clear_database'),
    path('edit/<str:id>/', login_required(WeatherEdit.as_view()), name='weather_edit'),
    path('remove/<str:id>/', login_required(WeatherRemove.as_view()), name='weather_remove'),
]
