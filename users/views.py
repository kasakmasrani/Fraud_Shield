from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import User
from .forms import CustomUserCreationForm  # Import the custom form
from django.contrib.auth.forms import AuthenticationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # Bind form with POST data
        if form.is_valid():  # Validate the form
            form.save()  # Save the user to the database
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')  # Redirect to the login page
        else:
            messages.error(request, "Registration failed. Please correct the errors.")
    else:
        form = CustomUserCreationForm()  # Render an empty form for GET requests
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful.")  # Trigger success message only after login
            return redirect('dashboard')  # Redirect to the dashboard after login
        else:
            messages.error(request, "Invalid username or password.")  # Trigger error message for invalid login
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")  # Trigger success message only after logout
    return redirect('login')  # Redirect to the login page after logout
