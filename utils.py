import streamlit as st
import deepl
import os
from embedchain import App
from embedchain import OpenSourceApp
from embedchain import Llama2App


# import pandas as pd
from streamlit.logger import get_logger
logger = get_logger(__name__)

@st.cache_resource()
def get_translator():
     auth_key = "2189c316-4cf5-225f-4602-ab2ee1dab2f8:fx"  # Replace with your key
     translator = deepl.Translator(auth_key)
     return translator

# sample usage
# result = translator.translate_text("Hello, world!", target_lang="FR")
# print(result.text)  # "Bonjour, le monde !"

# Create a bot instance
os.environ["OPENAI_API_KEY"] = st.secrets["openai_key"]
os.environ['REPLICATE_API_TOKEN'] = st.secrets["replicate_key"]

@st.cache_resource()
def load_app():
    
#     bot = OpenSourceApp() # downloads models
     # bot = Llama2App()
     bot = App()

     # Embed online resources
     bot.add("web_page", "https://en.wikipedia.org/wiki/Elon_Musk")
     bot.add("web_page", "https://tesla.com/elon-musk")
     bot.add("youtube_video", "https://www.youtube.com/watch?v=MxZpaJK74Y4")
# naval_chat_bot.add("pdf_file", "https://navalmanack.s3.amazonaws.com/Eric-Jorgenson_The-Almanack-of-Naval-Ravikant_Final.pdf")

     return bot

def send_email(receiver_email, random_password):
     import smtplib

     # Set up the SMTP server
     smtp_server = "smtp.gmail.com"
     port = 587
     sender_email = "nicopepe06@gmail.com"
     password = "psysalapteqxkmtw"

     # Create a secure SSL/TLS connection
     server = smtplib.SMTP(smtp_server, port)
     server.starttls()

     # Login to the server
     server.login(sender_email, password)

     # Compose the email
     receiver_email = receiver_email
     subject = "Forgot Password"
     body = f"That is the new password!, password {random_password}"
     message = f"Subject: {subject}\n\n{body}"

     # Send the email
     server.sendmail(sender_email, receiver_email, message)

     # Close the connection to the server
     server.quit()
