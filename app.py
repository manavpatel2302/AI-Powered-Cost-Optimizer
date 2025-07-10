from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import numpy as np
from werkzeug.utils import secure_filename
import os
import streamlit as st

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'csv', 'sheets'}

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']

    if file.filename == '':
        return "No file selected", 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            # Load Excel file
            df = pd.read_excel(filepath)

            # --- Simple mock analysis for demonstration ---
            cost_reduction = "28.5%"
            material_efficiency = "18.3%"
            durability_score = "87/100"

            # Simulate some design suggestions
            designs = [
                {
                    "id": "VAH-2245",
                    "description": "Feed Mixing Chamber",
                    "cost": "$2,150",
                    "durability": "88/100",
                    "materials": "Polymer, Stainless Steel",
                    "score": "94.7"
                },
                {
                    "id": "VAH-2246",
                    "description": "Cooling Fan Assembly",
                    "cost": "$1,780",
                    "durability": "85/100",
                    "materials": "Aluminum, PVC",
                    "score": "92.1"
                },
                {
                    "id": "VAH-2247",
                    "description": "Vibration Control Base",
                    "cost": "$980",
                    "durability": "90/100",
                    "materials": "Rubber, Steel",
                    "score": "95.2"
                }
            ]

            recommendations = [
                "Replace stainless steel with aluminum where feasible.",
                "Improve chamber airflow by 15% to enhance cooling efficiency.",
                "Reduce motor RPM by 5% to save energy without performance loss."
            ]

            # Also display uploaded table
            table_html = df.to_html(classes="table-auto w-full text-left text-sm", index=False, border=0)

            return render_template(
                'results.html',
                cost_reduction=cost_reduction,
                material_efficiency=material_efficiency,
                durability_score=durability_score,
                designs=designs,
                recommendations=recommendations,
                table_html=table_html
            )

        except Exception as e:
            return f"Error processing file: {str(e)}", 500

    return "Invalid file format", 400

if __name__ == '__main__':
    app.run(debug=True)
