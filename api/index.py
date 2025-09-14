import pickle
import joblib  # NEW: Import joblib to load the encoders
import numpy as np
import pandas as pd
from flask import Flask, request, render_template_string

# Load the trained model and the encoders
model = pickle.load(open("electricity_model.pkl", "rb"))
encoders = joblib.load("encoders.pkl") # NEW: Load the saved encoders

app = Flask(__name__)

# NEW: Extract the actual names for cities and companies from the encoders
city_names = encoders['City'].classes_
company_names = encoders['Company'].classes_


# NEW: Updated HTML template with dropdowns for City and Company
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Electricity Bill Prediction ⚡</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gradient-to-r from-blue-700 via-blue-800 to-gray-900 min-h-screen flex items-center justify-center p-6">
    <div class="bg-white rounded-2xl shadow-2xl max-w-3xl w-full p-10">
        
        <h1 class="text-4xl font-extrabold text-center text-yellow-500 mb-4">
            ⚡ Electricity Bill Prediction ⚡
        </h1>
        <p class="text-center text-gray-600 mb-8">
            Enter appliance usage and details below to predict your monthly electricity bill.
        </p>
        
        <form method="POST" class="grid grid-cols-2 gap-6">
            
            {% for field in fields %}
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">{{ field }}</label>
                    
                    {% if field == 'City' %}
                        <select name="City" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50">
                            {% for i in range(city_names|length) %}
                                <option value="{{ i }}">{{ city_names[i] }}</option>
                            {% endfor %}
                        </select>

                    {% elif field == 'Company' %}
                        <select name="Company" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50">
                            {% for i in range(company_names|length) %}
                                <option value="{{ i }}">{{ company_names[i] }}</option>
                            {% endfor %}
                        </select>

                    {% else %}
                        <input type="number" step="any" name="{{ field }}" required
                               class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50">
                    {% endif %}
                </div>
            {% endfor %}

            <div class="col-span-2 flex justify-center mt-6">
                <button type="submit" class="px-8 py-3 bg-blue-600 text-white font-bold rounded-xl hover:bg-blue-700 transition">
                    Predict ⚡
                </button>
            </div>
        </form>

        {% if prediction is not none %}
            <div class="mt-8 bg-green-100 text-green-800 p-4 rounded-lg text-center font-bold text-lg">
                💡 Predicted Electricity Bill: ₹ {{ prediction }}
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

# Form fields (same order as dataset features)
FIELDS = [
    "Fan", "Refrigerator", "Air Conditioner", "Television", "Monitor",
    "MotorPump", "Month", "City", "Company", "Monthly Hours", "Tariff Rate"
]

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    if request.method == "POST":
        try:
            # This part still works perfectly because the dropdowns submit the correct numeric value
            values = [float(request.form[f]) for f in FIELDS]
            prediction = round(model.predict([values])[0], 2)
        except Exception as e:
            prediction = f"Error: {e}"
    
    # NEW: Pass the lists of names to the template
    return render_template_string(
        HTML_TEMPLATE,
        fields=FIELDS,
        prediction=prediction,
        city_names=city_names,
        company_names=company_names
    )

from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify(message="Hello from Flask on Vercel!")
if __name__ == "__main__":
    app.run(debug=True)