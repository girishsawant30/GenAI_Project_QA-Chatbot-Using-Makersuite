from dotenv import load_dotenv
load_dotenv() ## loading all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image as PILImage  # Rename Image to PILImage to avoid conflict

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-pro-vision")
def get_gemini_response(input,image):
    config = {
        "max_output_tokens": 2048,
        "temperature": 0.9,
        "top_p": 1
    }
    
    
    if input != "":
        response = model.generate_content([input, image])
    else:
        response = model.generate_content([image])
    return response.text

# initialize our streamlit app

st.set_page_config(page_title="Gemini Image Demo")
st.header("Gemini LLM Application")
input=st.text_input("Input: ", key="input")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = None

if uploaded_file is not None:
    image = PILImage.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me about the image")

# if submit is clicked
if submit and image is not None:
    response = get_gemini_response(input, image)
    st.subheader("The response is")
    st.write(response)

