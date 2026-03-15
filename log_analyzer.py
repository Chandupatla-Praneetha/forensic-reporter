import pandas as pd

def analyze_logs(filepath):

    df = pd.read_csv(filepath)

    suspicious_activity = []

    # Check for failed logins
    if "status" in df.columns:
        failed_logins = df[df["status"] == "failed"]

        if len(failed_logins) > 3:
            suspicious_activity.append(
                f"Multiple failed login attempts detected: {len(failed_logins)}"
            )

    # Check repeated users
    if "user" in df.columns:
        user_counts = df["user"].value_counts()

        for user, count in user_counts.items():
            if count > 5:
                suspicious_activity.append(
                    f"User {user} has unusually high activity ({count} actions)"
                )

    if suspicious_activity:
        return "\n".join(suspicious_activity)

    return "No suspicious log activity detected."