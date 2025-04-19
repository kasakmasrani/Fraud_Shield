from django.db import models
from users.models import User
from django.contrib.auth.models import AbstractUser

# Remove the User model definition from this file
# class User(AbstractUser):
#     allowed_locations = models.TextField(default="")  # Comma-separated list of allowed locations

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_fraudulent = models.BooleanField(default=False)  # Flag for suspicious transactions
    location = models.CharField(max_length=255, null=True, blank=True)
    time = models.TimeField(null=True, blank=True)  # Add a time field

    def __str__(self):
        return f"{self.user.username} - {self.amount}"

class FraudRule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fraud_rules')
    rule_name = models.CharField(max_length=255)
    threshold_amount = models.DecimalField(max_digits=10, decimal_places=2, default=10000.00)  # Example: $10,000
    is_active = models.BooleanField(default=True)
    dynamic_threshold = models.BooleanField(default=False)  # Enable dynamic threshold adjustment

    def __str__(self):
        return f"{self.user.username} - {self.rule_name}"
