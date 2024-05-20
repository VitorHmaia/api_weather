# middleware.py
from django.shortcuts import redirect
from django.urls import reverse

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Evitar redirecionamento em loop para a página de Unauthorized
        if request.path != reverse('Unauthorized') and not request.user.is_authenticated:
            return redirect(reverse('Unauthorized'))
        response = self.get_response(request)
        return response
