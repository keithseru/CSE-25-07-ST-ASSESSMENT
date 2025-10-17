from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^(\+?256|0)?[0-9]{9}$',
        message="Phone number must be in format: '+256712345678' or '0712345678'"
    )
    
    phone_number = models.CharField(
        max_length=17, 
        blank=True, 
        unique=True, 
        null=True,
        validators=[phone_regex]
    )
    
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.email or self.username

    def save(self, *args, **kwargs):
        # Normalize phone number to include country code
        if self.phone_number and not self.phone_number.startswith('+'):
            if self.phone_number.startswith('0'):
                self.phone_number = '+256' + self.phone_number[1:]
            else:
                self.phone_number = '+256' + self.phone_number
        super().save(*args, **kwargs)