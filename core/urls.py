#urls.py
from django.urls import path
from weather.views import WeatherView, WeatherGenerate, WeatherClear, WeatherInsert, WeatherEdit, WeatherRemove, UnauthorizedView, UserTokenizer, RegisterView, LoginView, LogoutView
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', WeatherView.as_view(), name='Weather View'),
    path('generate', WeatherGenerate.as_view(), name='Generate Weather'),
    path('insert', WeatherInsert.as_view(), name='Insert Weather'),
    path('clear', WeatherClear.as_view(), name='Clear Database'),
    path('edit/<str:id>', WeatherEdit.as_view(), name='Weather Edit'),
    path('remove/<str:id>', WeatherRemove.as_view(), name='Weather Remove'),
    path('unauthorized', UnauthorizedView.as_view(), name='Unauthorized'),
    path('token/', UserTokenizer.as_view(), name='user_tokenizer'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]