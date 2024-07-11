import time

import streamlit as st
import anthropic
import os

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
for key in ["state", "cuisine", "diet", "flavors", "meal"]:
    if key not in st.session_state:
        st.session_state[key] = "START" if key == "state" else None

# Two columns
col1, col2 = st.columns(2)

with col1:
    # Butler image
    st.html("<img src='app/static/butler.png' id='butler-image' alt='The Butler' style='width: 100%; max-width: 300px;'>")

with col2:
    # Main content
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
            st.rerun()
        st.html('<span style="font-size: 0.875rem; font-weight: 500;">1 of 4</span>')

    if st.session_state.state == "DIET":
        st.html(f'''
            <p style="font-size: 1.125rem; font-weight: 500; margin-top: 0.25rem; margin-bottom: 0;">
                What's your diet preference, partner?
            </p>
        ''')
        if diet := st.selectbox('', DIET_OPTIONS, index=None):
            st.session_state.diet = diet
            st.session_state.state = "FLAVORS"
            st.rerun()
        st.html('<span style="font-size: 0.875rem; font-weight: 500;">2 of 4</span>')

    if st.session_state.state == "FLAVORS":
        st.html('''
            <p style="font-size: 1.125rem; font-weight: 500; margin-top: 0.25rem; margin-bottom: 0;">
                What flavors are you in the mood for?
            </p>
        ''')
        flavors = st.multiselect('', FLAVORS_OPTIONS)
        if st.button("Next", type="primary") and flavors:
            st.session_state.flavors = flavors
            st.session_state.state = "MEAL"
            st.rerun()
        st.html('<span style="font-size: 0.875rem; font-weight: 500;">3 of 4</span>')

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
        st.html('<span style="font-size: 0.875rem; font-weight: 500;">4 of 4</span>')

    if st.session_state.state == "END":
        st.html('''
            <h2 style="font-size: 2rem; margin-top: 0.5rem; padding: 0;">Summary</h2>
        ''')
        st.write(f"Cuisine: {st.session_state.cuisine}")
        st.write(f"Diet: {st.session_state.diet}")
        st.write(f"Flavors: {', '.join(st.session_state.flavors)}")
        st.write(f"Meal: {st.session_state.meal}")

if st.session_state.state == "END":
    with st.container(border=True):
        with st.status("Thinking 🤔...", expanded=True) as status:
            # Get assistant response
            message = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1024,
                system="You are a helpful butler that takes into account the user's prefered cuisine, diet, flavours and meal to suggest an appropriate dish."
                       "You are also a cowboy, so you speak in a cowboy accent and address the user as 'partner'.",
                messages=[
                    {
                        "role": "user",
                        "content": f"I'd like a {st.session_state.meal} dish with {st.session_state.cuisine} cuisine, {', '.join(st.session_state.flavors)} flavors, and {st.session_state.diet} diet."
                    }
                ]
            )
            status.update(label="I think I know what you want...! 🤠")
            time.sleep(1)
            status.update(label="Found it! 🍽", state="complete")

        # Display the response
        st.write(f"{message.content[0].text}")