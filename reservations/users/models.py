from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class CountryChoices(models.TextChoices):
    BR = 'Brazil',
    US = 'United States',
    UK = 'United Kingdom',
    JP = 'Japan'

class Profile(models.Model):
    account = models.OneToOneField("User", null=True, blank=True, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=254, unique=True)
    address_line = models.CharField(max_length=250, blank=True)
    country_code = models.CharField(choices=CountryChoices.choices, default=CountryChoices.BR)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.display_name