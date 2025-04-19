from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Transaction
from .forms import TransactionForm, FraudRuleForm
from fraud_detection.fraud_detection_service import load_model, predict_fraud
import numpy as np
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
import matplotlib.pyplot as plt
import io
import base64
import os
from fraud_detection.fraud_detection_service import load_model, retrieve_regulations, get_past_fraud_cases
from .utils import update_user_profile, detect_behavioral_anomaly

# Load the trained model
MODEL_PATH = os.path.join(os.path.dirname(__file__), '../fraud_detection/isolation_forest_model.pkl')
fraud_model = load_model(MODEL_PATH)

def analyze_transaction(user, transaction_features, transaction_amount, transaction_location):
    """
    Analyze the transaction using AI-based anomaly detection and provide contextual insights.
    """
    # Predict fraud using the AI model
    is_fraudulent = predict_fraud(fraud_model, transaction_features)

    # Detect behavioral anomalies
    if detect_behavioral_anomaly(user, transaction_amount):
        is_fraudulent = True

    # Check for location-based anomalies
    allowed_locations = user.allowed_locations or ""  # Ensure allowed_locations is a string
    if transaction_location not in allowed_locations.split(","):
        is_fraudulent = True

    # Retrieve relevant financial regulations
    regulations = retrieve_regulations(transaction_amount)

    # Retrieve past fraud cases for contextual insights
    past_fraud_cases = get_past_fraud_cases(user, transaction_amount)

    insights = {
        "regulations": regulations,
        "past_fraud_cases": past_fraud_cases,
        "location_anomaly": transaction_location not in allowed_locations.split(","),
    }

    return is_fraudulent, insights

@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user

            # Save the transaction to populate the timestamp field
            transaction.save()

            # Prepare transaction features for fraud detection
            # Ensure the input matches the model's expected shape
            transaction_features = np.array([[transaction.amount]])  # Use only the amount

            # Debugging: Print the shape of the input
            print("Shape of transaction_features before prediction:", transaction_features.shape)

            # Analyze the transaction
            transaction.is_fraudulent, insights = analyze_transaction(
                request.user, transaction_features, transaction.amount, transaction.location
            )

            # Check custom fraud rules
            active_rules = request.user.fraud_rules.filter(is_active=True)
            for rule in active_rules:
                threshold = rule.threshold_amount if not rule.dynamic_threshold else request.user.average_transaction_amount * 2
                if transaction.amount > threshold:
                    transaction.is_fraudulent = True
                    break

            # Save the updated transaction with fraud status
            transaction.save()
            update_user_profile(request.user)

            # Generate appropriate messages
            if transaction.is_fraudulent:
                messages.warning(request, f"Transaction flagged as suspicious! Insights: {insights}")
            else:
                messages.success(request, "Transaction added successfully.")
            return redirect('transactions:view_transactions')
        else:
            messages.error(request, "Failed to add transaction. Please correct the errors.")
    else:
        form = TransactionForm()
    return render(request, 'transactions/add_transaction.html', {'form': form})

@login_required
def view_transactions(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'transactions/view_transactions.html', {'transactions': transactions})

@login_required
def fraud_insights(request):
    fraudulent_transactions = Transaction.objects.filter(user=request.user, is_fraudulent=True)
    total_fraud = fraudulent_transactions.count()
    total_transactions = Transaction.objects.filter(user=request.user).count()
    fraud_percentage = round((total_fraud / total_transactions) * 100, 2) if total_transactions > 0 else 0.0  # Format to 2 decimal points

    context = {
        "fraudulent_transactions": fraudulent_transactions,
        "total_fraud": total_fraud,
        "fraud_percentage": fraud_percentage,
    }
    return render(request, 'transactions/fraud_insights.html', context)

@staff_member_required
def admin_dashboard(request):
    transactions = Transaction.objects.all()
    fraud_counts = transactions.values('is_fraudulent').annotate(count=Count('id'))
    fraud_dict = {item['is_fraudulent']: item['count'] for item in fraud_counts}

    fraudulent_count = fraud_dict.get(True, 0)
    non_fraudulent_count = fraud_dict.get(False, 0)

    labels = ['Fraudulent', 'Non-Fraudulent']
    values = [fraudulent_count, non_fraudulent_count]

    plt.figure(figsize=(6,4))
    plt.bar(labels, values, color=['red', 'green'])
    plt.title('Fraudulent vs Non-Fraudulent Transactions')
    plt.ylabel('Count')
    plt.xlabel('Transaction Type')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    chart = base64.b64encode(image_png).decode('utf-8')

    return render(request, 'transactions/admin_dashboard.html', {
        'chart': chart,
        'transactions': transactions,
    })

@login_required
def manage_fraud_rules(request):
    if request.method == 'POST':
        form = FraudRuleForm(request.POST)
        if form.is_valid():
            rule = form.save(commit=False)
            rule.user = request.user
            rule.save()
            messages.success(request, "Fraud rule added successfully.")
            return redirect('transactions:manage_fraud_rules')
    else:
        form = FraudRuleForm()
    rules = request.user.fraud_rules.all()
    return render(request, 'transactions/manage_fraud_rules.html', {'form': form, 'rules': rules})
