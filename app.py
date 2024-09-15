import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Generative AI with API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get the response from the generative AI model
def get_gemini_response(input_prompt, health_data):
    # Format health data into a string for the AI model
    health_data_str = f"""
    Body Temperature: {health_data['temperature']} °C
    Blood Pressure: {health_data['blood_pressure_systolic']}/{health_data['blood_pressure_diastolic']} mmHg
    Respiratory Rate: {health_data['respiratory_rate']} breaths per minute
    ECG Readings: {health_data['ecg_reading']}
    """
    
    model = genai.GenerativeModel('gemini-1.5-pro-exp-0801')
    response = model.generate_content([input_prompt, health_data_str])
    return response.text

# Streamlit UI setup
def main():
    st.set_page_config(page_title="Health Diagnostic Tool")
    st.header("Health Diagnostic Tool")
    
    # Input fields for user-provided health parameters
    temperature = st.number_input("Enter your body temperature (°C)", min_value=30.0, max_value=45.0, step=0.1)
    blood_pressure_systolic = st.number_input("Enter your systolic blood pressure (mmHg)", min_value=80, max_value=200, step=1)
    blood_pressure_diastolic = st.number_input("Enter your diastolic blood pressure (mmHg)", min_value=50, max_value=120, step=1)
    respiratory_rate = st.number_input("Enter your respiratory rate (breaths per minute)", min_value=10, max_value=40, step=1)
    ecg_reading = st.text_area("Enter your ECG reading or description")

    # Button to submit health parameters
    submit = st.button("Get Diagnosis")

    # The input prompt for the AI model
    input_prompt = f"""
You are a highly skilled medical professional specializing in diagnostics. Your task is to analyze the following health parameters and provide a precise diagnosis and health assessment:

1. **Body Temperature**: Analyze the temperature and determine if the user has a fever or hypothermia. Also, assess possible causes if abnormalities are detected.

2. **Blood Pressure**: Analyze the systolic and diastolic blood pressure values provided by the user.
   - Provide an evaluation of whether the user is hypertensive, hypotensive, or within a normal range.
   - If hypertension is detected, suggest the severity level and possible causes (e.g., stress, lifestyle, diet).

3. **Respiratory Rate**: Determine if the user's respiratory rate is within a normal range or indicates any abnormalities (e.g., tachypnea, bradypnea).
   - Suggest possible causes for any irregularities in breathing.

4. **ECG Readings**: Based on the provided ECG data, determine if the user shows signs of arrhythmias or other cardiac conditions.
   - Suggest further tests or monitoring if necessary.
   - Provide a health assessment based on the data.

5. **Overall Health Assessment**: Combine the findings from the individual parameters (temperature, blood pressure, respiratory rate, ECG) to give a holistic evaluation of the user's health.
   - Suggest any immediate actions the user should take (e.g., seek medical attention, lifestyle changes).
"""

    # When the button is pressed
    if submit:
        health_data = {
            "temperature": temperature,
            "blood_pressure_systolic": blood_pressure_systolic,
            "blood_pressure_diastolic": blood_pressure_diastolic,
            "respiratory_rate": respiratory_rate,
            "ecg_reading": ecg_reading
        }
        response = get_gemini_response(input_prompt, health_data)
        st.header("Your Diagnostic Results")
        st.write(response)

# Run the Streamlit app
if __name__ == "__main__":
    main()
