from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('add/', views.add_transaction, name='add_transaction'),
    path('view/', views.view_transactions, name='view_transactions'),
    path('fraud-insights/', views.fraud_insights, name='fraud_insights'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Admin dashboard
    path('manage-fraud-rules/', views.manage_fraud_rules, name='manage_fraud_rules'),
]
