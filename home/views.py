from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'home/index.html')  # Ensure this path matches your folder structure

@login_required
def dashboard(request):
    return render(request, 'home/dashboard.html')  # Render the dashboard template
