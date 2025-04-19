from django.contrib import admin
from django.urls import path, include
from users import views  # Import views from users app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),  # Add logout URL
    path('', include('home.urls')),  # Include home app URLs
    path('transactions/', include('transactions.urls', namespace='transactions')),  # Include transactions app URLs with namespace
]
