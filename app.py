import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image


load_dotenv()


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


SAVE_DIR = r"D:\Saved Images"  # Path updated to "D:\Saved Images"


if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)


def save_image_locally(uploaded_file):
    # Create a path to save the image
    save_path = os.path.join(SAVE_DIR, uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

# Function to handle the image upload and setup
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Save the image locally without notification
        save_image_locally(uploaded_file)

        # Prepare image for AI processing
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
        You are an expert nutritionist. Analyze the food items in the image and calculate the total 
        calories. Provide the details in the following format:
        1. Item 1 - no of calories
        2. Item 2 - no of calories
        Then calculate the total calories
        
        Finally, mention whether the food is healthy or not.
        """
        
        # When the button is pressed
        if submit:
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_response(input_prompt, image_data)
            
            # Display the response without showing the save path
            st.header("Your food details")
            st.write(response)

# Run the Streamlit app
if __name__ == "__main__":
    main()
