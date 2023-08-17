import streamlit as st
from langchain.schema import messages_to_dict

st.set_page_config(
     page_title='QA Immigration',
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

set_keys()

authenticator, config = get_credentials()

if st.session_state.logout:

    cols = st.columns([1,2,1])

    with cols[1]:

        tab1, tab2, tab3 = st.tabs(["Sign in", "Sign up", "Manage Access Credentials"])

        with tab1:
            name, authentication_status, username = authenticator.login('Login', 'main')

            if st.session_state["authentication_status"]:
                st.session_state.logout = False
                # authenticator.logout('Logout', 'sidebar', key='unique_key')
                st.write(f'Welcome *{st.session_state["name"]}*')
            elif st.session_state["authentication_status"] is False:
                st.error('Username/password is incorrect')
                st.session_state.logout = True
            elif st.session_state["authentication_status"] is None:
                st.warning('Please enter your username and password')
                st.session_state.logout = True

        with tab2:
            try:
                if authenticator.register_user('Register user', preauthorization=False):
                    st.success('User registered successfully')
            except Exception as e:
                st.error(e)

        with tab3:

            st.write("Forgot Password")
            try:
                username_forgot_pw, email_forgot_password, random_password = authenticator.forgot_password('Forgot password')
                if username_forgot_pw:
                    send_email(receiver_email=email_forgot_password, random_password=random_password)
                    st.success('New password sent securely')
                    # Random password to be transferred to user securely
                else:
                    st.error('Username not found')
            except Exception as e:
                st.error(e)

            st.write("Forgot Username")
            try:
                username_forgot_username, email_forgot_username = authenticator.forgot_username('Forgot username')
                if username_forgot_username:
                    send_email(receiver_email=email_forgot_username, username=username_forgot_username)
                    st.success('Username sent securely')
                    # Username to be transferred to user securely
                else:
                    st.error('Email not found')
            except Exception as e:
                st.error(e)

        # update credential file, on server side
        with open('config.yaml', 'w') as file:
            yaml.dump(config, file, default_flow_style=False)

        # upload modified blob
        upload_config()

else:

    authenticator.logout('Logout', 'sidebar', key='unique_key')

    with st.sidebar:
        with st.expander("Advanced Options"):
            st.write("Update User Details")
            if st.session_state["authentication_status"]:
                try:
                    if authenticator.update_user_details(st.session_state["name"], 'Update user details'):
                        st.success('Entries updated successfully')
                except Exception as e:
                    st.error(e)
            else:
                st.info("you must be logged in to take this action")

            st.write("Reset Password")
            if st.session_state["authentication_status"]:
                try:
                    if authenticator.reset_password(st.session_state["name"], 'Reset password'):
                        st.success('Password modified successfully')
                except Exception as e:
                    st.error(e)
            else:
                st.info("you must be logged in to take this action")
            

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
        
        # answer = bot.query("How many companies does Elon Musk run?")
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
