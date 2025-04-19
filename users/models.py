from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True)
    average_transaction_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    transaction_frequency = models.IntegerField(default=0)  # Number of transactions in the last 30 days
    allowed_locations = models.TextField(default="")  # Comma-separated list of allowed locations

    objects = UserManager()

    def __str__(self):
        return self.username


# filepath: c:\SEM_IV\Fraud_Shield\users\models.py
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    average_transaction_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
