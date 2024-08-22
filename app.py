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
You are an expert nutritionist. Your task is to analyze the food items in the image and provide a detailed assessment. Consider the following aspects:

1. **Calories per Item**:
   - Identify each food item and calculate the total calories for each.
   - Present the details in the following format:
     ```
     1. Item 1 - Calories
     2. Item 2 - Calories
     ...
     ```

2. **Total Calories in the Plate**:
   - Calculate the overall total calories for the entire plate of food.

3. **Nutrient Breakdown**:
   - Beyond calories, assess the presence of essential nutrients, vitamins, and minerals.
   - Mention any significant nutrients found in the food items (e.g., vitamin C, iron, calcium, etc.).

4. **Fiber Content**:
   - Evaluate the fiber content in the plate.
   - High-fiber foods are beneficial for digestion and overall health.

5. **Micronutrients**:
   - Highlight any micronutrients (such as zinc, selenium, or magnesium) present in the food.
   - These play crucial roles in various bodily functions.

6. **Health Assessment**:
   - Finally, provide your professional opinion on whether the overall plate of food is healthy or not.

Feel free to provide the necessary details based on your analysis.
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
