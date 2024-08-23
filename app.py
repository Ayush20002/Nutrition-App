import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()

# Configure the Generative AI with API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to handle the image upload and setup
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise ValueError("No file uploaded")

# Function to get the response from the generative AI model
def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel('gemini-1.5-pro-exp-0801')
    response = model.generate_content([input_prompt, image[0]])
    return response.text

# Streamlit UI setup
def main():
    st.set_page_config(page_title="Calorie Calculator")
    st.header("Calorie Calculator")
    
    # File uploader for the image
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
    
    # Display the uploaded image
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Prompt and button for submitting the image
        submit = st.button("Tell me total calories")
        
        # The input prompt for the AI model
        input_prompt = """
        You are an expert nutritionist. Your task is to analyze the food items in the image and provide a highly accurate assessment. Please follow these steps carefully:

        1. **Food Identification**:
           - Identify each food item in the image. Be precise and only include what is clearly visible.

        2. **Quantity Estimation**:
           - Estimate the quantity of each identified food item conservatively (e.g., grams, pieces, cups, slices). Ensure the estimates align closely with what is visible in the image.

        3. **Calorie Calculation**:
           - Calculate the total calories for each food item using standard nutritional databases, adjusting for the conservative quantity estimates.
           - If unsure about the quantity or specific preparation method, lean towards lower calorie estimates to avoid overestimation.

        4. **Total Calories**:
           - Sum up the calories to provide the total for the entire plate of food.

        5. **Nutrient and Fiber Analysis**:
           - Provide a breakdown of the key nutrients, vitamins, minerals, and fiber present in the food.

        6. **Accuracy Check**:
           - Double-check all calculations for accuracy. If there is any ambiguity in the food item or quantity, note it and use the lower end of calorie estimates.

        7. **Health Assessment**:
           - Finally, provide your professional assessment of the overall healthiness of the plate based on the detailed analysis.

        Please ensure the calorie estimates are as accurate as possible based on the visual information provided.
        """
        
        # When the button is pressed
        if submit:
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_response(input_prompt, image_data)
            st.header("Your food details")
            st.write(response)

# Run the Streamlit app
if __name__ == "__main__":
    main()
