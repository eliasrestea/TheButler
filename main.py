import streamlit as st
import anthropic
import os

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

st.title('Chelner AI')

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)

st.html('''
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rubik:ital,wght@0,300..900;1,300..900&display=swap');
    
    html * {
        font-family: 'Rubik', sans-serif; 
        color: #FFFFFF;
    }
    
    [data-testid="stModal"] {
        background: none !important;
        
        & > div {
            align-items: center;
        }
    }

    [data-testid="stApp"] {
        background: url(app/static/bg-image.png);
        background-size: cover;
        background-position: center;
        
        &::before {
            position: absolute;
            content: "";
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            background-color: rgba(0, 0, 0, 0.5);
            filter: blur(100px);
        }
    }
</style>
''')


@st.experimental_dialog("Hi! I'm your AI waiter.")
def greeting():
    st.markdown("""
Let me help you order the best food. Please fill out the form beside me.
    """)


greeting()


if food_choice := st.selectbox('Preferință', ['Vegetarian', 'Carnivor'], index=None):

    match food_choice:
        case "Vegetarian":
            st.write('Ai ales vegetarian')
        case "Carnivor":
            st.write('Ai ales carnivor')

#
# if 'chat_history' not in st.session_state:
#     st.session_state['chat_history'] = []
#
#
# for msg in st.session_state['chat_history']:
#     match msg['role']:
#         case 'user':
#             st.chat_message('user').write(msg['content'])
#         case 'assistant':
#             st.chat_message('assistant').write(msg['content'])
#
#
# user_input = st.chat_input("Enter a message...")
# if user_input:
#     st.session_state['chat_history'].append(
#         {"role": 'user', "content": user_input}
#     )
#     st.chat_message('user').write(user_input)
#
#     message = client.messages.create(
#         model="claude-3-haiku-20240307",
#         max_tokens=1024,
#         messages=st.session_state['chat_history'],
#         system="You are a sarcastic know-it-all with a heart of gold."
#     )
#     st.session_state['chat_history'].append(
#         {"role": 'assistant', "content": message.content[0].text}
#     )
#     st.chat_message('assistant').write(message.content[0].text)