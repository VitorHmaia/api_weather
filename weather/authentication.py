import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.utils.timezone import make_aware, timezone

from .models import UserEntity

def authenticate(username, password):
    if username == 'user' and password == 'a1b2c3':
        user = UserEntity(username=username, password=password)
        return user
    return None

def generate_token(user):
    payload = {
        'username': user.username,
        'exp': make_aware(datetime.now() + timedelta(minutes=5), timezone.utc)
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

def refresh_token(user):
    return generate_token(user)

def verify_token(token):
    error_code = 0
    payload = None
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        error_code = 1
    except jwt.InvalidTokenError:
        error_code = 2

    return [error_code, payload]

def get_authenticated_user(token):
    _, payload = verify_token(token)
    if payload:
        return UserEntity(username=payload['username'])
    return None
