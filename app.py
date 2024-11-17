import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Generative AI with API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get the response from the generative AI model
def get_gemini_response(input_prompt):
    # Create a GenerativeModel instance with the correct model ID
    model = genai.GenerativeModel('gemini-1.5-pro-exp-0801')
    # Generate content based on the input prompt
    response = model.generate_content([input_prompt])
    return response.text

# Streamlit UI setup
def main():
    # Set up the Streamlit page
    st.set_page_config(page_title="Health Assessment Tool")
    st.header("Health Assessment Tool")

    # Collect user inputs for health metrics
    age = st.number_input("Enter your age", min_value=0, max_value=120, step=1)
    sex = st.selectbox("Select your sex", options=["Male", "Female"])
    systolic_bp = st.number_input("Enter your systolic blood pressure (mm Hg)", min_value=0)
    diastolic_bp = st.number_input("Enter your diastolic blood pressure (mm Hg)", min_value=0)
    heart_rate = st.number_input("Enter your heart rate (bpm)", min_value=0)
    weight = st.number_input("Enter your weight (kg)", min_value=0.0, format="%.1f")
    height = st.number_input("Enter your height (cm)", min_value=0.0, format="%.1f")

    # Button to assess health status
    submit = st.button("Assess Health")

    # Prepare the input prompt for the API
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

    ### Health Status Categorization
    Define the user's health status risk level based on the following criteria:
    1. *BMI (Body Mass Index)*:
       - Low risk: 18.5 - 24.9
       - Moderate risk: 25 - 29.9
       - High risk: below 18.5 (underweight) or 30 and above (overweight/obese)

    2. *Blood Pressure*:
       - Low risk: Systolic (90-120 mm Hg) and Diastolic (60-80 mm Hg)
       - Moderate risk: Systolic (121-139 mm Hg) or Diastolic (81-89 mm Hg)
       - High risk: Systolic (140 mm Hg or higher) or Diastolic (90 mm Hg or higher)

    3. *Heart Rate*:
       - Low risk: Resting heart rate of 60-100 bpm
       - Moderate risk: Resting heart rate of 101-110 bpm
       - High risk: Resting heart rate above 110 bpm

    ### Response Format
    Please categorize the user's health status as follows:
    - *Risk Level (1: Low, 2: Moderate, 3: High)*: Provide a risk level based on an analysis of the user's BMI, blood pressure, and heart rate.
    - *Recommendation*: Provide brief advice based on the categorized risk level.

    ### Example Response
    Risk Level: 2 (Moderate)
    Recommendation: "Your blood pressure and BMI are slightly elevated. Consider regular monitoring and lifestyle changes. Consultation with a healthcare provider is recommended for personalized advice."

    Please analyze and provide a response following this format.
    """

    # When the button is pressed
    if submit:
        try:
            # Send the prompt to the Gemini model and get the response
            response = get_gemini_response(input_prompt)
            
            # Display the API response as the health assessment
            st.header("Health Assessment Result")
            st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Run the Streamlit app
if __name__ == "__main__":
    main()
