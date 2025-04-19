from sklearn.cluster import KMeans
import pandas as pd

def cluster_fraud_patterns(transactions):
    # Convert transactions to a DataFrame
    df = pd.DataFrame(list(transactions.values('amount', 'timestamp')))
    df['timestamp'] = pd.to_datetime(df['timestamp']).astype(int) / 10**9  # Convert timestamp to numeric

    # Apply K-Means clustering
    kmeans = KMeans(n_clusters=2, random_state=42)
    df['cluster'] = kmeans.fit_predict(df[['amount', 'timestamp']])

    return df
