from dotenv import load_dotenv
load_dotenv() ## loading all the environment variables

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# initialize our streamlit app

st.set_page_config(page_title="Q&A Demo")

st.header("Gemini LLM Application")

# initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []


input = st.text_input("Input:", key="input")
submit = st.button("Ask the question")

if submit and input:
    response=get_gemini_response(input)
    ## Add user query and response to seession chat history

    st.session_state['chat_history'].append(("You", input))
    st.subheader("The response is ")

    for chunk in response:
    # Concatenate bot's responses into a single line
        bot_response = " ".join(chunk.text for chunk in response)
        st.write(f"Bot: {bot_response}")
    st.session_state['chat_history'].append(("Bot", bot_response))
st.subheader("The chat history is")

for role, text in st.session_state["chat_history"]:
    st.write(f"{role}: {text}")
    #st.markdown("---") # Add a separator line between each discussion
    st.markdown("<hr>", unsafe_allow_html=True)  # Use HTML for the separator line
    #st.text("------------------------------------------------------")  # Use st.text for separator