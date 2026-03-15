def analyze_text(text):

    suspicious_keywords = [
        "error",
        "failed login",
        "unauthorized",
        "malware",
        "attack",
        "breach",
        "denied"
    ]

    findings = []

    for keyword in suspicious_keywords:
        if keyword.lower() in text.lower():
            findings.append(f"Suspicious keyword detected: {keyword}")

    if findings:
        return "\n".join(findings)
    else:
        return "No suspicious activity detected."