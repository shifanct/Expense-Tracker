from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:  
            try:
                user = User.objects.create_user(username=username, password=password)
                login(request, user)
                return redirect('dashboard')
                
            except:
                return render(request, 'auth/signup.html', {'error': 'Username already exists'})
        
        return render(request, 'auth/signup.html', {'error': 'Please fill all fields'})
    return render(request, 'auth/signup.html')

def login_view(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username') 
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            error_message = 'Invalid username or password'
    
    return render(request, 'auth/login.html', {'error_message': error_message})

def logout(request):
    auth_logout(request)
    return redirect('login')