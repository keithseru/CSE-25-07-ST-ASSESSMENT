from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
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
    
    phone_regex = RegexValidator(
        regex=r'^(\+?256|0)?[0-9]{9}$',
        message="Phone number must be in format: '+256712345678' or '0712345678'"
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
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered!')
        return email
    
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone.startswith('0'):
            normalized_phone = '+256' + phone[1:]
        elif phone.startswith('+'):
            normalized_phone = phone
        else:
            normalized_phone = '+256' + phone
        
        if CustomUser.objects.filter(phone_number=normalized_phone).exists():
            raise forms.ValidationError('This phone number is already registered.')
        return phone
    
    
    def save(self, commit=True):
        user = super().save(commit=False)
        full_name_parts = self.cleaned_data['full_name'].split()
        user.first_name = full_name_parts[0]
        if len(full_name_parts) > 1:
            user.last_name = ' '.join(full_name_parts[1:])
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data['phone_number']
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
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
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            # Try to find user by email or phone number
            user = None
            
            # Check if username is email
            if '@' in username:
                try:
                    user = CustomUser.objects.get(email=username)
                except CustomUser.DoesNotExist:
                    pass
            else:
                # It's a phone number, normalize it
                if username.startswith('0'):
                    normalized_phone = '+256' + username[1:]
                elif username.startswith('+'):
                    normalized_phone = username
                else:
                    normalized_phone = '+256' + username
                
                try:
                    user = CustomUser.objects.get(phone_number=normalized_phone)
                except CustomUser.DoesNotExist:
                    pass
            
            if user:
                # Authenticate using the username field
                self.user_cache = authenticate(username=user.username, password=password)
                if self.user_cache is None:
                    raise forms.ValidationError('Invalid credentials')
            else:
                raise forms.ValidationError('Invalid credentials')
        
        return self.cleaned_data

    def get_user(self):
        return getattr(self, 'user_cache', None)