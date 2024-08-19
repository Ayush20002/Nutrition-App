import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image


load_dotenv()


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


SAVE_DIR = r"D:\Saved Images"  


if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)


def save_image_locally(uploaded_file):
    
    save_path = os.path.join(SAVE_DIR, uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

]
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        ]
        save_image_locally(uploaded_file)

        
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


def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel('gemini-1.5-pro-exp-0801')
    response = model.generate_content([input_prompt, image[0]])
    return response.text


def main():
    st.set_page_config(page_title="Calorie Calculator")
    st.header("Calorie Calculator")
    
   
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
       
        submit = st.button("Tell me total calories")
        
       
        input_prompt = """
        You are an expert nutritionist. Analyze the food items in the image and calculate the total 
        calories. Provide the details in the following format:
        1. Item 1 - no of calories
        2. Item 2 - no of calories
        Then calculate the total calories
        
        Finally, mention whether the food is healthy or not.
        """
        
       
        if submit:
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_response(input_prompt, image_data)
            
            
            st.header("Your food details")
            st.write(response)


if __name__ == "__main__":
    main()
