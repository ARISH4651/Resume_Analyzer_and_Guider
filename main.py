import os 

import streamlit as st

#set the working directory
working_dir = os.getcwd()

st.tite("DEEPSEEK-R1 CHATBOT🐋")

#file upload widget
uploaded_file=st.file_uploader(" 📑 Upload your files here" , type['Pdf','docx'])

if uploaded_file is not None:
    #define save path
    save_path = os.path.join(working_dir, uploaded_file.name)
    #save the file
    with open(save_path , "wb") as f:
        f.write(uploaded_file.getbuffer())

#text widget to get input from user