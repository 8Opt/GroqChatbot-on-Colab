# The code is heavenly inspired by: https://github.com/dataprofessor/llama2.git

import os
from dotenv import load_dotenv

import streamlit as st

from groq import Groq

from src.schema import GenerationConfig
from src.agent import generate_response

load_dotenv()

supported_model = {"LLaMA3 8b": "llama3-8b-8192", 
                    "LLaMA3 70b": "llama3-70b-8192", 
                    "Mixtral 8x7b": "mixtral-8x7b-32768",
                    "Gemma 7b": "gemma-7b-it", 
                    }

# ================

# App title
# st.set_page_config(page_title="💬 GROQ Chatbot")


# Groq Credentials
with st.sidebar:
    st.title('💬 GROQ Chatbot')
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    if GROQ_API_KEY:
        st.success('API key already provided!', icon='✅')
        agent = Groq(api_key=GROQ_API_KEY)
    else:
        GROQ_API_KEY = st.text_input('Enter GROQ API token:', type='password')
        if not (GROQ_API_KEY.startswith('gsk_') and len(GROQ_API_KEY)==40):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')

    st.subheader('Models and parameters')
    selected_model = st.sidebar.selectbox('We serve: ', supported_model.keys(), key='selected_model')
    llm = supported_model[selected_model]

    temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=5.0, value=0.1, step=0.01)
    top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.sidebar.slider('max_length', min_value=64, max_value=4096, value=512, step=8)

    gen_config = GenerationConfig(temperature=temperature, 
                                  top_p=top_p, 
                                  max_tokens=max_length)


# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Hi! How can I help you?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Hi! How can I help you?"}]

st.sidebar.button('Clear Chat History', on_click=clear_chat_history)


# User-provided prompt
if prompt := st.chat_input(disabled=not GROQ_API_KEY):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(client=agent, 
                                         model=llm,
                                         prompt=prompt, 
                                         config=gen_config)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)