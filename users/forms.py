from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User  # Import your custom user model

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User  # Use the custom User model
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number', 'address']
