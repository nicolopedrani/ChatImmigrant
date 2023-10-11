import streamlit as st
import deepl
import os
from embedchain import App
# from embedchain import OpenSourceApp
# from embedchain import Llama2App

import streamlit_authenticator as stauth

# import pandas as pd
from streamlit.logger import get_logger
logger = get_logger(__name__)

@st.cache_resource()
def get_translator():
     auth_key = st.secrets["deepl_key"]  # Replace with your key
     translator = deepl.Translator(auth_key)
     return translator

# sample usage
# result = translator.translate_text("Hello, world!", target_lang="FR")
# print(result.text)  # "Bonjour, le monde !"

@st.cache_resource(show_spinner=False)
def set_keys():

     os.environ["OPENAI_API_KEY"] = st.secrets["openai_key"]
     # os.environ['REPLICATE_API_TOKEN'] = st.secrets["replicate_key"]

@st.cache_resource()
def load_bot():
    
     # bot = OpenSourceApp() # downloads models
     # bot = Llama2App()
     bot = App()

     # Embed online resources
     bot.add("web_page", "https://european-union.europa.eu/live-work-study/immigration-eu_en")
     bot.add("web_page", "https://immigration-portal.ec.europa.eu/general-information/what-category-do-i-fit_en")
     bot.add("pdf_file", "https://www.europarl.europa.eu/erpl-app-public/factsheets/pdf/en/FTU_4.2.3.pdf")
     bot.add("youtube_video", "https://www.youtube.com/watch?v=1rFcAofSXzk")

     return bot

def send_email(receiver_email, random_password=None, username=None):

     import smtplib

     # Set up the SMTP server
     smtp_server = "smtp.gmail.com"
     port = 587
     sender_email = "nicopepe06@gmail.com"
     password = st.secrets["gmail_password"]

     # Create a secure SSL/TLS connection
     server = smtplib.SMTP(smtp_server, port)
     server.starttls()

     # Login to the server
     server.login(sender_email, password)

     # Compose the email
     if random_password:
          receiver_email = receiver_email
          subject = "Forgot Password"
          body = f"That is the new password!, password {random_password}"
          message = f"Subject: {subject}\n\n{body}"
     else:
          receiver_email = receiver_email
          subject = "Forgot Username"
          body = f"This is your username, username {username}"
          message = f"Subject: {subject}\n\n{body}"

     # Send the email
     server.sendmail(sender_email, receiver_email, message)

     # Close the connection to the server
     server.quit()
