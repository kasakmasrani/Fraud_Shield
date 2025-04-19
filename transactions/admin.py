from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'description', 'timestamp', 'is_fraudulent', 'admin_dashboard_link')
    list_filter = ('is_fraudulent', 'timestamp')
    search_fields = ('user__username', 'description')

    def admin_dashboard_link(self, obj):
        url = reverse('transactions:admin_dashboard')  # Use the URL name for the admin dashboard
        return format_html('<a href="{}" target="_blank">Go to Admin Dashboard</a>', url)

    admin_dashboard_link.short_description = "Admin Dashboard"
