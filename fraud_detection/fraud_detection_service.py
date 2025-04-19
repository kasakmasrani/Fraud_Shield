import pickle
import numpy as np
import os

# Load the trained model
MODEL_PATH = 'd:/Fraud_Shield/fraud_detection/isolation_forest_model.pkl'

def load_model(filepath):  # Add 'filepath' parameter
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Model file not found at {filepath}")
    with open(filepath, "rb") as f:
        return pickle.load(f)

# Predict fraud
def predict_fraud(fraud_model, transaction_features):  # Accept fraud_model as an argument
    features_array = np.array(transaction_features).reshape(1, -1)
    prediction = fraud_model.predict(features_array)
    return prediction[0] == -1  # -1 indicates fraud

def retrieve_regulations(transaction_amount):
    """
    Retrieve relevant financial regulations based on the transaction amount.
    """
    # Placeholder for actual implementation
    return f"Regulations for transactions above {transaction_amount}"

def get_past_fraud_cases(user, transaction_amount):
    """
    Retrieve past fraud cases for contextual insights.
    """
    # Placeholder for actual implementation
    return f"Past fraud cases for user {user.username} involving amounts near {transaction_amount}"
