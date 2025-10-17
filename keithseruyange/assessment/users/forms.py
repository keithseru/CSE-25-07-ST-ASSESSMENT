from django import forms 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class SignupForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': "Full Name",
            'class': 'form-input'
        })
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder' : 'Email',
            'class': 'form-input',
        })
    )
    
    phone_number = forms.CharField(
        max_length=20,
        required=True,
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
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['full_name'].split()[0]
        if len(self.cleaned_data['full_name'].split()) > 1:
            user.last_name = ' '.join(self.cleaned_data['full_name'].split()[1:])
        user.phone_number = self.cleaned_data['phone_number']
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user

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