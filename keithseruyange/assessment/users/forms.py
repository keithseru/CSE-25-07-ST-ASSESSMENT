from django import forms 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class SignupForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextINput(attrs={
            'placeholder': "Full Name",
            'class': 'form-input'
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder' : 'Email',
            'class': 'form-input',
        })
    )
    
    phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder':'Phone Number',
            'class':'form-input',
        })
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class':'form-input'
        })
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm Password',
            'class':'form-input'
        })
    )
    
    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'phone_number', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Email or Phone Number',
            'class': 'form-input'
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder':'Password',
            'class':'form-input'
        })
    )