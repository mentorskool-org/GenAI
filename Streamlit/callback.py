import streamlit as st

st.set_page_config(page_title='Learning Callback!', initial_sidebar_state='expanded')
st.title('Learning Callback!')

'st.session_state object:', st.session_state

# 1. On_change
def kg_to_lbs():
    st.session_state.lbs = st.session_state.kg*2.2046

def lbs_to_kg():
    st.session_state.kg = st.session_state.lbs/2.2046

col1, col2 = st.columns(2)

with col1:
    pounds = st.number_input('Pounds:', key="lbs", on_change=lbs_to_kg)

with col2:
    kilogram = st.number_input('Kilograms:', key='kg', on_change=kg_to_lbs)


# 2. on_click
def take_input():
    prompt = st.chat_input('Give your name:', key='name')


button = st.button('Click here to display text box:', on_click=take_input)

if "name" in st.session_state and st.session_state.name!=None:
    st.write(f'Hey {st.session_state.name}! How are you?')
