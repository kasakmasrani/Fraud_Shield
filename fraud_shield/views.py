from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return HttpResponse("Welcome to Fraud Shield! This is the home page.")


def register_view(request):
    return render(request, 'home/register.html')  # Make sure this template exists!
