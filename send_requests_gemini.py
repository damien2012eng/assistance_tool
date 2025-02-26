import streamlit as st
from google import genai
import os

client = genai.Client(api_key=os.getenv("GEMINI_FREE_key"))

# Load the knowledge base and system prompt
with open("configs/all_text.txt", "r", encoding="utf-8") as file:
    knowledge = file.read()

with open("configs/system_prompt.txt", "r", encoding="utf-8") as file:
    system_template = file.read()

system_prompt = f"{system_template} {knowledge}"

def getAnswers(questions):
    query = f"<instruction> {system_prompt} <instruction> <question> {questions} <question>"  
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=query,
)

    return response.text


# define the chatbot interface
st.subheader('HE Assistant', divider='rainbow')

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message['role']):
        st.markdown(message['text'])

# get the user input
questions = st.chat_input('Enter you questions here...')
if questions:
    with st.chat_message('user'):
        st.markdown(questions)
    st.session_state.chat_history.append({"role":'user', "text":questions})

    answer = getAnswers(questions)

    with st.chat_message('assistant'):
        st.markdown(answer)
    st.session_state.chat_history.append({"role":'assistant', "text": answer})