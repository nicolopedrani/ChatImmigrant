import streamlit as st
# from langchain.schema import messages_to_dict

st.set_page_config(
     page_title='European QA chatbot for Immigration',
     layout = 'wide',
     page_icon = "🇪🇺",
     initial_sidebar_state = 'collapsed',
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

# Embed Online Resources
# bot.add("https://en.wikipedia.org/wiki/Immigration_to_Europe")
# bot.add("https://www.europarl.europa.eu/factsheets/en/sheet/152/immigration-policy")
# bot.add("https://www.youtube.com/watch?v=uQqmRkhuMWU")
# bot.add("https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:52015DC0240")
# bot.add("https://www.europarl.europa.eu/news/en/headlines/society/20170629STO78629/the-eu-response-to-migration-and-asylum")
# bot.add("https://www.europarl.europa.eu/news/en/headlines/world/20200624STO81906/exploring-migration-causes-why-people-migrate")

bot = load_bot()

first_sentence = """ Sometimes it can be very diffult to move to another country, and there are a lot of documents that one must be 
            read carefully before understanding just a little bit about the immigration policies of that country..    """
second_sentence = """ Here we are! by the use of `python`, `emdebchain` and `chatgpt` we have implemented a chatbot that from different resources try to
            answer to all of your questions about european immigration policies!"""

target_langs = (
'EN-GB - English (British)',
'BG - Bulgarian',
'CS - Czech',
'DA - Danish',
'DE - German',
'EL - Greek',
'EN-US - English (American)',
'ES - Spanish',
'ET - Estonian',
'FI - Finnish',
'FR - French',
'HU - Hungarian',
'ID - Indonesian',
'IT - Italian',
'JA - Japanese',
'KO - Korean',
'LT - Lithuanian',
'LV - Latvian',
'NB - Norwegian (Bokmål)',
'NL - Dutch',
'PL - Polish',
'PT-BR - Portuguese (Brazilian)',
'PT-PT - Portuguese (all Portuguese varieties excluding Brazilian Portuguese)',
'RO - Romanian',
'RU - Russian',
'SK - Slovak',
'SL - Slovenian',
'SV - Swedish',
'TR - Turkish',
'UK - Ukrainian',
'ZH - Chinese (simplified)'
)

dict_target_langs = { element : element.split(' - ')[0] for element in target_langs }

translator = get_translator()

with st.container():
    
    cols = st.columns([1,3,1])
    with cols[1]:
        st.title('European QA chatbot for Immigration')
    cols = st.columns([1,1,1,1,1])
    with cols[2]:
        st.selectbox(
                'Language',
                target_langs, key='destination_language')
    
    first_sentence = translator.translate_text(first_sentence, target_lang=dict_target_langs[st.session_state.destination_language]).text
    second_sentence = translator.translate_text(second_sentence, target_lang=dict_target_langs[st.session_state.destination_language]).text

    st.markdown(first_sentence)
    st.markdown("""----------------""")
    st.markdown(second_sentence)   

if 'openaikey' not in st.session_state:
     st.session_state.setdefault("openaikey", '')

with st.container():

     with st.sidebar:
          with st.expander("Some Resources"):
               st.link_button(label='european resources',url="https://www.europarl.europa.eu/factsheets/en/sheet/152/immigration-policy")
            
st.title("Chat About EU Immigration policies 🇪🇺 💬 🤖")

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
