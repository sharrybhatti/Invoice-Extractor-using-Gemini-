import os
import streamlit as st 

from dotenv import load_dotenv
load_dotenv()
from PIL import Image
import google.generativeai as genai 

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

model=genai.GenerativeModel('gemini-1.5-flash')

def get_gemini_response(input,image,prompt):
    response=model.generate_content([input,image[0],prompt])
    return response.text


def input_image_details(uploaded_file):
    """
    Processes the uploaded file and returns its MIME type and byte data.

    Parameters:
    uploaded_file: An uploaded file object.

    Returns:
    A list containing a dictionary with the MIME type and byte data of the uploaded file.

    Raises:
    FileNotFoundError: If no file is uploaded.
    """
    # Check if a file has been uploaded
    if uploaded_file is None:
        raise FileNotFoundError("No file uploaded")

    # Read the file into bytes and create the image parts dictionary
    return [{
        "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
        "data": uploaded_file.getvalue()   # Read the file into bytes
    }]

##initialize our streamlit app

st.set_page_config(page_title="Multi Language Invoice Extractor")

st.header("Invoice Extractor")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image of an inovice..", type=["jpg", "jpeg", "png"])
image="" 
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption='Uploaded Image',use_column_width=True)

submit=st.button('Tell me about Invoice')

input_prompt ="""
             You are an expert in understanding invoices.You will receive input images as invoices &
               you will have to answer questions based on the input image
               """


## If ask button is clicked

if submit:
    image_data = input_image_details(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The Response is")
    st.write(response)