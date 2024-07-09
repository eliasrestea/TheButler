import streamlit as st
import anthropic
import os
import random

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
    [data-testid="column"] {
        padding: 20px;
        background-color: rgb(14, 17, 23);
        border-radius: 10px;
        text-align: center;
    [data-testid="stImage"] {
      display: block;
      margin-left: auto;
      margin-right: auto;
      width: 50%;
    }
    [data-testid="stTextInput"] {
        margin-top: 20px;
        }
    [data-testid="stHorizontalBlock"] {
        display: flex;
       align-items: flex-start;
        }
</style>
''')

if "greeted" not in st.session_state:
    st.session_state.greeted = False

if "prompt" not in st.session_state:
    st.session_state['prompt'] = []

if "diet_preference" not in st.session_state:
    st.session_state.diet_preference = None

if "food_preference" not in st.session_state:
    st.session_state.food_preference = None


def greeting():
    st.markdown("""
Let me help you order the best food. Please fill out the form beside me.
    """)


def display_joke(diet):
    if diet == "Vegetarian":
        joke = random.choice([
            "Save a cow, eat a vegetarian!",
            "What do you call it when one chickpea murders another? A hummus-cide.",
            "Why did the tomato turn red? Because it saw the salad dressing!",
            "What do you call a fake noodle? An impasta.",
            "Why did the tofu cross the road? To prove he wasn't chicken.",
            "What do you call a sad strawberry? A blueberry.",
        ])
    else:
        joke = random.choice([
            "Why did the short carnivore hate poker? Because the steaks were too high.",
            "What do you call a cow with no legs? Ground beef.",
            "What do you call a cow with a twitch? Beef jerky.",
            "What do you call a cow during an earthquake? A milkshake.",
            "What do you call a cow that plays the guitar? A moo-sician.",
            "Why did the carnivore pull the plug on his wife when she was in a coma? He didn't like vegetables.",
        ])
    st.write(joke)


def user_food_choice_input(diet):
    return st.text_input(f"What specific {diet} food would you like to eat?")


def prompt_content(diet, food):
    return f"I am craving {food} today. I am a {diet}."


def clear_session_state():
    for key in list(st.session_state.keys()):
        del st.session_state[key]


col1, col2 = st.columns(2, gap="large")
with col1:
    st.image("static/butler.png", width=150)
    if not st.session_state.greeted:
        greeting()
        st.session_state.greeted = True
    if st.session_state['prompt']:
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            messages=st.session_state['prompt'],
            system="You are a helpful and attentive waiter from the wild west, designed to assist the user in "
                   "ordering the best food based on their preferences. Be as concise as you can. Do not use language "
                   "that continues the conversation. Your line is the last line."
        )
        st.write(message.content[0].text)
    elif st.session_state.diet_preference is not None and st.session_state['prompt'] == []:
        display_joke(st.session_state.diet_preference)
with col2:
    if st.session_state.diet_preference is None:
        diet_preference = st.selectbox('Preference', ['Vegetarian', 'Carnivor'], index=None)
        if diet_preference:
            st.session_state.diet_preference = diet_preference
            st.rerun()
    elif st.session_state.food_preference is None:
        st.write(f"You are a {st.session_state.diet_preference}")
        food_preference = user_food_choice_input(diet=st.session_state.diet_preference)
        if food_preference:
            st.session_state.food_preference = food_preference
        if st.session_state.food_preference:
            st.session_state['prompt'].append(
                {"role": 'user', "content": prompt_content(st.session_state.diet_preference, st.session_state.food_preference)}
            )
            st.rerun()
    else:
        st.write(f"Your are a {st.session_state.diet_preference}")
        st.write(f"You are craving {st.session_state.food_preference} today.")
        if st.button("Reset"):
            clear_session_state()
            st.rerun()
