from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, EmailValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

class Weather(models.Model):
    temperature = models.FloatField()
    city = models.CharField(max_length=100)
    atmospheric_pressure = models.FloatField()
    humidity = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    weather = models.CharField(max_length=50)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"Weather <{self.temperature}°C> in {self.city} on {self.date.strftime('%d/%m/%Y %H:%M:%S')}"

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = timezone.now()
        super().save(*args, **kwargs)

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True, validators=[EmailValidator()])
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def __str__(self) -> str:
        return f'{self.username}'

    def set_password(self, raw_password: str):
        super().set_password(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return super().check_password(raw_password)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
