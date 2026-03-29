from datetime import datetime
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def calculate_risk_score(analysis_result):

    score = 0

    if "failed login" in analysis_result.lower():
        score += 30

    if "unauthorized" in analysis_result.lower():
        score += 30

    if "anomal" in analysis_result.lower():
        score += 40

    return min(score, 100)


def classify_threat(score):

    if score >= 70:
        return "HIGH"
    elif score >= 40:
        return "MEDIUM"
    else:
        return "LOW"


def generate_pdf(report_text, filename):

    clean_name = filename.split(".")[0]
    pdf_path = os.path.join("static", f"{clean_name}.pdf")
    c = canvas.Canvas(pdf_path, pagesize=letter)

    text = c.beginText(40, 750)
    text.setFont("Helvetica", 10)

    for line in report_text.split("\n"):
        text.textLine(line)

    c.drawText(text)
    c.save()


def generate_report(filename, extracted_text, analysis_result):

    risk_score = calculate_risk_score(analysis_result)
    threat_level = classify_threat(risk_score)

    report = f"""
DIGITAL FORENSIC ANALYSIS REPORT
---------------------------------

File Name: {filename}
Analysis Date: {datetime.now()}

Threat Level: {threat_level}
Risk Score: {risk_score} / 100

---------------------------------
EXTRACTED DATA
---------------------------------

{extracted_text}

---------------------------------
AI ANALYSIS RESULT
---------------------------------

{analysis_result}
"""

    # Save TXT
    txt_path = os.path.join("reports", f"{filename}.txt")
    with open(txt_path, "w") as file:
        file.write(report)

    # Save PDF
    generate_pdf(report, filename)

    return report