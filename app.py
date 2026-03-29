from flask import Flask, render_template, request
import os
import pandas as pd

from text_extractor import extract_text
from ai_analyzer import analyze_text
from report_generator import generate_report

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():

    if "file" not in request.files:
        return "No file uploaded"

    file = request.files["file"]

    if file.filename == "":
        return "No file selected"

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    filename = file.filename

    # 🔹 TXT FILE (Conversation)
    if filename.endswith(".txt"):

        extracted_text = extract_text(filepath)
        analysis_result = analyze_text(extracted_text)

    # 🔹 CSV FILE (Treat as conversation dataset)
    elif filename.endswith(".csv"):

        df = pd.read_csv(filepath)

        # Convert all rows into one big text
        extracted_text = df.astype(str).apply(" ".join, axis=1).str.cat(sep=" ")

        analysis_result = analyze_text(extracted_text)

    else:
        return "Unsupported file format"

    # Generate report
    report = generate_report(filename, extracted_text, analysis_result)

    # PDF filename
    clean_name = filename.split(".")[0]
    pdf_file = f"{clean_name}.pdf"

    # 🔥 Suspicious keyword detection
    suspicious_keywords = ["attack", "hack", "unauthorized", "password", "kill"]

    count = 0
    for word in suspicious_keywords:
        count += analysis_result.lower().count(word)

    stats = {
        "suspicious_count": count
    }

    return render_template(
        "index.html",
        report=report,
        pdf_file=pdf_file,
        stats=stats
    )


if __name__ == "__main__":
    app.run(debug=True)

    