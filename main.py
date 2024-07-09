import streamlit as st
import anthropic
import os

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

st.title('Butler AI')

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


if "greeted" not in st.session_state:
    st.session_state.greeted = False

if "prompt" not in st.session_state:
    st.session_state.prompt = {"diet": None, "food": None}

@st.experimental_dialog("Hi! I'm your AI waiter.")
def greeting():
    st.markdown("""
Let me help you order the best food. Please fill out the form beside me.
    """)

@st.experimental_dialog("Tell me more")
def user_food_choice_input(diet_preference):
    st.markdown(f"""
What specific {diet_preference} food you would like to eat?
    """)
    food_preference = st.text_input("")
    if st.button("Next"):
        st.session_state.prompt = {"diet": diet_preference, "food": food_preference}
        st.rerun()


if not st.session_state.greeted:
    greeting()
    st.session_state.greeted = True


if st.session_state.prompt['food'] and st.session_state.prompt['diet']:
    st.write("""ai response here""")
else:
    if diet_preference := st.selectbox('Preference', ['Vegetarian', 'Carnivor'], index=None):
        match diet_preference:
            case "Vegetarian":
                st.write('Ai ales vegetarian')
            case "Carnivor":
                st.write('Ai ales carnivor')
        user_food_choice_input(diet_preference=diet_preference)
