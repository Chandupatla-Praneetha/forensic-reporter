from flask import Flask, render_template, request
import os
from text_extractor import extract_text
from ai_analyzer import analyze_text
from report_generator import generate_report
from log_analyzer import analyze_logs
from ml_analyzer import detect_anomalies

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/", methods=["GET", "POST"])
def upload_file():

    if request.method == "POST":

        file = request.files["file"]

        if file.filename == "":
            return "No file selected"

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        filename = file.filename

        # If CSV file → log analysis + ML anomaly detection
        if filename.endswith(".csv"):

            log_analysis = analyze_logs(filepath)

            ml_analysis = detect_anomalies(filepath)

            analysis_result = log_analysis + "\n" + ml_analysis

            extracted_text = "CSV log dataset analyzed using forensic log analysis and machine learning."

        # Otherwise → normal text evidence analysis
        else:

            extracted_text = extract_text(filepath)

            analysis_result = analyze_text(extracted_text)

        # Generate forensic report
        report = generate_report(filename, extracted_text, analysis_result)

        return f"<pre>{report}</pre>"

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)