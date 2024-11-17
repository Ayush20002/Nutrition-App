import streamlit as st
import google.generativeai as genai
import pandas as pd
import numpy as np
import os
from joblib import load
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Generative AI with API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load pre-trained models
logreg_binary = load('logistic_regression_binary.pkl')
rf_multiclass = load('random_forest_multiclass.pkl')
rf_hypertension = load('random_forest_hypertension.pkl')
linear_reg_bmi = load('linear_regression_bmi.pkl')

# Function to get the response from the generative AI model
def get_gemini_response(input_prompt):
    model = genai.GenerativeModel('gemini-1.5-pro-exp-0801')
    response = model.generate_content([input_prompt])
    return response.text

# Function to calculate BMI
def calculate_bmi(weight, height):
    return weight / ((height / 100) ** 2) if height > 0 else None

# Streamlit UI setup
def main():
    st.set_page_config(page_title="Health Assessment Tool")
    st.header("Health Assessment Tool")

    # Collect user inputs for health metrics
    st.subheader("Enter Your Health Data")
    age = st.number_input("Enter your age", min_value=0, max_value=120, step=1)
    sex = st.selectbox("Select your sex", options=["Male", "Female"])
    systolic_bp = st.number_input("Enter your systolic blood pressure (mm Hg)", min_value=0)
    diastolic_bp = st.number_input("Enter your diastolic blood pressure (mm Hg)", min_value=0)
    heart_rate = st.number_input("Enter your heart rate (bpm)", min_value=0)
    weight = st.number_input("Enter your weight (kg)", min_value=0.0, format="%.1f")
    height = st.number_input("Enter your height (cm)", min_value=0.0, format="%.1f")

    # Calculate BMI
    bmi = calculate_bmi(weight, height)

    # Prepare features for model predictions
    features = [[age, 1 if sex == "Female" else 0, systolic_bp, diastolic_bp, heart_rate, bmi]]

    # Display the comparison table after input
    if st.button("Assess Health"):
        # Create a DataFrame for healthy ranges and user's values
        data = {
            "Health Parameter": ["BMI (kg/m²)", "Systolic BP (mm Hg)", "Diastolic BP (mm Hg)", "Heart Rate (bpm)"],
            "Healthy Range": ["18.5 - 24.9", "90 - 120", "60 - 80", "60 - 100"],
            "Your Values": [
                f"{bmi:.1f}" if bmi is not None else "N/A",
                f"{systolic_bp}",
                f"{diastolic_bp}",
                f"{heart_rate}"
            ]
        }
        comparison_table = pd.DataFrame(data)
        st.subheader("Comparison with Healthy Ranges")
        st.table(comparison_table)

        # Model predictions
        binary_health_status = logreg_binary.predict(features)[0]
        multi_class_health_status = rf_multiclass.predict(features)[0]
        hypertension_status = rf_hypertension.predict(features)[0]
        predicted_bmi = linear_reg_bmi.predict(features)[0]

        # Prepare health status from model results
        health_category = {1: "Low Risk", 2: "Moderate Risk", 3: "High Risk"}
        health_status = health_category.get(multi_class_health_status, "Unknown")
        binary_result = "Consult a doctor" if binary_health_status == 1 else "No need to consult a doctor"
        hypertension_result = "Hypertension Detected" if hypertension_status == 1 else "Normal Blood Pressure"

        # Prepare input prompt for the Gemini API
        input_prompt = f"""
        You are a professional healthcare advisor. Based on the provided health parameters, categorize the user's health status into risk levels and provide a recommendation.

        User's Health Parameters:
        - Age: {age}
        - Sex: {sex}
        - Systolic Blood Pressure: {systolic_bp} mm Hg
        - Diastolic Blood Pressure: {diastolic_bp} mm Hg
        - Heart Rate: {heart_rate} bpm
        - Weight: {weight} kg
        - Height: {height} cm
        - BMI: {f"{bmi:.1f}" if bmi is not None else "N/A"}

        Model Predictions:
        - Binary Health Status: {binary_result}
        - Multi-Class Health Status: {health_status}
        - Hypertension Status: {hypertension_result}
        - Predicted BMI: {predicted_bmi:.2f}

        ### Health Status Categorization
        Define the user's health status risk level based on the following criteria:
        1. **BMI (Body Mass Index)**:
           - Low risk: 18.5 - 24.9
           - Moderate risk: 25 - 29.9
           - High risk: below 18.5 or 30 and above

        2. **Blood Pressure**:
           - Low risk: Systolic (90-120 mm Hg) and Diastolic (60-80 mm Hg)
           - Moderate risk: Systolic (121-139 mm Hg) or Diastolic (81-89 mm Hg)
           - High risk: Systolic (140 mm Hg or higher) or Diastolic (90 mm Hg or higher)

        3. **Heart Rate**:
           - Low risk: 60-100 bpm
           - Moderate risk: 101-110 bpm
           - High risk: above 110 bpm

        ### Response Format
        Please categorize the user's health status as follows:
        - **Risk Level (1: Low, 2: Moderate, 3: High)**: Provide a risk level based on an analysis of the user's BMI, blood pressure, and heart rate.
        - **Recommendation**: Provide brief advice based on the categorized risk level.
        """
        
        # Send the prompt to the Gemini model and get the response
        response = get_gemini_response(input_prompt)

        # Display model results and API response
        st.header("Health Assessment Result")
        st.subheader("Model Predictions")
        st.write(f"Binary Health Status: {binary_result}")
        st.write(f"Multi-Class Health Status: {health_status}")
        st.write(f"Hypertension Status: {hypertension_result}")
        st.write(f"Predicted BMI: {predicted_bmi:.2f}")
        
        st.subheader("Gemini API Response")
        st.write(response)

# Run the Streamlit app
if __name__ == "__main__":
    main()
