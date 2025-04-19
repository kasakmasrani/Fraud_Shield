# import pandas as pd
# from sklearn.ensemble import IsolationForest
# import pickle

# # Load transaction data
# DATASET_PATH = 'd:/Fraud_Shield/fraud_detection/transaction_data.csv'  # Replace with your dataset
# data = pd.read_csv(DATASET_PATH)  # Ensure the dataset file exists at this path
# features = data[['amount']]  # Add more features as needed

# # Train the model
# model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
# model.fit(features.values)

# # Save the model
# MODEL_PATH = 'd:/Fraud_Shield/fraud_detection/isolation_forest_model.pkl'
# with open(MODEL_PATH, 'wb') as f:
#     pickle.dump(model, f)
# print(f"Model saved to {MODEL_PATH}")
import pandas as pd
from sklearn.ensemble import IsolationForest
import pickle

# Load transaction data
DATASET_PATH = 'd:/Fraud_Shield/fraud_detection/transaction_data.csv'  
data = pd.read_csv(DATASET_PATH)

# Feature selection
features = data[['amount', 'time']]  # Add 'user_history', 'device', etc.

# Train the Isolation Forest model
model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
model.fit(features)

# Save the model
MODEL_PATH = 'd:/Fraud_Shield/fraud_detection/isolation_forest_model.pkl'
with open(MODEL_PATH, 'wb') as f:
    pickle.dump(model, f)

print(f"Model saved to {MODEL_PATH}")
