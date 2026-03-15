import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(filepath):

    df = pd.read_csv(filepath)

    # Convert categorical data to numbers
    df_encoded = df.select_dtypes(include=["number"])

    if df_encoded.empty:
        return "No numerical data available for ML anomaly detection."

    model = IsolationForest(contamination=0.1)

    predictions = model.fit_predict(df_encoded)

    anomaly_count = list(predictions).count(-1)

    if anomaly_count > 0:
        return f"AI detected {anomaly_count} anomalous log entries."

    return "No anomalies detected by machine learning."