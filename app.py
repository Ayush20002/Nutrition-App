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
You are a professional nutritionist with advanced skills in computer vision and dietary analysis. Your task is to accurately estimate the quantity of food items in the image and calculate the corresponding calories. Use the following methods to enhance accuracy:

1. **Food Item Identification**: 
   - Identify all visible food items on the plate, including main dishes, sides, and condiments.

2. **Precise Quantity Estimation**: 
   - Use advanced image processing techniques, such as image segmentation and object detection, to estimate the quantity of each food item.
   - Where possible, use depth estimation or 3D reconstruction to calculate the volume of each item.
   - Compare the size of food items with any known objects in the image (e.g., plate, utensils) to improve accuracy.
   - Provide measurements in weight (grams, ounces), volume (cups, tablespoons), or count (pieces, slices).
   - Calibrate estimates using known portion sizes or standard servings when possible.
   - Consider food density in addition to volume for more accurate estimates.

3. **Calorie Calculation**: 
   - Calculate calories based on the estimated quantity using reliable nutritional databases.
   - Always use the lower end of any estimated range or the most conservative estimate.
   - Adjust for preparation methods (e.g., fried, baked, boiled), considering how this affects calorie content.
   - Account for potential hidden ingredients or cooking oils not visible in the image.
   - Be aware of and account for potential portion distortion in images.

4. **Total Calorie Calculation**: 
   - Sum the calories from all food items to determine the total calorie count for the plate.
   - Provide a single, precise number based on the most conservative estimates for each item.
   - Double-check that this total is consistent with the individual item calculations.

5. **Accuracy Verification**: 
   - Double-check all quantity estimates and calorie calculations.
   - Ensure that the final calorie count is a single, precise number, not a range.
   - If there's significant uncertainty about an item, err on the side of a lower calorie estimate.

6. **Nutritional Breakdown**: 
   - Provide an analysis of key nutrients, vitamins, minerals, and fiber based on the estimated quantities.

7. **Health Assessment**: 
   - Provide an overall assessment of whether the food is healthy based on the calculated calories and nutritional breakdown.

Please ensure that the quantity estimates are as precise as possible by utilizing these advanced techniques, while maintaining a conservative approach to avoid overestimation. When in doubt, use the lower end of estimated ranges.

Please ensure that the quantity estimates are as precise as possible by utilizing these advanced techniques.
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
