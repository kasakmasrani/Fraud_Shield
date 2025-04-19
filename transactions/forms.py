from django import forms
from .models import Transaction, FraudRule

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'description']  # Do not include 'is_fraudulent' (set by AI)

class FraudRuleForm(forms.ModelForm):
    class Meta:
        model = FraudRule
        fields = ['rule_name', 'threshold_amount', 'is_active', 'dynamic_threshold']  # Include dynamic_threshold
