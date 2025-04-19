from datetime import timedelta
from django.utils.timezone import now
from .models import Transaction

def update_user_profile(user):
    """
    Update the user's average transaction amount and transaction frequency.
    """
    # Ensure numeric fields are properly converted
    total_transactions = user.transaction_frequency or 0  # Default to 0 if None
    total_amount = float(user.average_transaction_amount or 0.0)  # Default to 0.0 if None

    # Fetch all transactions for the user
    transactions = user.transaction_set.all()
    if transactions.exists():
        total_transactions = transactions.count()
        total_amount = sum(float(transaction.amount) for transaction in transactions)

    # Update user profile
    user.transaction_frequency = total_transactions
    user.average_transaction_amount = total_amount / total_transactions if total_transactions > 0 else 0.0
    user.save()

def detect_behavioral_anomaly(user, transaction_amount):
    # Check if the transaction amount is significantly higher than the user's average
    threshold = user.average_transaction_amount * 2  # Example: Flag if 2x the average
    return transaction_amount > threshold
