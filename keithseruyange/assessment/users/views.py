from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, LoginForm

# Create your views here.
def signup_view(request):
    '''Sign up new user'''
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = SignupForm()
        
    return render(request, 'signup.html', {'form':form})


def login_user(request):
    '''Log in user'''
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid credentials')
                
        else:
            messages.error(request, 'Invalid credentials')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form':form})

def logout_user(request):
    '''Logout User'''
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    ''''Success Message'''
    return render(request, 'dashboard.html')