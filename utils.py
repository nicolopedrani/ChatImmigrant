import streamlit as st
import deepl
import os
from embedchain import App
from embedchain.llm.openai import OpenAILlm
from embedchain.config import LlmConfig

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

@st.cache_resource(show_spinner=False)
def set_keys():

     os.environ["OPENAI_API_KEY"] = st.secrets["openai_key"]
     # os.environ['REPLICATE_API_TOKEN'] = st.secrets["replicate_key"]

@st.cache_resource()
def load_bot():
    
     # bot = OpenSourceApp() # downloads models
     # bot = Llama2App()
     # bot = App()
     bot = App(llm=OpenAILlm(), llm_config=LlmConfig(model="gpt-4",temperature=0))
     
     # Embed Online Resources
     bot.add("https://en.wikipedia.org/wiki/Immigration_to_Europe")
     bot.add("https://www.europarl.europa.eu/factsheets/en/sheet/152/immigration-policy")
     bot.add("https://www.youtube.com/watch?v=uQqmRkhuMWU")
     bot.add("https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:52015DC0240")
     bot.add("https://www.europarl.europa.eu/news/en/headlines/society/20170629STO78629/the-eu-response-to-migration-and-asylum")
     bot.add("https://www.europarl.europa.eu/news/en/headlines/world/20200624STO81906/exploring-migration-causes-why-people-migrate")


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
