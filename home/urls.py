from django.urls import path
from .views import index, dashboard

urlpatterns = [
    path('', index, name='index'),
    path('dashboard/', dashboard, name='dashboard'),  # Add URL for the dashboard
]
