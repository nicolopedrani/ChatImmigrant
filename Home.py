import streamlit as st
from langchain.schema import messages_to_dict

st.set_page_config(
     page_title='European QA chatbot for Immigration',
     layout = 'wide',
     page_icon = "🇪🇺",
     # initial_sidebar_state = 'collapsed',
     menu_items = {
          'About': 'https://www.linkedin.com/in/nicolo-pedrani/',
          'Get Help': 'https://github.com',
          'Report a bug': 'https://github.com'
     }
)

from utils import *

# if 'messages' not in st.session_state:
st.session_state.setdefault("messages", [])

set_keys()
bot = load_bot()

st.title("Chat About Immigration policies")

for message in st.session_state.messages:
    if message["role"]=='user':
            cols = st.columns([1,2])
            with cols[1]:
                st.chat_message(message["role"],avatar="🧑‍💻").markdown(message["content"])
    elif message["role"]=='assistant':
            cols = st.columns([2,1])
            with cols[0]:
                st.chat_message(message["role"], avatar="🤖").markdown(message["content"])
                    
if prompt := st.chat_input("ask a question about Immigration"):

    # Query the bot
    query = prompt

    cols = st.columns([1,2])
    with cols[1]:
        st.chat_message("user", avatar="🧑‍💻").markdown(query)
    
    answer = bot.chat(query) # remember 5 questions
    cols = st.columns([2,1])
    with cols[0]:
        st.chat_message("assistant",avatar="🤖").markdown(answer) 

    st.session_state.messages.append({"role": "user", "content": query})
    st.session_state.messages.append({"role": "assistant", "content": answer})

    cols = st.columns([1,2])
    with cols[0]:
        with st.expander("Want to Download chat history?"):
            text_chat = f"Chat History: \n"
            for message in st.session_state.messages:
                    text_chat += f"{message['role']}: {message['content']}\n"
            st.download_button('Download Chat History', text_chat, file_name=f'chat_about_immigration.txt')
