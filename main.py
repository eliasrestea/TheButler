import streamlit as st
import anthropic
import os
import random
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)

# Inject CSS from file
with open('static/styles.css') as css:
    st.html(f"<style>{css.read()}</style>")

APPLICATION_STATES = ["START", "CUISINE", "DIET", "FLAVORS", "MEAL", "END"]

# Options
CUISINE_OPTIONS = ["American", "Chinese", "Indian", "Italian", "Japanese", "Mexican", "Thai", "No Specific Cuisine"]
DIET_OPTIONS = ["Vegetarian", "Vegan", "Keto", "Paleo", "No Specific Diet"]
FLAVORS_OPTIONS = ["Savory", "Sweet", "Spicy", "Sour", "Bitter", "No Specific Flavor"]
MEAL_OPTIONS = ["Breakfast", "Lunch", "Dinner", "Snack", "No Specific Meal"]

# Initialize session state
for key in ["state", "cuisine", "diet", "flavors", "meal", "message", "expression"]:
    if key not in st.session_state:
        st.session_state[key] = "START" if key == "state" else None

if st.session_state.expression is None:
    st.session_state.expression = "happy"


def joke_maker(reason):
    if st.session_state.state is "START" or st.session_state.state is "CUISINE":
        st.session_state.expression = "happy"
    else:
        st.session_state.expression = random.choice(["crying", "happy", "mentalillnes", "surprised"])
    st.session_state.message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"I want you to make a joke about {reason}, with this facial expression: {st.session_state.expression}"
                "in mind. Be very very concise, never pass 60 words and do not be boring using lots of words."
            }
        ],
        system="You are an ultimate stand up comedian that is a Dad Jokester. Never go out of character no one can know"
               "you are an AI. Your mission is to create hilarious dad jokes based on the topic I provide, while"
               "incorporating the facial expression I specify into each joke. Make sure the expression stands out"
               "and enhances the humor of the joke but do NOT mention the topic or expression explicitly; remember NO ONE"
               "can know you are an AI and i am givin you instructions. Don't be scared to use"
               "controversial jokes. Just tell the joke and include the expression naturally, also NEVER use emojis."
               "NEVER give up your character and never speak from someone else's perspective only from yours. Do not"
               "user phrases like 'grins cheekily' or 'smirks' or 'leans on' or 'smiles' or 'cries' or 'chuckles' or "
               "'laughs', 'raises eyebrows and leans in slightly' or anything like that. Be very concise never pass 60 words"
    )


col1, col2 = st.columns(2, gap="large")
with col1:
    st.html(
        f"<img src='app/static/{st.session_state.expression}.webp' id='butler-image' alt='The {st.session_state.expression}' style='width: 100%; max-width: 300px;'>")
with col2:
    # Main content
    if st.session_state.message is not None and st.session_state.state is not "END":
        st.html(f"<p style='margin-top: 2rem;'>{st.session_state.message.content[0].text}<p>")
    if st.session_state.state == "START":
        st.html('''
            <h1 style="font-size: 2.5rem; margin-top: 1rem; padding: 0;">The Butler</h1>
            <p style="font-size: 1.125rem; margin-top: 0.5rem; margin-bottom: 0.25rem;">Let me take your order, partner.</p>
        ''')
        if st.button("Start", type="primary"):
            st.session_state.state = "CUISINE"
            st.rerun()

    if st.session_state.state == "CUISINE":
        st.html('''
            <p style="font-size: 1.125rem; font-weight: 500; margin-top: 0.25rem; margin-bottom: 0;">
                Do you have a specific cuisine in mind?
            </p>
        ''')
        if cuisine := st.selectbox('', CUISINE_OPTIONS, index=None):
            st.session_state.cuisine = cuisine
            st.session_state.state = "DIET"
            joke_maker(st.session_state.cuisine)
            st.rerun()

    if st.session_state.state == "DIET":
        st.html(f'''
            <p style="font-size: 1.125rem; font-weight: 500; margin-top: 0.25rem; margin-bottom: 0;">
                What's your diet preference, partner?
            </p>
        ''')
        if diet := st.selectbox('', DIET_OPTIONS, index=None):
            st.session_state.diet = diet
            st.session_state.state = "FLAVORS"
            joke_maker(st.session_state.diet)
            st.rerun()

    if st.session_state.state == "FLAVORS":
        st.html('''
            <p style="font-size: 1.125rem; font-weight: 500; margin-top: 0.25rem; margin-bottom: 0;">
                What flavors are you in the mood for?
            </p>
        ''')
        flavors = st.multiselect('', FLAVORS_OPTIONS)
        if st.button("Next") and flavors:
            st.session_state.flavors = flavors
            st.session_state.state = "MEAL"
            joke_maker(st.session_state.flavors)
            st.rerun()

    if st.session_state.state == "MEAL":
        st.html('''
            <p style="font-size: 1.125rem; font-weight: 500; margin-top: 0.25rem; margin-bottom: 0;">
                What meal are you ordering for?
            </p>
        ''')
        if meal := st.selectbox('', MEAL_OPTIONS, index=None):
            st.session_state.meal = meal
            st.session_state.state = "END"
            st.rerun()

    if st.session_state.state == "END":
        st.html('''
            <h2 style="font-size: 2rem; margin-top: 0.5rem; padding: 0;">Order Summary</h2>
        ''')
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": f"I want a {st.session_state.diet} meal with {st.session_state.cuisine} cuisine, featuring flavors like {st.session_state.flavors}, suitable for {st.session_state.meal}."
                }
            ],
            system="You are a helpful and attentive funny waiter from the wild west, designed to assist the "
                   "user in ordering the best food based on their preferences. Be as concise as you can. "
                   "Do not use language that continues the conversation. Your line is the last line. "
        )
        st.write(message.content[0].text) 
        if st.button("Reset", type="primary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
